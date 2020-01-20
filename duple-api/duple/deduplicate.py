from duple import logger
from duple.utility import clean_df, select_fields

import pandas as pd

import math
import os
import dedupe


def data_prep(df):
    logger.debug("Preparing data and dictionary for deduplication")
    df = clean_df(df)
    df["dictionary"] = df.to_dict("records")
    data_d = dict(zip(df.index, df.dictionary))

    return df, data_d


def data_cluster(deduper, data_dict, threshold):
    logger.debug("Clustering data")
    duplicates = deduper.match(data_dict, threshold)
    logger.debug("Duplicate records found: %d", len(duplicates))

    df_data = [
        {"id": record_id, "cluster_id": cluster_id, "confidence": score}
        for cluster_id, records in enumerate(duplicates)
        for record_id, score in zip(*records)
    ]

    clustered_df = pd.DataFrame(df_data)
    clustered_df = clustered_df.set_index("id")

    return clustered_df


def dedupe_prep(fields):
    logger.debug("Preparing deduper training phase")
    fields = select_fields(fields)
    return dedupe.Dedupe(fields)


def dedupe_pairs(deduper, pairs=10):
    logger.debug("Retrieving pairs for active labeling")

    return [
        {"pair_id": i, "records": {"record": m1, "match": m2}}
        for i in range(pairs)
        for m1, m2 in deduper.uncertainPairs()
    ]


def dedupe_mark(deduper, labelled_pairs):
    logger.debug("Marking labelled training pairs")
    deduper.markPairs(labelled_pairs)


def dedupe_sample(deduper, df, sample_size=0.3):
    df, data_dict = data_prep(df)

    logger.debug("Getting candidate training matches")
    sample_num = math.floor(len(data_dict) * sample_size)

    logger.debug("Taking data sample of %s records", sample_num)
    deduper.sample(data_dict, sample_num)


def dedupe_train(deduper, client_id="test1234"):
    logger.debug("Finalising deduper training")
    deduper.train()

    logger.debug("Writing training files to disk")
    training_file = os.path.join("training-data", client_id, "dedupe_training.json")
    os.makedirs(os.path.dirname(training_file), exist_ok=True)
    settings_file = os.path.join("training-data", client_id, "dedupe_learned_settings")
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)

    with open(training_file, "w") as tf:
        deduper.writeTraining(tf)
    with open(settings_file, "wb") as sf:
        deduper.writeSettings(sf)


def dedupe_deduplicate(deduper, df, recall_weight=1):
    df, data_d = data_prep(df)
    threshold = deduper.threshold(data_d, recall_weight=recall_weight)
    clustered_df = data_cluster(deduper, data_d, threshold)
    results = df.join(clustered_df, how="left")
    results.drop(["dictionary"], axis=1, inplace=True)

    return results
