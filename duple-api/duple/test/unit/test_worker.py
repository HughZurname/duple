import asyncio
import pytest

from duple.message import message_wrapper, MessageType
import duple.worker as worker

# pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_coro(mocker, monkeypatch):
    def _create_mock_coro(to_patch=None):
        mock = mocker.Mock()

        async def _coro(*args, **kwargs):
            return mock(*args, **kwargs)

        if to_patch:
            monkeypatch.setattr(to_patch, _coro)
        return mock, _coro

    return _create_mock_coro


@pytest.fixture
def queue(mocker, monkeypatch):
    queue = mocker.Mock()
    monkeypatch.setattr(worker.asyncio, "Queue", queue)
    return queue.return_value


@pytest.fixture
def queue_get(queue, mock_coro):
    mock_get, coro_get = mock_coro()
    queue.get = coro_get
    return mock_get


@pytest.fixture
def queue_put(queue, mock_coro):
    mock_put, coro_put = mock_coro()
    queue.put = coro_put
    return mock_put


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


async def test_producer_model(model_message, event_loop, queue, queue_put):
    await worker.producer(queue, model_message)
    assert model_message.message_type == MessageType.MODEL


async def test_producer_sample(sample_message, event_loop, queue, queue_put):
    await worker.producer(queue, sample_message)
    assert sample_message.message_type == MessageType.SAMPLE


async def test_producer_label(label_message, event_loop, queue, queue_put):
    await worker.producer(queue, label_message)
    assert label_message.message_type == MessageType.LABEL


async def test_producer_train(train_message, event_loop, queue, queue_put):
    await worker.producer(queue, train_message)
    assert train_message.message_type == MessageType.TRAIN


async def test_producer_dedupe(dedupe_message, event_loop, queue, queue_put):
    await worker.producer(queue, dedupe_message)
    assert dedupe_message.message_type == MessageType.DEDUPE
