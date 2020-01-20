from duple import logger
from duple.message import MessageType
from duple.deduplicate import training_pairs, data_prep, deduper_prep, deduper_sample

import asyncio
import pandas as pd
from dataclasses import dataclass


@dataclass
class DataStore:
    training_buffer: list
    training_attempts: int

    async def sample(self, filepath):
        self.data_frame = pd.read_csv(filepath)

        # FIXME: Hack for Date fields, needs some mechanism for specifying types.
        self.data_frame["date_of_birth"] = pd.to_datetime(
            self.data_frame["date_of_birth"], errors="coerce", format="%d/%m/%Y"
        )
        fields = ["given_name", "surname", ["date_of_birth", "DateTime"], "sex"]
        # fields = self.data_frame.columns
        # hack ends

        self.data_frame, data_dict = data_prep(self.data_frame)
        self.deduper = deduper_prep(fields)
        deduper_sample(self.deduper, data_dict)
        self.training_buffer = training_pairs(self.deduper)

    async def pairs(self, labelled_pairs):
        self.deduper.markPairs(labelled_pairs)
        self.training_buffer = training_pairs(self.deduper)
        self.training_attempts += 1


datastore = DataStore([], 0)


async def producer(queue, message):
    """[summary].

    [description]
    """
    logger.debug(
        "Producing job for message (%s) with state (%s)",
        message.message_id,
        message.state.name,
    )
    if message.state == MessageType.NEW and message.data["filepath"]:
        message.state = MessageType.SAMPLE
        asyncio.create_task(queue.put(message))


async def consumer(queue):
    """[summary].

    [description]
    """
    while True:
        message = await queue.get()
        logger.debug(
            "Consuming job for message (%s) with state (%s)",
            message.message_id,
            message.state.name,
        )
        if message.state == MessageType.CANCEL:
            break
        if message.state == MessageType.SAMPLE:
            await datastore.sample(message.data["filepath"])
            queue.task_done()
