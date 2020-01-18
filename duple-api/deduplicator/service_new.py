from quart import Quart
from quart_cors import cors, route_cors
from deduplicator.deduplicate import (
    training_pairs,
    data_prep,
    deduper_prep,
    deduper_sample,
)
import pandas as pd
import json

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

app = Quart(__name__)

@app.route("/")
async def index():
    return {"hello": "world"}


@app.route("/training")
@route_cors(allow_origin="*")
async def training():
    return json.dumps(training_buffer)


@app.route("/matching", methods=['POST'])
@route_cors(allow_origin="*", allow_headers=["content-type"], allow_methods=["POST"])
async def matching(request):
    match_json = await request.get_data()
    dd.markPairs(match_json)
    training_buffer = training_pairs(dd)
    return json.dumps(training_buffer)

def run():
    # app.run(port=5000, certfile='server.crt', keyfile='server.key')
    app.run()
