import glob
import os
import re

import dask.dataframe as dd

FOLDER_PATH = "/Users/vigrel/Git/BigDataProject/data/raw"
OUTPUT_INTERIM = "data/interim/dataConcat_silver.csv"
OUTPUT_PROCESSED = "data/processed/dataConcat_gold.csv"

dtypes = {"ISO2": "object", "ObjectId": "int64"}


def get_csv_files(folder_path: str) -> list:
    return glob.glob(os.path.join(folder_path, "*.csv"))


def get_final_columns(folder_path: str):
    all_columns = set()

    for path in get_csv_files(folder_path)[:1]:
        columns = dd.read_csv(path, dtype=dtypes, assume_missing=True).columns
        all_columns.update(columns)

    normalized_columns = {
        col.lower().strip().replace(" ", "").replace("_", "") for col in all_columns
    }
    year_columns = {col for col in normalized_columns if re.search(r"\d{4}$", col)}
    return list(normalized_columns - year_columns), list(year_columns)


def normalize_columns(df, final_columns):
    df = df.rename(
        columns=lambda col: col.lower().strip().replace(" ", "").replace("_", "")
    )
    for col in final_columns:
        if col not in df.columns:
            df[col] = None
    return df[final_columns]


def groupby_country(interim_df):
    interim_df["year"] = interim_df["year"].str.replace("f", "")
    interim_df["indicator_unit"] = (
        interim_df["indicator"].str.replace(" ", "")
        + "_"
        + interim_df["unit"].str.replace(" ", "")
    )

    index_cols = ["country", "iso2", "iso3", "year"]

    df_processed = interim_df.compute()
    return df_processed.pivot_table(
        index=index_cols,
        columns="indicator_unit",
        values="feature_value",
        aggfunc="first",
    ).reset_index()


def main():
    general_columns, year_columns = get_final_columns(FOLDER_PATH)
    final_columns = general_columns + year_columns
    df_list = []

    for path in get_csv_files(FOLDER_PATH):
        df = dd.read_csv(path, dtype=dtypes, assume_missing=True).set_index("ObjectId")
        df = df.map_partitions(normalize_columns, final_columns=final_columns)
        df_melted = df.melt(
            id_vars=[col for col in general_columns],
            value_vars=year_columns,
            var_name="year",
            value_name="feature_value",
        )
        df_melted["datasource"] = os.path.basename(path)
        df_list.append(df_melted)

    data_interim = dd.concat(df_list)

    data_processed = groupby_country(data_interim)

    data_interim.to_csv(OUTPUT_INTERIM, index=False, single_file=True)
    data_processed.to_csv(OUTPUT_PROCESSED, index=False)


if __name__ == "__main__":
    main()