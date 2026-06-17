import pandas as pd

# The thresholds are defined here. Can easily switch these if they change in the future with improved machinery
AVG_TEMP_THRESHOLD = 85.0
VIBRATION_THRESHOLD = 15.0

# Turn the CSV data into a data frame
df = pd.read_csv("data/telemetry_data.csv")

# Ensure we only process the most recent 24 hours of data (as required)
df["timestamp"] = pd.to_datetime(df["timestamp"])
latest_time = df["timestamp"].max()
df = df[
    df["timestamp"] >= latest_time - pd.Timedelta(hours=24)
]

# Calculate average temperature and max vibration
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