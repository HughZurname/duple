import asyncio
import pytest

from duple.message import message_wrapper, MessageType
import duple.worker as worker

pytestmark = pytest.mark.asyncio


@pytest.fixture
def model_message():
    return message_wrapper("123abc", {"use_model": True})


@pytest.fixture
def sample_message():
    return message_wrapper("123abc", {"filepath": "some/file/path.csv"})


@pytest.fixture
def label_message():
    return message_wrapper(
        "123abc", {"labeled_pairs": {"match": [{}], "distinct": [{}]}}
    )


@pytest.fixture
def train_message():
    return message_wrapper("123abc", {"labeling_complete": True})


@pytest.fixture
def dedupe_message():
    return message_wrapper("123abc", {"training_complete": True})


async def test_producer_model(model_message, event_loop):
    await worker.producer(asyncio.Queue(), model_message)
    assert model_message.message_type == MessageType.MODEL


async def test_producer_sample(sample_message, event_loop):
    await worker.producer(asyncio.Queue(), sample_message)
    assert sample_message.message_type == MessageType.SAMPLE


async def test_producer_label(label_message, event_loop):
    await worker.producer(asyncio.Queue(), label_message)
    assert label_message.message_type == MessageType.LABEL


async def test_producer_train(train_message, event_loop):
    await worker.producer(asyncio.Queue(), train_message)
    assert train_message.message_type == MessageType.TRAIN


async def test_producer_dedupe(dedupe_message, event_loop):
    await worker.producer(asyncio.Queue(), dedupe_message)
    assert dedupe_message.message_type == MessageType.DEDUPE
