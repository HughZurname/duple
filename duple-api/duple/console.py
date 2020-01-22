from duple import logger
from duple.data_utils import clean_df, select_fields

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
    logger.info("Duplicate records found: %d", len(duplicates))

    df_data = [
        {"id": record_id, "cluster_id": cluster_id, "confidence": score}
        for cluster_id, records in enumerate(duplicates)
        for record_id, score in zip(*records)
    ]

    clustered_df = pd.DataFrame(df_data)
    clustered_df = clustered_df.set_index("id")

    return clustered_df


def deduplicate(
    df,
    recall_weight=1,
    sample_size=0.3,
    settings_file="training-data/dedupe_learned_settings",
    training_file="training-data/dedupe_training.json",
):
    fields = df.columns
    df, data_d = data_prep(df)

    if os.path.exists(settings_file):
        logger.info("Existing settings found. Loading from: %s", settings_file)
        with open(settings_file, "rb") as f:
            deduper = dedupe.StaticDedupe(f)
    else:
        fields = select_fields(fields)
        deduper = dedupe.Dedupe(fields)
        sample_num = math.floor(len(data_d) * sample_size)

        logger.info("Extracting data sample of %s records", sample_num)
        deduper.sample(data_d, sample_num)

        if os.path.exists(training_file):
            logger.info("Reading training examples from: %s", training_file)
            with open(training_file, "rb") as f:
                deduper.readTraining(f)

        logger.info("Starting active labeling")

        dedupe.consoleLabel(deduper)

        deduper.train()

        with open(training_file, "w") as tf:
            deduper.writeTraining(tf)
        with open(settings_file, "wb") as sf:
            deduper.writeSettings(sf)

    threshold = deduper.threshold(data_d, recall_weight=recall_weight)

    clustered_df = data_cluster(deduper, data_d, threshold)
    results = df.join(clustered_df, how="left")
    results.drop(["dictionary"], axis=1, inplace=True)

    return results


def console_deduplicate(filename):
    logger.info("Starting console deduplicator")
    df = pd.read_csv(filename)
    result = deduplicate(df)
    logger.info("Writing results file to relateddata.csv")
    result.to_csv("relateddata.csv", index=False)
