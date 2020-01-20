from duple import logger
from duple.message import MessageType
from duple.deduplicate import (
    dedupe_prep,
    dedupe_sample,
    dedupe_pairs,
    dedupe_mark,
    dedupe_train,
    dedupe_deduplicate,
)

import asyncio
import pandas as pd
from dataclasses import dataclass


@dataclass
class DataStore:
    pairs_buffer: list
    stats: dict
    updating: bool = False
    has_result: bool = False
    training_complete: bool = False
    dedupe_complete: bool = False

    async def sample(self, filepath):
        self.data_frame = pd.read_csv(filepath)
        self.stats.update({"records": self.data_frame.shape[1]})

        # FIXME: Hack for Date fields, needs some mechanism for specifying types.
        self.data_frame["date_of_birth"] = pd.to_datetime(
            self.data_frame["date_of_birth"], errors="coerce", format="%d/%m/%Y"
        )
        fields = ["given_name", "surname", ["date_of_birth", "DateTime"], "sex"]
        # hack ends

        self.deduper = dedupe_prep(fields)
        dedupe_sample(self.deduper, self.data_frame)
        self.pairs_buffer = dedupe_pairs(self.deduper)

    async def pairs(self, labeled_pairs):
        self.updating = True
        dedupe_mark(self.deduper, labeled_pairs)
        self.pairs_buffer = dedupe_pairs(self.deduper)
        self.updating = False

    async def train(self):
        self.updating = True
        logger.warning("TODO: Add client id to messages")
        dedupe_train(self.deduper)
        self.training_complete = True
        self.updating = False

    async def dedupe(self):
        self.updating = True
        logger.warning("TODO: Use original df here?")
        self.result, duplicates = dedupe_deduplicate(self.deduper, self.data_frame)
        self.stats.update({"duplicates": duplicates})
        self.dedupe_complete = True
        self.has_result = True
        self.updating = False

    async def get_pairs(self):
        while self.updating:
            asyncio.sleep(1)
        return self.pairs_buffer

    async def get_status(self, item):
        status = {"training": self.training_complete, "dedupe": self.dedupe_complete}
        while self.updating:
            asyncio.sleep(1)
        return status.get(item)


datastore = DataStore([], {})


async def producer(queue, message):
    """Process messagees and schedule worker work items.

    [description]
    """
    logger.info(
        "Scheduling work item for %s message (%s)",
        message.message_type.name,
        message.message_id,
    )
    if message.message_type == MessageType.NEW and message.data:
        if message.data.get("filepath"):
            message.message_type = MessageType.SAMPLE
            asyncio.create_task(queue.put(message))
        elif message.data.get("labeled_pairs"):
            message.message_type = MessageType.LABEL
            asyncio.create_task(queue.put(message))
        elif message.data.get("labeling_complete"):
            message.message_type = MessageType.TRAIN
            asyncio.create_task(queue.put(message))
        elif message.data.get("training_complete"):
            message.message_type = MessageType.DEDUPE
            asyncio.create_task(queue.put(message))
        else:
            logger.error(
                "Unable to schedule message (%s). Unknown message data %s",
                message.message_id,
                message.data,
            )
    else:
        logger.error("Unable to schedule message %s", message)


async def consumer(queue):
    """Consume scheduled work items.

    [description]
    """
    while True:
        message = await queue.get()
        logger.info(
            "Processing work item for %s message (%s)",
            message.message_type.name,
            message.message_id,
        )
        if message.message_type == MessageType.SAMPLE:
            await datastore.sample(message.data.get("filepath"))
            queue.task_done()
        if message.message_type == MessageType.LABEL:
            await datastore.pairs(message.data.get("labeled_pairs"))
            queue.task_done()
        if message.message_type == MessageType.TRAIN:
            await datastore.train()
            queue.task_done()
        if message.message_type == MessageType.DEDUPE:
            await datastore.dedupe()
            queue.task_done()
