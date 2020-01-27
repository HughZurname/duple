from duple import logger
from duple.datautils import select_fields, data_prep, data_cluster

import pandas as pd
import math
import os
import dedupe


class Deduplicate:
    """Base dedupliction class.

    Provides deduplication functionality using python-dedupe.
    """

    def dedupe_static(self, client_id):
        """Dedupe for existing data.

        Loads an existing deduper with StaticDedupe. Prioritises model trained
        by client and falls back to default model.

        Arguments:
            client_id -- Unique client identifier.

        Returns:
            StaticDedupe -- Pre-trained deduper.

        """
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
        """Prepare a Dedupe instance.

        Prepares a dedupe instance based on input data fields

        Arguments:
            fields {list} -- List of fields representing the input data columns.

        Returns:
            Dedupe -- New Deduper for further training

        """
        logger.debug("Preparing deduper training phase %s", fields)
        fields = select_fields(fields)
        return dedupe.Dedupe(fields)

    def dedupe_pairs(self, deduper, pairs=6):
        """Training pairs for labelling.

        Selects a number of pairs for active labelling in the training phase.

        Arguments:
            deduper {Dedupe} -- Dedupe instance prepared with fields.

        Keyword Arguments:
            pairs {number} -- Number of labeling pairs to return (default: {6})

        Returns:
            list -- List of pairs to be matched.

        """
        logger.debug("Retrieving pairs for active labeling")

        try:
            training_pairs = [
                {"pair_id": i, "records": {"record": m1, "match": m2}}
                for i in range(pairs)
                for m1, m2 in deduper.uncertainPairs()
            ]
            return training_pairs
        except IndexError as e:
            logger.error(
                "Unable to retrieve training pairs with the following error: %s", e
            )
            return []

    def dedupe_mark(self, deduper, labelled_pairs):
        """Mark labeled pairs.

        Marks labelled pairs with the Dedupe instance for reinforcement training.

        Arguments:
            deduper {Deduper} -- Dudeper instance
            labelled_pairs {list} -- List of pairs labeleld as distinct or a match

        """
        logger.debug("Marking labelled training pairs")
        deduper.markPairs(labelled_pairs)

    def dedupe_sample(self, deduper, df, sample_size=0.3):
        """Sample supplied DataFrame for training.

        Selects a representative sample from the input DataFrame to be used in
        the training phase.

        Arguments:
            deduper {[type]} -- [description]
            df {DataFrame} -- [description]

        Keyword Arguments:
            sample_size {number} -- [description] (default: {0.3})
        """
        df, data_dict = data_prep(df)

        logger.debug("Getting candidate training matches")
        if len(data_dict) < 500:
            sample_num = len(data_dict)
        elif len(data_dict) > 5000:
            sample_num = math.floor(len(data_dict) * sample_size)
        else:
            logger.debug("Dataset too small, decreasing sample size")
            sample_num = math.floor(len(data_dict) * 0.2)

        logger.debug("Requsting data sample of %s records", sample_num)
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
        logger.debug("Preparing deduper results")
        df, data_d = data_prep(df)
        try:
            threshold = deduper.threshold(data_d, recall_weight=recall_weight)
            clustered_df, duplicates = data_cluster(deduper, data_d, threshold)
            results = df.join(clustered_df, how="left")
            results.drop(["dictionary"], axis=1, inplace=True)

            return results, duplicates
        except Exception as e:
            logger.error("Unable to deduplicate data with the following error: %s", e)
            return pd.DataFrame(), 0
