from duple import logger
from duple.message import message_wrapper
from duple.datastore import get_datastore, delete_datastore
import duple.worker as worker


from multidict import MultiDict
from aiohttp import web
from aiohttp_swagger import setup_swagger
import aiohttp_cors

import os
import shutil
import asyncio
import shortuuid

routes = web.RouteTableDef()
app = web.Application()


@routes.get("/register")
async def register(request):
    """Registers a new client with duple.

    ---
    description: Supplies a unique client identifier.
    tags:
    - Results
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return client id.
    """
    client_id = shortuuid.uuid(request.headers.get("token"))
    return web.json_response({"clientId": client_id})


@routes.post("/existing")
async def existing(request):
    """File upload endpoint using existing model.

    ---
    description: Recieves data for deduplication.
    tags:
    - Upload
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return confirmation response.
    """
    client_id = request.headers.get("clientId")
    logger.debug("Recieving data for classification")
    reader = await request.multipart()
    field = await reader.next()
    filepath = os.path.join("profile-data/", client_id, field.filename)
    size = 0

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    message = message_wrapper(
        client_id,
        {"use_model": True, "filepath": filepath})
    await app["message_queue"].put(message)

    return web.json_response({"recieved": field.filename, "size": size})


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
    client_id = request.headers.get("clientId")
    logger.debug("Recieving data for classification")
    reader = await request.multipart()
    field = await reader.next()
    filepath = os.path.join("profile-data/", client_id, field.filename)
    size = 0

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    message = message_wrapper(client_id, {"filepath": filepath})
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
    client_id = request.headers.get("clientId")
    datastore = get_datastore(client_id)

    if datastore.training_rounds <= 4:
        training_data = await datastore.get_pairs()
        return web.json_response(training_data)
    else:
        return web.json_response([])


@routes.post("/training")
async def training_post(request):
    """Training endpoint for submitting labelled data.

    ---
    description: Accepts labeled data for training the data matching model.
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
        client_id = request.headers.get("clientId")
        datastore = get_datastore(client_id)

        if datastore.training_rounds < 4:
            logger.info("Updating traing pairs for labeling")
            labeled_pairs = await request.json()
            message = message_wrapper(
                client_id,
                {"labeled_pairs": labeled_pairs})
            await app["message_queue"].put(message)
        else:
            message = message_wrapper(client_id, {"labeling_complete": True})
            await app["message_queue"].put(message)
        return web.Response(status=201)

    return web.Response(status=400)


@routes.get("/results")
async def results(request):
    """Results endpoint for retrieving classified data.

    ---
    description: Supplies clustered data containing duplicates.
    tags:
    - Results
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return labeled results.
    """
    client_id = request.headers.get("clientId")
    datastore = get_datastore(client_id)

    if datastore.has_result and datastore.result.size > 0:
        result = datastore.result
        result = (
            result[result.cluster_id > 0]
            .sort_values("cluster_id")
            .to_json(orient="table")
        )
        return web.Response(body=result, content_type="application/json")
    else:
        if await datastore.get_status("training"):
            message = message_wrapper(client_id, {"training_complete": True})
            await app["message_queue"].put(message)
        if await datastore.get_status("dedupe") and datastore.result.size > 0:
            result = datastore.result
            result = (
                result[result.cluster_id > 0]
                .sort_values("cluster_id")
                .to_json(orient="table")
            )
            return web.Response(body=result, content_type="application/json")
        if datastore.result.size <= 0:
            return web.json_response({})


@routes.get("/results/file")
async def results_file(request):
    """Results endpoint for retrieving classified data results file.

    ---
    description: Supplies a file containing duplicates found.
    tags:
    - Results
    produces:
    - text/csv
    responses:
        "200":
            description: successful operation. Return labeled results file.
    """
    params = request.rel_url.query
    datastore = get_datastore(params.get("clientId"))
    if datastore.has_result:
        result = datastore.result
        result = (
            result[result.cluster_id > 0]
            .sort_values("cluster_id")
            .to_csv(mode="wb", index=False)
        )
        return web.Response(
            headers=MultiDict(
                {"Content-Disposition": 'attachment; filename="relateddata.csv"'}
            ),
            body=result,
        )
    else:
        return web.Response(status=503)


@routes.get("/stats")
async def stats(request):
    """Stats endpoint for retrieving classification statistics.

    ---
    description: Supplies information reagarding the records processed.
    tags:
    - Results
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Return duple statistics.
    """
    client_id = request.headers.get("clientId")
    datastore = get_datastore(client_id)
    if datastore.has_result:
        return web.json_response(datastore.stats)
    else:
        return web.json_response({})


@routes.get("/reset")
async def reset(request):
    """Reset endpoint.

    ---
    description: Resets the state of the application and deletes stored data.
    tags:
    - Results
    produces:
    - application/json
    responses:
        "200":
            description: successful operation. Reset duple application data.
    """
    client_id = request.headers.get("clientId")

    profile_data = os.path.join("profile-data/", client_id)
    training_data = os.path.join("training_data/", client_id)
    if os.path.exists(profile_data):
        shutil.rmtree(profile_data)
    if os.path.exists(training_data):
        shutil.rmtree(training_data)

    delete_datastore(client_id)

    return web.json_response({"reset": "OK"})


async def message_push(queue):
    """Message handler for service messages.

    Puts pending message items on to a queue to be sheduled for processing.
    """
    while True:
        await asyncio.sleep(1)
        message = await app["message_queue"].get()
        asyncio.create_task(worker.producer(queue, message))


async def on_startup(app):
    """Startup background tasks.

    Schedules message and worker coroutines.
    """
    app["message_queue"] = asyncio.Queue()
    worker_queue = asyncio.Queue()
    asyncio.create_task(message_push(worker_queue))
    asyncio.create_task(worker.consumer(worker_queue))


async def on_shutdown(app, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logger.info(f"Received exit signal, shutting down.")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info(f"Stopping")


def route_cors(host, app):
    """Add cors to all routes for supplied host."""
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


async def create_app():
    """Create service app instance.

    Creates and configures the duple service, sets up CORS and swagger and adds
    the starup and shutdown processes.
    """
    app.add_routes(routes)
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
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


def run():
    """Duple service runnner."""
    logger.info("Starting duple.")
    web.run_app(create_app())
    logger.info("Duple successfully shutdown.")
