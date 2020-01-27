import pytest


from duple.datastore import DataStore, get_datastore, delete_datastore, datastore_repository


@pytest.fixture
def new_datastore():
    return DataStore([], {})


@pytest.fixture
def existing_datastore():
    return DataStore([], {"records": 10000}, 2, True, True, True, True)


@pytest.fixture
def modify_repository(existing_datastore):
    datastore_repository.update({"test234": existing_datastore})


def test_get_new_datastore(new_datastore):
    assert get_datastore("test123") == new_datastore


def test_get_existing_datastore(modify_repository, existing_datastore, new_datastore):
    assert get_datastore("test234") != new_datastore
    assert get_datastore("test234") == existing_datastore
    assert get_datastore("test567") != get_datastore("test234")


def test_delete_empty_datastores(modify_repository, existing_datastore, new_datastore):
    delete_datastore("test234")
    assert get_datastore("test234") == new_datastore
