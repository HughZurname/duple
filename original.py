import re
import unicodedata
import pandas as pd
import numpy as np
import logging
import os
import sys

from string_grouper import group_similar_strings
from fuzzy import DMetaphone

logging.basicConfig(
    level=logging.getLevelName(os.getenv("LOG_LEVEL") or "INFO"),
    format="[%(asctime)s] [%(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def read_data(file):
    profile_data = pd.read_csv(file)
    logger.info(f"File data loaded with {profile_data.shape[0]} records")
    return profile_data


def write_data(profile_data: pd.DataFrame, profile_duplicates: pd.DataFrame):
    logger.info(f"Writing cleaned data to: profile-data/cleaneddata.csv")
    profile_data.to_csv("profile-data/cleaneddata.csv", index=False)
    logger.info(f"Writing duplicate data to: profile-data/relateddata.csv")
    profile_duplicates.to_csv("profile-data/relateddata.csv", index=False)


def normalize(data):
    data = np.str_(data)
    data = unicodedata.normalize("NFKD", data).encode("ASCII", "ignore").decode("utf-8")
    data = re.sub(r"[^a-zA-Z]", "", data)
    return re.sub(r"NaN", "", data)


def clean(profile_data: pd.DataFrame):
    logger.info(f"Cleaning & Normalizing {profile_data.shape[0]} rows")
    profile_data["given_name"] = profile_data["given_name"].apply(normalize)
    profile_data["surname"] = profile_data["surname"].apply(normalize)
    return profile_data


def split_duplicates(profile_data: pd.DataFrame):
    profile_duplicates = profile_data[profile_data.duplicated()]
    profile_data = profile_data.drop_duplicates()
    logger.info(f"Removing {profile_duplicates.shape[0]} exact mach rows")
    return (profile_data, profile_duplicates)


def split_tf_idf(profile_data: pd.DataFrame):
    profile_data["match_code"] = profile_data.apply(
        lambda x: f'{x["given_name"]} {x["surname"]} {x["date_of_birth"]}', axis=1
    )
    profile_data["group"] = group_similar_strings(profile_data["match_code"])
    profile_duplicates = profile_data[
        profile_data["group"] != profile_data["match_code"]
    ]
    profile_data = profile_data.drop(index=profile_duplicates.index).drop(
        columns=["match_code", "group"]
    )
    profile_duplicates = profile_duplicates.drop(columns=["match_code", "group"])
    logger.info(f"Removing {profile_duplicates.shape[0]} close match rows")
    return profile_data, profile_duplicates


# def split_nysiis(profile_data: pd.DataFrame):
#     profile_data["nysiis"] = profile_data.apply(
#         lambda x: nysiis(f'{x["given_name"]} {x["surname"]}'), axis=1
#     )
#     profile_duplicates = profile_data.groupby("nysiis").agg(
#         {
#             "given_name": lambda x: x,
#             "surname": lambda x: x,
#             "date_of_birth": lambda x: x,
#             "sex": lambda x: x,
#         }
#     )
#     print(profile_duplicates)


def match_metaphone(value1, value2):
    doublemetaphone = DMetaphone(4)
    v1m = doublemetaphone.doublemetaphone(value1)
    v2m = doublemetaphone.doublemetaphone(value2)
    possibilities = [
        v1m[0] == v2m[0],
        v1m[0] == v2m[1],
        v1m[1] == v2m[0],
        v1m[1] == v2m[1] != "",
    ]
    return 1.0 if True in possibilities else 0.0


def second_pass(profile_data: pd.DataFrame, profile_duplicates: pd.DataFrame):
    profile_data, duplicates = split_duplicates(profile_data)
    profile_duplicates = profile_duplicates.append(duplicates)
    logger.info(f"Removed {profile_duplicates.shape[0]} duplicate rows")
    return profile_data, profile_duplicates


def first_pass(file="profile-data/DataShed_Technical_Test.csv"):
    return split_tf_idf(clean(read_data(file)))


write_data(*second_pass(*first_pass()))
