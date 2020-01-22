from duple import logger
import asyncio
from duple.message import MessageType
from duple.datastore import get_datastore


async def producer(queue, message):
    """Process messagees and schedule worker work items.

    [description]
    """
    logger.info(
        "Scheduling %s work item for client %s message (%s)",
        message.message_type.name,
        message.client_id,
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
        datastore = get_datastore(message.client_id)
        logger.info(
            "Processing %s work item for client %s message (%s)",
            message.message_type.name,
            message.client_id,
            message.message_id,
        )
        if message.message_type == MessageType.SAMPLE:
            await datastore.sample(message.data.get("filepath"))
            queue.task_done()
        if message.message_type == MessageType.LABEL:
            await datastore.pairs(message.data.get("labeled_pairs"))
            queue.task_done()
        if message.message_type == MessageType.TRAIN:
            await datastore.train(message.client_id)
            queue.task_done()
        if message.message_type == MessageType.DEDUPE:
            await datastore.dedupe()
            queue.task_done()
