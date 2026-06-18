# IEUK Sector Skills Project

## Contents

- `src/main.py`: The data processing script. Parses `telemetry_data.csv`, calculates average temperature and maximum vibrations per turbine and flags turbines breaching the anomaly thresholds.
- `Dockerfile` / `.dockerignore`: Containerises the script for consistent, portable execution.
- `data/telemetry_data.csv`: The provided telemetry data.
- `architecture/architecture_diagram.pdf`: Proposed System Architecture Diagram.
- `report/report.txt`: 300-word Engineering Report, summarising my work.
- `requirements.txt`: Python dependencies.

## Running the Code

To get the repository, run `git clone https://github.com/JamesThoburn/ieuk-engineering-project.git` in the terminal. 

Alternatively, you can download this repository as a zip by scrolling to the top of this page, clicking on the green "Code" dropdown, clicking "Download ZIP", then extracting the ZIP file in your folder of choice.

Then you can run the code in two ways:

1. Running locally (without Docker)
2. Running via Docker

### Running locally (without Docker)

Ensure you are in ieuk-engineering-project folder before you run the following terminal commands:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Running via Docker

Ensure that Docker is running on your computer and you are in ieuk-engineering-project folder before you run the following terminal commands: 

```
docker build -t aerogrid-telemetry .
docker run --rm -v "${pwd}/data:/app/data" aerogrid-telemetry
```

The CSV is mounted at runtime rather than being baked into the image. This reflects how in a cloud environment data wouldn't be baked into the image, giving a more representative model of what the implementation would actually be like.

### Expected Output

```
===== FAILING TURBINES =====

Turbine ID: T-04 | Average Temperature: 90.48°C | Maximum Vibration: 10.00 mm/s
Turbine ID: T-07 | Average Temperature: 68.10°C | Maximum Vibration: 25.00 mm/s
```