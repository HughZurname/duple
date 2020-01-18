from deduplicator.deduplicate import deduplicate, training_pairs, data_prep
from deduplicator.service import run
import pandas as pd
import json

# df = pd.read_csv("profile-data/DataShed_Technical_Test.csv")
# fields = ["given_name", "surname", ["date_of_birth", "DateTime"], "sex"]

# df["date_of_birth"] = pd.to_datetime(
#     df["date_of_birth"], errors="coerce", format="%d/%m/%Y"
# )

# # df2 = deduplicate(df, fields, 0.75, 0.2, 'dong_settings', 'dong_training.json')

# # df2[df2["cluster_id"] > 0].sort_values("cluster_id").to_csv("ml.csv")

# df, data_d = data_prep(df)
# print(json.dumps(training_pairs(data_d, fields, 0.2)))

run()
