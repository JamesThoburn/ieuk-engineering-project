import sys
import pandas as pd

# The thresholds are defined here. Can easily switch these if they change in the future with improved machinery
AVG_TEMP_THRESHOLD = 85.0
VIBRATION_THRESHOLD = 15.0

try:
    # Turn the CSV data into a data frame
    df = pd.read_csv("data/telemetry_data.csv")
except FileNotFoundError:
    # Handle FileNotFoundError
    sys.exit(f"ERROR: 'data/telemetry_data.csv' not found.")
except pd.errors.EmptyDataError:
    # Handle if the file is empty
    sys.exit(f"ERROR: 'data/telemetry_data.csv' exists but contains no data.")

# Check for missing columns
REQUIRED_COLUMNS = {"timestamp", "turbine_id", "temperature_c", "vibration_mm_s"}
missing_columns = REQUIRED_COLUMNS - set(df.columns)
if missing_columns:
    sys.exit(f"ERROR: missing expected column(s): {sorted(missing_columns)}. Found columns: {list(df.columns)}.")

# Check if data frame is empty
if df.empty:
    sys.exit(f"ERROR: CSV loaded but contains zero rows. Nothing to process.")

# Turn timestamp into a DateTime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Get rid of any rows that contain NA timestamps
if df["timestamp"].isna().any():
    number_of_bad_rows = df["timestamp"].isna().sum()
    print(f"WARNING: {number_of_bad_rows} row(s) had an unparseable timestamp and will be dropped.")
    df = df.dropna(subset=["timestamp"])

# Ensure we only process the most recent 24 hours of data (as required)
latest_time = df["timestamp"].max()
df = df[
    df["timestamp"] >= latest_time - pd.Timedelta(hours=24)
]

# Check that there are still rows remaining after filtering
if df.empty:
    sys.exit("ERROR: no rows fall within the most recent 24-hour window after filtering. Check sensor feed and timestamps.")

# Calculate average temperature and max vibration
# NOTE: mean and max skip over NA values, meaning that we don't need to formally check for them
# This does increase risk for turbines with little to no readings over the 24-hours, but handling
# turbines that can't read properly (maybe they went down) is not the purpose of this script
turbine_metrics = (
    df.groupby("turbine_id")
    .agg(
        average_temperature=("temperature_c", "mean"),
        max_vibration=("vibration_mm_s", "max")
    )
    .reset_index()
)

# Check the failing condition on each turbine
turbine_metrics["failing"] = (
    (turbine_metrics["average_temperature"] > AVG_TEMP_THRESHOLD)
    |
    (turbine_metrics["max_vibration"] > VIBRATION_THRESHOLD)
)

# Pick out only the rows where the turbine is failing
failing = turbine_metrics[turbine_metrics["failing"]]

# Check if any turbines need maintenance
if failing.empty:
    print("No turbines require urgent maintenance")
else:
    print("\n===== FAILING TURBINES =====\n")
    # Turn the failing turbine_ids into a list and output it
    for _, row in failing.iterrows():
        print(
            f"Turbine ID: {row['turbine_id']} | "
            f"Average Temperature: {row['average_temperature']:.2f}°C | "
            f"Maximum Vibration: {row['max_vibration']:.2f} mm/s"
        )