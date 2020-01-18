from deduplicator import logger
from deduplicator.utility import clean_df, select_fields

import pandas as pd

import math
import os
import dedupe


def train_console(settings_file, training_file, data, fields, sample_size):
    logger.info("Starting training phase...")

    if os.path.exists(settings_file):
        logger.info("Existing settings found. Loading from: %s", settings_file)
        with open(settings_file, "rb") as f:
            deduper = dedupe.StaticDedupe(f)
    else:
        fields = select_fields(fields)
        deduper = dedupe.Dedupe(fields)
        sample_num = math.floor(len(data) * sample_size)

        logger.info("Extracting data sample of %s records...", sample_num)
        deduper.sample(data, sample_num)

        if os.path.exists(training_file):
            logger.info("Reading training examples from: %s", training_file)
            with open(training_file, "rb") as f:
                deduper.readTraining(f)

        logger.info("Starting active labeling...")

        dedupe.consoleLabel(deduper)

        deduper.train()

        with open(training_file, "w") as tf:
            deduper.writeTraining(tf)
        with open(settings_file, "wb") as sf:
            deduper.writeSettings(sf)

    return deduper


def deduper_prep(fields):
    logger.info("Preparing deduper training phase...")
    fields = select_fields(fields)
    return dedupe.Dedupe(fields)


def deduper_sample(deduper, data_dict, sample_size):
    logger.info("Getting candidate training matches...")
    sample_num = math.floor(len(data_dict) * sample_size)

    logger.info("Extracting data sample of %s records...", sample_num)
    deduper.sample(data_dict, sample_num)


def training_pairs(deduper, pairs=10):
    logger.info("Retrieving pairs for client labeling...")

    return [
        {"pair_id": i, "records": {"record": m1, "match": m2}}
        for i in range(pairs)
        for m1, m2 in deduper.uncertainPairs()
    ]


def cluster(deduper, data, threshold):
    logger.info("Clustering data...")
    duplicates = deduper.match(data, threshold)
    logger.info("Duplicate records found: %d", len(duplicates))

    df_data = [
        {"id": record_id, "cluster_id": cluster_id, "confidence": score}
        for cluster_id, records in enumerate(duplicates)
        for record_id, score in zip(*records)
    ]

    clustered_df = pd.DataFrame(df_data)
    clustered_df = clustered_df.set_index("id")

    return clustered_df


def data_prep(df):
    logger.debug("Preparing data and dictionary for deduplication...")
    df = clean_df(df)
    df["dictionary"] = df.to_dict("records")
    data_d = dict(zip(df.index, df.dictionary))

    return df, data_d


def deduplicate(
    df,
    field_properties,
    recall_weight=1,
    sample_size=0.3,
    settings_file="training-data/dedupe_learned_settings",
    training_file="training-data/dedupe_training.json",
):

    df, data_d = data_prep(df)

    deduper = train_console(
        settings_file, training_file, data_d, field_properties, sample_size
    )
    threshold = deduper.threshold(data_d, recall_weight=recall_weight)

    clustered_df = cluster(deduper, data_d, threshold)
    results = df.join(clustered_df, how="left")
    results.drop(["dictionary"], axis=1, inplace=True)

    return results
