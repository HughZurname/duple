from enum import Enum

import attr
import uuid


class MessageType(Enum):
    """Job status enum for test job execution.

    Extends:
        Enum

    Variables:
        NEW {number} -- Initial Message type.
        SAMPLE {number} -- Sampling Message. Sampling input data for training.
        LABEL {number} -- Labeling Message. Acvtive training phase.
        TRAIN {number} -- Training Message. Complete training phase.
        DEDUPE {number} -- Deduplication Message. Deduplicating data with trained model.
    """

    NEW = 1
    MODEL = 2
    SAMPLE = 3
    LABEL = 4
    TRAIN = 5
    DEDUPE = 6


@attr.s
class Message:
    client_id = attr.ib()
    message_id = attr.ib(repr=False)
    message_type = attr.ib(validator=attr.validators.in_(MessageType))
    data = attr.ib()


def message_wrapper(client_id, data, message_state=None):
    return Message(client_id, uuid.uuid4(), message_state or MessageType.NEW, data)
