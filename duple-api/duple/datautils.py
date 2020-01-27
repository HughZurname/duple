from duple import logger

from unidecode import unidecode

import pandas as pd


def data_prep(df):
    logger.debug("Preparing data and dictionary for deduplication")
    df = clean_df(df)
    df["dictionary"] = df.to_dict("records")
    data_d = dict(zip(df.index, df.dictionary))

    return df, data_d


def data_cluster(deduper, data_dict, threshold):
    logger.debug("Clustering data")
    duplicates = deduper.match(data_dict, threshold)
    logger.info("Testing deduper duplicates: %s", duplicates)
    logger.debug("Duplicate records found: %d", len(duplicates))

    df_data = [
        {"id": record_id, "cluster_id": cluster_id, "confidence": score}
        for cluster_id, records in enumerate(duplicates)
        for record_id, score in zip(*records)
    ]

    clustered_df = pd.DataFrame(df_data)
    clustered_df = clustered_df.set_index("id")

    return clustered_df, len(duplicates)


def select_fields(fields):
    logger.info("Generating data field mappings")

    def gen_field(field):
        if type(field) == str:
            return {"field": field, "type": "String"}
        if len(field) == 2:
            return {"field": field[0], "type": field[1]}

    return [gen_field(field) for field in fields]


def clean_df(df):
    logger.info("Cleaning dataframe")
    df = df.astype(str)
    df = df.applymap(lambda x: unidecode(x))
    df = df.applymap(lambda x: x.lower())
    df = df.replace({"nan": "", "none": "", "nat": ""})
    for i in df.columns:
        df[i] = df[i].str.replace(r"[^a-zA-Z0-9\/-]", "")
    return df
