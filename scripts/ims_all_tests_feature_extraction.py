import os
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
BASE_OUTPUT_FOLDER = r"PROJECT_ROOT\processed_data"

TEST_CONFIGS = [
    {
        "test_id": "1st_test",
        "input_folder": r"path_for_RAW_DATA_DIR\1st_test",
        "expected_columns": 8,
        # Test 1: 2 channels per bearing
        "bearing_map": {
            1: 1, 2: 1,
            3: 2, 4: 2,
            5: 3, 6: 3,
            7: 4, 8: 4
        }
    },
    {
        "test_id": "2nd_test",
        "input_folder": r"path_for_RAW_DATA_DIR\2nd_test",
        "expected_columns": 4,
        # Test 2: 1 channel per bearing
        "bearing_map": {
            1: 1, 2: 2, 3: 3, 4: 4
        }
    },
    {
        "test_id": "3rd_test",
        "input_folder": r"path_for_RAW_DATA_DIR\3rd_test\4th_test\txt",
        "expected_columns": 4,
        # Test 3: 1 channel per bearing
        "bearing_map": {
            1: 1, 2: 2, 3: 3, 4: 4
        }
    }
]

# =========================================================
# HELPERS
# =========================================================
def parse_timestamp_from_filename(filename: str):
    """
    Expected filename format:
    YYYY.MM.DD.HH.MM.SS
    Example:
    2004.02.12.10.32.39
    """
    try:
        return datetime.strptime(filename, "%Y.%m.%d.%H.%M.%S")
    except ValueError:
        return None


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x))))


def peak_abs(x: np.ndarray) -> float:
    return float(np.max(np.abs(x)))


def std_dev(x: np.ndarray) -> float:
    return float(np.std(x, ddof=1))


def mean_val(x: np.ndarray) -> float:
    return float(np.mean(x))


def min_val(x: np.ndarray) -> float:
    return float(np.min(x))


def max_val(x: np.ndarray) -> float:
    return float(np.max(x))


def kurtosis_pearson(x: np.ndarray) -> float:
    """
    Pearson kurtosis:
    E[((X - mu)/sigma)^4]
    Normal distribution is close to 3.
    """
    mu = np.mean(x)
    sigma = np.std(x, ddof=0)

    if sigma == 0:
        return np.nan

    z = (x - mu) / sigma
    return float(np.mean(z ** 4))


def crest_factor(x: np.ndarray) -> float:
    x_rms = rms(x)
    x_peak = peak_abs(x)
    if x_rms == 0:
        return np.nan
    return float(x_peak / x_rms)


def ensure_output_folder(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)


def process_single_test(test_config: dict):
    test_id = test_config["test_id"]
    input_folder = test_config["input_folder"]
    expected_columns = test_config["expected_columns"]
    bearing_map = test_config["bearing_map"]

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    all_files = [
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f))
    ]

    valid_files = [f for f in all_files if parse_timestamp_from_filename(f) is not None]

    if not valid_files:
        raise ValueError(f"No valid IMS timestamp files found in {input_folder}")

    valid_files = sorted(valid_files, key=parse_timestamp_from_filename)
    start_time = parse_timestamp_from_filename(valid_files[0])

    channel_rows = []
    error_rows = []

    print(f"\nProcessing {test_id} ...")
    print(f"Input folder: {input_folder}")
    print(f"Valid files found: {len(valid_files)}")
    print(f"Start time: {start_time}")

    for file_index, file_name in enumerate(valid_files, start=1):
        file_path = os.path.join(input_folder, file_name)

        try:
            df = pd.read_csv(file_path, sep=r"\s+", header=None, engine="python")

            if df.shape[1] != expected_columns:
                raise ValueError(
                    f"{test_id}: expected {expected_columns} columns, found {df.shape[1]}"
                )

            timestamp = parse_timestamp_from_filename(file_name)
            elapsed_minutes = (timestamp - start_time).total_seconds() / 60.0
            elapsed_hours = elapsed_minutes / 60.0

            for col_idx in range(df.shape[1]):
                channel = col_idx + 1
                bearing = bearing_map[channel]

                # For Test 1, this tells you whether it is the 1st or 2nd channel in a bearing pair
                if expected_columns == 8:
                    channel_in_bearing = 1 if channel % 2 == 1 else 2
                else:
                    channel_in_bearing = 1

                x = df.iloc[:, col_idx].astype(float).to_numpy()

                row = {
                    "test_id": test_id,
                    "file_name": file_name,
                    "timestamp": timestamp,
                    "file_index": file_index,
                    "elapsed_minutes": round(elapsed_minutes, 3),
                    "elapsed_hours": round(elapsed_hours, 3),
                    "bearing": bearing,
                    "channel": channel,
                    "channel_in_bearing": channel_in_bearing,
                    "sample_count": len(x),
                    "mean": round(mean_val(x), 6),
                    "std_dev": round(std_dev(x), 6),
                    "rms": round(rms(x), 6),
                    "peak_abs": round(peak_abs(x), 6),
                    "min_value": round(min_val(x), 6),
                    "max_value": round(max_val(x), 6),
                    "kurtosis": round(kurtosis_pearson(x), 6),
                    "crest_factor": round(crest_factor(x), 6),
                }
                channel_rows.append(row)

            if file_index % 100 == 0 or file_index == len(valid_files):
                print(f"Processed {file_index}/{len(valid_files)} files...")

        except Exception as e:
            error_rows.append({
                "test_id": test_id,
                "file_name": file_name,
                "error": str(e)
            })

    channel_df = pd.DataFrame(channel_rows)
    error_df = pd.DataFrame(error_rows)

    # ---------------------------------------------------------
    # Bearing-level aggregation
    # For Test 1, this averages the 2 channels that belong to the same bearing.
    # For Tests 2 and 3, it effectively stays 1 channel = 1 bearing.
    # ---------------------------------------------------------
    group_cols = [
        "test_id",
        "file_name",
        "timestamp",
        "file_index",
        "elapsed_minutes",
        "elapsed_hours",
        "bearing"
    ]

    numeric_cols = [
        "sample_count",
        "mean",
        "std_dev",
        "rms",
        "peak_abs",
        "min_value",
        "max_value",
        "kurtosis",
        "crest_factor"
    ]

    bearing_df = (
        channel_df
        .groupby(group_cols, as_index=False)[numeric_cols]
        .mean()
    )

    # Add how many channels contributed to the bearing record
    channel_count_df = (
        channel_df
        .groupby(group_cols, as_index=False)["channel"]
        .count()
        .rename(columns={"channel": "channels_per_bearing"})
    )

    bearing_df = bearing_df.merge(channel_count_df, on=group_cols, how="left")

    # Round aggregated numeric fields again for neatness
    for col in numeric_cols:
        bearing_df[col] = bearing_df[col].round(6)

    return channel_df, bearing_df, error_df


# =========================================================
# MAIN
# =========================================================
def main():
    ensure_output_folder(BASE_OUTPUT_FOLDER)

    all_channel_dfs = []
    all_bearing_dfs = []
    all_error_dfs = []

    for test_config in TEST_CONFIGS:
        channel_df, bearing_df, error_df = process_single_test(test_config)

        test_id = test_config["test_id"]

        channel_output = os.path.join(BASE_OUTPUT_FOLDER, f"ims_{test_id}_channel_features.csv")
        bearing_output = os.path.join(BASE_OUTPUT_FOLDER, f"ims_{test_id}_bearing_features.csv")

        channel_df.to_csv(channel_output, index=False)
        bearing_df.to_csv(bearing_output, index=False)

        print(f"Saved: {channel_output}")
        print(f"Saved: {bearing_output}")

        all_channel_dfs.append(channel_df)
        all_bearing_dfs.append(bearing_df)

        if not error_df.empty:
            all_error_dfs.append(error_df)

    # Combined master files
    all_tests_channel_df = pd.concat(all_channel_dfs, ignore_index=True)
    all_tests_bearing_df = pd.concat(all_bearing_dfs, ignore_index=True)

    all_tests_channel_output = os.path.join(BASE_OUTPUT_FOLDER, "ims_all_tests_channel_features.csv")
    all_tests_bearing_output = os.path.join(BASE_OUTPUT_FOLDER, "ims_all_tests_bearing_features.csv")

    all_tests_channel_df.to_csv(all_tests_channel_output, index=False)
    all_tests_bearing_df.to_csv(all_tests_bearing_output, index=False)

    print(f"\nSaved combined file: {all_tests_channel_output}")
    print(f"Saved combined file: {all_tests_bearing_output}")

    # Combined error log
    if all_error_dfs:
        all_errors_df = pd.concat(all_error_dfs, ignore_index=True)
    else:
        all_errors_df = pd.DataFrame(columns=["test_id", "file_name", "error"])

    error_output = os.path.join(BASE_OUTPUT_FOLDER, "ims_processing_errors.csv")
    all_errors_df.to_csv(error_output, index=False)

    print(f"Saved error log: {error_output}")

    print("\nDone.")
    print(f"Total channel-level rows: {len(all_tests_channel_df)}")
    print(f"Total bearing-level rows: {len(all_tests_bearing_df)}")
    print(f"Total errors logged: {len(all_errors_df)}")


if __name__ == "__main__":
    main()