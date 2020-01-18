from deduplicator import logger

from unidecode import unidecode


def select_fields(fields):
    logger.info("Generating data field mappings...")

    def gen_field(field):
        if type(field) == str:
            return {"field": field, "type": "String"}
        if len(field) == 2:
            return {"field": field[0], "type": field[1]}

    return [gen_field(field) for field in fields]


def clean_df(df):
    logger.info("Cleaning dataframe...")
    df = df.astype(str)
    df = df.applymap(lambda x: x.replace(r"[^a-zA-Z0-9/-]", ""))
    df = df.applymap(lambda x: unidecode(x))
    df = df.applymap(lambda x: x.lower())
    df = df.replace({"nan": "", "none": "", "nat": ""})
    return df
