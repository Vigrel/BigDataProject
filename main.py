import glob
import os
import re

import pandas as pd

FOLDER_PATH = "/Users/vigrel/Git/BigDataProject/data/raw"


def get_csv_files(folder_path: str) -> list:
    return glob.glob(os.path.join(folder_path, "*.csv"))


def get_final_columns(folder_path: str) -> list[str]:
    all_columns = set()
    year_columns = set()

    for path in get_csv_files(folder_path):
        columns = pd.read_csv(path, index_col="ObjectId", nrows=0).columns
        all_columns.update(columns)

    normalized_columns = set(
        col.lower().strip().replace(" ", "").replace("_", "") for col in all_columns
    )

    for col in normalized_columns:
        if re.search(r"\d{4}$", col):
            year_columns.add(col)
        else:
            all_columns.add(col)

    return list(normalized_columns - year_columns), list(year_columns)


def normalize_columns(df, final_columns):
    df.columns = (
        df.columns.str.lower().str.strip().str.replace(" ", "").str.replace("_", "")
    )

    missing_cols = set(final_columns) - set(df.columns)
    for col in missing_cols:
        df[col] = pd.NA

    df = df[final_columns]

    return df


if __name__ == "__main__":
    general_columns, year_columns = get_final_columns(FOLDER_PATH)
    general_columns.extend(year_columns)
    df_list = []

    for path in get_csv_files(FOLDER_PATH):
        df = pd.read_csv(path, index_col="ObjectId")
        df = normalize_columns(df, general_columns)
        df_melted = df.melt(
            id_vars=[col for col in general_columns if col not in year_columns],
            value_vars=year_columns,
            var_name="year",
            value_name="feature_value",
        )

        df_melted["datasource"] = path
        df_list.append(df_melted)

    data_processed = pd.concat(df_list, ignore_index=True)
    data_processed.to_csv("data/processed/dataConcat.csv", index=False)
