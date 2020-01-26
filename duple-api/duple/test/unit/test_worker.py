import pytest

from duple.message import message_wrapper, MessageType
import duple.worker as worker
# import duple.datastore as datastore


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
def mock_queue(mocker, monkeypatch):
    mock_queue = mocker.Mock()
    monkeypatch.setattr(worker.asyncio, "Queue", mock_queue)
    return mock_queue.return_value


@pytest.fixture
def queue_get(mock_queue, mock_coro):
    mock_get, coro_get = mock_coro()
    mock_queue.get = coro_get
    return mock_get


@pytest.fixture
def queue_put(mock_queue, mock_coro):
    mock_put, coro_put = mock_coro()
    mock_queue.put = coro_put
    return mock_put


# @pytest.fixture
# def mock_datastore(mocker, monkeypatch):
#     mock_datastore = mocker.Mock()
#     mock_deduper = mocker.PropertyMock()
#     monkeypatch.setattr(datastore, "DataStore", mock_datastore)
#     monkeypatch.setattr(datastore.DataStore, "deduper", mock_deduper)
#     return mock_datastore.return_value


# @pytest.fixture
# def datastore_model(mock_datastore, mock_coro):
#     mock_model, coro_model = mock_coro()
#     datastore.model = coro_model
#     return mock_model


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


async def test_producer_model(model_message, event_loop, mock_queue, queue_put):
    await worker.producer(mock_queue, model_message)
    assert model_message.message_type == MessageType.MODEL


# async def test_consumer_model(
#     model_message,
#     event_loop,
#     mock_queue,
#     mock_coro,
#     queue_put,
#     queue_get,
# ):
#     await worker.producer(mock_queue, model_message)
#     assert model_message.message_type == MessageType.MODEL

#     queue_get.side_effect = [model_message, Exception()]
#     datastore_model = mock_coro("duple.datastore.DataStore.model")

#     with pytest.raises(Exception):
#         await worker.consumer(mock_queue)

#     ret_tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

#     assert 1 == len(ret_tasks)
#     datastore_model.assert_not_called()

#     await asyncio.gather(*ret_tasks)

#     datastore_model.assert_called_once_with(model_message)


async def test_producer_sample(sample_message, event_loop, mock_queue, queue_put):
    await worker.producer(mock_queue, sample_message)
    assert sample_message.message_type == MessageType.SAMPLE


async def test_producer_label(label_message, event_loop, mock_queue, queue_put):
    await worker.producer(mock_queue, label_message)
    assert label_message.message_type == MessageType.LABEL


async def test_producer_train(train_message, event_loop, mock_queue, queue_put):
    await worker.producer(mock_queue, train_message)
    assert train_message.message_type == MessageType.TRAIN


async def test_producer_dedupe(dedupe_message, event_loop, mock_queue, queue_put):
    await worker.producer(mock_queue, dedupe_message)
    assert dedupe_message.message_type == MessageType.DEDUPE
