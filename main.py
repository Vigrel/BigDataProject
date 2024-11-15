import glob
import os
import re

import dask.dataframe as dd

FOLDER_PATH = "/Users/vigrel/Git/BigDataProject/data/raw"

dtypes = {"ISO2": "object", "ObjectId": "int64"}


def get_csv_files(folder_path: str) -> list:
    return glob.glob(os.path.join(folder_path, "*.csv"))


def get_final_columns(folder_path: str) -> list[str]:
    all_columns = set()
    year_columns = set()

    for path in get_csv_files(folder_path)[:1]:
        columns = dd.read_csv(path, dtype=dtypes, assume_missing=True).columns
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
        df[col] = None

    df = df[final_columns]
    return df


def groupby_country(iterim_df):
    iterim_df['year'] = iterim_df['year'].str.replace("f", "")
    iterim_df['indicator_unit'] = iterim_df['indicator'].str.replace(" ", "") + "_" + iterim_df['unit'].str.replace(" ", "")

    index_cols = ["country", "iso2", "iso3", "year"]

    df_processed = iterim_df[["country", "iso2", "iso3", "year", "indicator_unit", "feature_value"]].compute()
    return df_processed.pivot_table(
        index=index_cols,
        columns="indicator_unit",
        values="feature_value",
        aggfunc="first"
    ).reset_index()


def main():
    general_columns, year_columns = get_final_columns(FOLDER_PATH)
    general_columns.extend(year_columns)
    df_list = []

    for path in get_csv_files(FOLDER_PATH):
        df = dd.read_csv(path, dtype=dtypes, assume_missing=True)
        df = df.set_index("ObjectId")
        df = df.map_partitions(normalize_columns, final_columns=general_columns)
        df_melted = df.melt(
            id_vars=[col for col in general_columns if col not in year_columns],
            value_vars=year_columns,
            var_name="year",
            value_name="feature_value",
        )

        df_melted["datasource"] = path
        df_list.append(df_melted)

    data_iterim = dd.concat(df_list)

    data_processed = groupby_country(data_iterim)

    data_iterim.to_csv("data/iterim/dataConcat_silver.csv", index=False, single_file=True)
    data_processed.to_csv("data/processed/dataConcat_gold.csv", index=False)


if __name__ == "__main__":
    main()