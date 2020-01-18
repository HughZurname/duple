import pandas as pd
import textwrap
import json

import asyncio
from aiohttp import web
import aiohttp_cors

from deduplicator.deduplicate import (
    training_pairs,
    data_prep,
    deduper_prep,
    deduper_sample,
)

routes = web.RouteTableDef()

fields = ["given_name", "surname", ["date_of_birth", "DateTime"], "sex"]
df = pd.read_csv("profile-data/DataShed_Technical_Test.csv")
df["date_of_birth"] = pd.to_datetime(
    df["date_of_birth"], errors="coerce", dayfirst=True
)
df.to_csv("test.csv")
df, data_d = data_prep(df)
dd = deduper_prep(fields)
deduper_sample(dd, data_d, 0.2)
training_buffer = training_pairs(dd)


@routes.get("/")
async def intro(request):
    txt = textwrap.dedent(
        """\
        Type {url}/hello/John  {url}/simple or {url}/change_body
        in browser url bar
    """
    ).format(url="127.0.0.1:8080")
    binary = txt.encode("utf8")
    resp = web.StreamResponse()
    resp.content_length = len(binary)
    resp.content_type = "text/plain"
    await resp.prepare(request)
    await resp.write(binary)
    return resp


@routes.get("/training")
async def training(request):
    return web.json_response(training_buffer)


@routes.post("/matching")
async def matches(request):
    if request.body_exists and request.can_read_body and attempts <= 3:
        match_json = await request.json()
        dd.markPairs(match_json)
        training_buffer = training_pairs(dd)
        return web.json_response(training_buffer)

    return web.Response()


def init():
    app = web.Application()
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    app.router.add_routes(routes)

    for route in list(app.router.routes()):
        cors.add(route)

    return app


def run():
    web.run_app(init())
