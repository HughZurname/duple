import asyncio
from duple import logger

from duple.deduplicate import Deduplicate

import pandas as pd
from dataclasses import dataclass


@dataclass
class DataStore(Deduplicate):
    pairs_buffer: list
    stats: dict
    training_rounds: int = 1
    updating: bool = False
    has_result: bool = False
    training_complete: bool = False
    dedupe_complete: bool = False

    def read_file(self, filepath):
        df = pd.read_csv(filepath)
        filtered = df.filter(regex="date")
        df[filtered.columns] = filtered.apply(
            lambda x: pd.to_datetime(x, errors="coerce", format="%d/%m/%Y")
        )
        fields = [
            [col, "DateTime"] if "date" in col else col for col in list(df.columns)
        ]
        return df, fields

    async def model(self, filepath, client_id):
        self.data_frame, _ = self.read_file(filepath)

        self.deduper = self.dedupe_static(client_id)
        self.stats.update({"records": self.data_frame.shape[0]})

    async def sample(self, filepath):
        self.data_frame, fields = self.read_file(filepath)

        self.deduper = self.dedupe_prep(fields)
        self.dedupe_sample(self.deduper, self.data_frame)
        self.pairs_buffer = self.dedupe_pairs(self.deduper)
        self.stats.update({"records": self.data_frame.shape[0]})

    async def pairs(self, labeled_pairs):
        self.updating = True
        self.dedupe_mark(self.deduper, labeled_pairs)
        self.pairs_buffer = self.dedupe_pairs(self.deduper)
        self.training_rounds += 1
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


datastore_repository = dict()


def get_datastore(client_id):
    if datastore_repository.get(client_id):
        return datastore_repository.get(client_id)
    else:
        datastore_repository.update({client_id: DataStore([], {})})
        return datastore_repository.get(client_id)


def delete_datastore(client_id):
    try:
        del datastore_repository[client_id]
    except KeyError:
        logger.error(
            "Failed to remove datastore for client_id %s, datastore not found",
            client_id,
        )
