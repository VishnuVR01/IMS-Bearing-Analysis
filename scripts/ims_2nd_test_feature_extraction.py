import os
import numpy as np
import pandas as pd
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
INPUT_FOLDER = r"D:\Learning\Data Analytics\Projects\IMS\2nd_test\2nd_test"
OUTPUT_CSV = r"D:\Learning\Data Analytics\Projects\IMS\processed_ims_2nd_test_features.csv"
ERROR_LOG_CSV = r"D:\Learning\Data Analytics\Projects\IMS\processed_ims_2nd_test_errors.csv"

TEST_ID = "2nd_test"
EXPECTED_COLUMNS = 4


# =========================================================
# HELPERS
# =========================================================
def parse_timestamp_from_filename(filename: str):
    """
    Example filename:
    2004.02.12.10.32.39
    -> datetime(2004, 2, 12, 10, 32, 39)
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


def process_file(file_path: str, file_name: str, file_index: int, start_time: datetime):
    """
    Reads one IMS file and returns feature rows for its 4 channels.
    """
    # Read whitespace-separated numeric text
    df = pd.read_csv(file_path, sep=r"\s+", header=None, engine="python")

    if df.shape[1] != EXPECTED_COLUMNS:
        raise ValueError(
            f"Expected {EXPECTED_COLUMNS} columns, but found {df.shape[1]}"
        )

    timestamp = parse_timestamp_from_filename(file_name)
    if timestamp is None:
        raise ValueError(f"Could not parse timestamp from filename: {file_name}")

    elapsed_minutes = (timestamp - start_time).total_seconds() / 60.0
    elapsed_hours = elapsed_minutes / 60.0

    rows = []

    for channel_idx in range(df.shape[1]):
        bearing = channel_idx + 1   # For 2nd_test: 1 channel = 1 bearing
        channel = channel_idx + 1

        x = df.iloc[:, channel_idx].astype(float).to_numpy()

        row = {
            "test_id": TEST_ID,
            "file_name": file_name,
            "timestamp": timestamp,
            "file_index": file_index,
            "elapsed_minutes": round(elapsed_minutes, 3),
            "elapsed_hours": round(elapsed_hours, 3),
            "bearing": bearing,
            "channel": channel,
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
        rows.append(row)

    return rows


# =========================================================
# MAIN
# =========================================================
def main():
    if not os.path.exists(INPUT_FOLDER):
        raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")

    all_files = [
        f for f in os.listdir(INPUT_FOLDER)
        if os.path.isfile(os.path.join(INPUT_FOLDER, f))
    ]

    # Keep only files that match the IMS timestamp naming pattern
    valid_files = [f for f in all_files if parse_timestamp_from_filename(f) is not None]

    if not valid_files:
        raise ValueError("No valid IMS timestamp files found in the folder.")

    # Sort by actual timestamp
    valid_files = sorted(valid_files, key=parse_timestamp_from_filename)

    start_time = parse_timestamp_from_filename(valid_files[0])

    feature_rows = []
    error_rows = []

    print(f"Found {len(valid_files)} valid files.")
    print(f"Start time: {start_time}")

    for idx, file_name in enumerate(valid_files, start=1):
        file_path = os.path.join(INPUT_FOLDER, file_name)

        try:
            rows = process_file(file_path, file_name, idx, start_time)
            feature_rows.extend(rows)

            if idx % 100 == 0 or idx == len(valid_files):
                print(f"Processed {idx}/{len(valid_files)} files...")

        except Exception as e:
            error_rows.append({
                "file_name": file_name,
                "error": str(e)
            })

    features_df = pd.DataFrame(feature_rows)
    errors_df = pd.DataFrame(error_rows)

    # Save outputs
    features_df.to_csv(OUTPUT_CSV, index=False)
    errors_df.to_csv(ERROR_LOG_CSV, index=False)

    print("\nDone.")
    print(f"Feature rows created: {len(features_df)}")
    print(f"Errors logged: {len(errors_df)}")
    print(f"Features CSV saved to: {OUTPUT_CSV}")
    print(f"Error log saved to: {ERROR_LOG_CSV}")

    print("\nPreview:")
    print(features_df.head(12))


if __name__ == "__main__":
    main()
