import asyncio
from duple import logger

from duple.deduplicate import Deduplicate

import pandas as pd
from dataclasses import dataclass


@dataclass
class DataStore(Deduplicate):
    pairs_buffer: list
    stats: dict
    updating: bool = False
    has_result: bool = False
    training_complete: bool = False
    dedupe_complete: bool = False

    async def model(self, filepath, client_id):
        self.data_frame = pd.read_csv(filepath)

        # FIXME: Hack for Date fields
        self.data_frame["date_of_birth"] = pd.to_datetime(
            self.data_frame["date_of_birth"], errors="coerce", format="%d/%m/%Y"
        )

        self.stats.update({"records": self.data_frame.shape[0]})
        self.deduper = self.dedupe_static(client_id)

    async def sample(self, filepath):
        self.data_frame = pd.read_csv(filepath)
        self.stats.update({"records": self.data_frame.shape[0]})

        # FIXME: Hack for Date fields, needs some mechanism for specifying types.
        self.data_frame["date_of_birth"] = pd.to_datetime(
            self.data_frame["date_of_birth"], errors="coerce", format="%d/%m/%Y"
        )
        fields = ["given_name", "surname", ["date_of_birth", "DateTime"], "sex"]
        # hack ends

        self.deduper = self.dedupe_prep(fields)
        self.dedupe_sample(self.deduper, self.data_frame)
        self.pairs_buffer = self.dedupe_pairs(self.deduper)

    async def pairs(self, labeled_pairs):
        self.updating = True
        self.dedupe_mark(self.deduper, labeled_pairs)
        self.pairs_buffer = self.dedupe_pairs(self.deduper)
        self.updating = False

    async def train(self, client_id):
        self.updating = True
        self.dedupe_train(self.deduper, client_id)
        self.training_complete = True
        self.updating = False

    async def dedupe(self):
        self.updating = True
        self.result, duplicates = self.dedupe_deduplicate(self.deduper, self.data_frame)
        self.stats.update({"duplicates": duplicates})
        self.dedupe_complete = True
        self.has_result = True
        self.updating = False

    async def get_pairs(self):
        while self.updating:
            await asyncio.sleep(1)
        return self.pairs_buffer

    async def get_status(self, item):
        status = {"training": self.training_complete, "dedupe": self.dedupe_complete}
        while self.updating:
            await asyncio.sleep(1)
        return status.get(item)


datastores = dict()


def get_datastore(client_id):
    if datastores.get(client_id):
        return datastores.get(client_id)
    else:
        datastores.update({client_id: DataStore([], {})})
        return datastores.get(client_id)


def delete_datastore(client_id):
    try:
        del datastores[client_id]
    except KeyError:
        logger.error(
            "Failed to remove datastore for client_id %s, datastore not found",
            client_id,
        )
