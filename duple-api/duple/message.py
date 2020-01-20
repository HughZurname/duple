from enum import Enum

import attr
import uuid

class MessageType(Enum):
    """Job status enum for test job execution.

    Extends:
        Enum

    Variables:
        CANCEL {number} -- Cancelled Message. All work stops immediately
        NEW {number} -- Initial Message state.
        SAMPLE {number} -- Sampling Message. Sampling input data for training.
        TRAIN {number} -- Training Message. Acvtive training phase.
        DEDUPE {number} -- Deduplication Message. Deduplicating data with trained model.
        DONE {number} -- Message is complete.
    """

    CANCEL = 1
    NEW = 2
    SAMPLE = 3
    TRAIN = 4
    DEDUPE = 5
    DONE = 6


@attr.s
class Message:
    message_id = attr.ib(repr=False)
    state = attr.ib(validator=attr.validators.in_(MessageType))
    data = attr.ib()


def messaage_wrapper(data, message_state=None):
    return Message(uuid.uuid4(), message_state or MessageType.NEW, data)
