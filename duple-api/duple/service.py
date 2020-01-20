from duple import logger
from duple.message import messaage_wrapper
import duple.worker as worker

from aiohttp import web
from aiohttp_swagger import setup_swagger
import aiohttp_cors

import os
import asyncio


def route_cors(host, app):
    logger.info("Configuring cors")
    cors = aiohttp_cors.setup(
        app,
        defaults={
            host: aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    [cors.add(route) for route in list(app.router.routes())]


routes = web.RouteTableDef()
app = web.Application()


@routes.get("/health")
async def health_get(request):
    """Health check endpoint.

    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return status json
    """
    return web.json_response({"status": "UP"})


@routes.post("/upload")
async def upload(request):
    """File upload endpoint.

    ---
    description: Recieves data for training and clasification.
    tags:
    - Upload
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return confirmation response.
    """
    logger.debug("Recieving data for classification")
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == "duple_data"
    assert field.headers["Content-Type"] == "text/csv" or "application/vnd.ms-excel"
    filepath = os.path.join("profile-data/", field.filename)
    size = 0

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    message = messaage_wrapper({"filepath": filepath})
    await app["message_queue"].put(message)
    return web.json_response({"recieved": field.filename, "size": size})


@routes.get("/training")
async def training_get(request):
    """Training endpoint for retrieving sample data.

    ---
    description: Supplies data used to train the duple data matching model.
    tags:
    - Training
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return unlabeled training records.
    """
    logger.debug("Training data request recieved")
    if app["labeling_attempts"] <= 3:
        training_data = await worker.datastore.get_pairs()
        return web.json_response(training_data)
    else:
        return web.json_response([])


@routes.post("/training")
async def training_post(request):
    """Training endpoint for submitting labelled data.

    ---
    description: Accepts labelled data for training the duple data matching model.
    tags:
    - Training
    produces:
    - application/json
    responses:
        "200":
            description: Successful operation. Return further training records.
        "400":
            description: Unsuccessful operation. Labelled date not supplied.
    parameters:
    - in: body
      name: body
      description: Labelled training data
      required: true
      schema:
        type: object
        properties:
          match:
            type: array
            items:
              type: array
              items:
                - $ref: '#/definitions/Person'
                - $ref: '#/definitions/Person'
          distinct:
            type: array
            items:
              type: array
              items:
                - $ref: '#/definitions/Person'
                - $ref: '#/definitions/Person'
    """
    if request.body_exists and request.can_read_body:
        logger.debug("Labelled training data recieved.")
        if app["labeling_attempts"] < 3:
            logger.info("Updating traing pairs for labeling")
            labeled_pairs = await request.json()
            message = messaage_wrapper({"labeled_pairs": labeled_pairs})
            await app["message_queue"].put(message)
            app["labeling_attempts"] += 1
        else:
            message = messaage_wrapper({"labeling_complete": True})
            await app["message_queue"].put(message)
        return web.Response(status=201)

    return web.Response(status=400)


@routes.get("/results")
async def results(request):
    if worker.datastore.has_result:
        result = worker.datastore.result
        result = result[result.cluster_id > 0].to_json(orient="table")
        return web.Response(body=result, content_type="application/json")
    else:
        if await worker.datastore.get_status("training"):
            message = messaage_wrapper({"training_complete": True})
            await app["message_queue"].put(message)
        if await worker.datastore.get_status("dedupe"):
            result = worker.datastore.result
            result = result[result.cluster_id > 0].to_json(orient="table")
            return web.Response(body=result, content_type="application/json")


@routes.get("/stats")
async def stats(request):
    if worker.datastore.has_result:
        pass
    else:
        pass


async def message_push(queue):
    while True:
        await asyncio.sleep(1)
        try:
            message = await app["message_queue"].get()
            asyncio.create_task(worker.producer(queue, message))
        except Exception as e:
            logger.error(f"Failed to queue message with error: {e}")


async def shutdown(loop, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logger.info(f"Received exit signal, shutting down.")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info(f"Stopping")


async def on_startup(app):
    app["labeling_attempts"] = 1
    app["worker_queue"] = asyncio.Queue()
    app["message_queue"] = asyncio.Queue()
    asyncio.create_task(message_push(app["worker_queue"]))
    asyncio.create_task(worker.consumer(app["worker_queue"]))
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(shutdown)


async def on_shutdown(app):
    await shutdown(asyncio.get_running_loop())


def init():
    app.add_routes(routes)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    route_cors("*", app)
    setup_swagger(
        app,
        description="API for duple data deduplication tool",
        title="Duple API",
        api_version="1.0.0",
        contact="info@qonda.io",
        definitions={
            "Person": {
                "type": "object",
                "properties": {
                    "given_name": {"type": "string"},
                    "surname": {"type": "string"},
                    "date_of_birth": {"type": "string"},
                    "sex": {"type": "string"},
                },
            }
        },
    )
    return app


def run():
    logger.info("Starting duple.")
    web.run_app(init())
    logger.info("Duple successfully shutdown.")
