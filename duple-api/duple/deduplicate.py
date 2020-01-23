from duple import logger
from duple.datautils import select_fields, data_prep, data_cluster

import math
import os
import dedupe


class Deduplicate:
    def dedupe_static(self, client_id):
        default_settings = os.path.join("training-data", "dedupe_learned_settings")
        client_settings = os.path.join(
            "training-data", client_id, "dedupe_learned_settings"
        )
        if os.path.exists(client_settings):
            with open(client_settings, "rb") as cs:
                deduper = dedupe.StaticDedupe(cs)
        else:
            with open(default_settings, "rb") as ds:
                deduper = dedupe.StaticDedupe(ds)

        return deduper

    def dedupe_prep(self, fields):
        logger.debug("Preparing deduper training phase %s", fields)
        fields = select_fields(fields)
        return dedupe.Dedupe(fields)

    def dedupe_pairs(self, deduper, pairs=6):
        logger.debug("Retrieving pairs for active labeling")

        return [
            {"pair_id": i, "records": {"record": m1, "match": m2}}
            for i in range(pairs)
            for m1, m2 in deduper.uncertainPairs()
        ]

    def dedupe_mark(self, deduper, labelled_pairs):
        logger.debug("Marking labelled training pairs")
        deduper.markPairs(labelled_pairs)

    def dedupe_sample(self, deduper, df, sample_size=0.3):
        df, data_dict = data_prep(df)

        logger.debug("Getting candidate training matches")
        if len(data_dict) > 5000:
            sample_num = math.floor(len(data_dict) * sample_size)
        else:
            logger.debug("Dataset too small, decreasing sample size")
            sample_num = math.floor(len(data_dict) * 0.2)

        logger.debug("Taking data sample of %s records", sample_num)
        deduper.sample(data_dict, sample_num)

    def dedupe_train(self, deduper, client_id):
        logger.debug("Finalising deduper training")
        deduper.train()

        logger.debug("Writing training files to disk")
        training_file = os.path.join("training-data", client_id, "dedupe_training.json")
        os.makedirs(os.path.dirname(training_file), exist_ok=True)
        settings_file = os.path.join(
            "training-data", client_id, "dedupe_learned_settings"
        )
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)

        with open(training_file, "w") as tf:
            deduper.writeTraining(tf)
        with open(settings_file, "wb") as sf:
            deduper.writeSettings(sf)

    def dedupe_deduplicate(self, deduper, df, recall_weight=1):
        df, data_d = data_prep(df)
        threshold = deduper.threshold(data_d, recall_weight=recall_weight)
        clustered_df, duplicates = data_cluster(deduper, data_d, threshold)
        results = df.join(clustered_df, how="left")
        results.drop(["dictionary"], axis=1, inplace=True)

        return results, duplicates
