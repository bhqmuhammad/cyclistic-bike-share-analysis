# Cyclistic Data Directory

This directory contains data files for the Cyclistic bike-share analysis project.

## Directory Structure

```
data/
├── raw/                    # Raw data files (CSV format)
├── processed/             # Cleaned and processed data
├── sample/               # Sample data for demonstration
└── README.md            # This file
```

## Data Sources

The original data comes from Divvy (Chicago's bike-share system) and is made available by Motivate International Inc. under the [Divvy Data License Agreement](https://ride.divvybikes.com/data-license-agreement).

### Required Files

For the complete analysis, you need the following CSV files in the `raw/` directory:
- `Divvy_Trips_2019_Q1.csv` - Q1 2019 trip data
- `Divvy_Trips_2020_Q1.csv` - Q1 2020 trip data

### Data Download

Due to size constraints, the actual data files are not included in this repository. 

To download the data:
1. Visit [Divvy System Data](https://divvy-tripdata.s3.amazonaws.com/index.html)
2. Download the Q1 2019 and Q1 2020 trip data
3. Place the CSV files in the `data/raw/` directory

### Sample Data

If you don't have access to the original data files, sample data is provided in the `sample/` directory for demonstration purposes. The sample data maintains the same structure and statistical patterns as the original data.

## Data Schema

The data files should contain the following columns:

### 2019 Q1 Format
- `trip_id`: Unique identifier for the trip
- `start_time`: Start time of the trip
- `end_time`: End time of the trip
- `bikeid`: Unique identifier for the bike
- `tripduration`: Duration of the trip in seconds
- `from_station_id`: ID of the start station
- `from_station_name`: Name of the start station
- `to_station_id`: ID of the end station
- `to_station_name`: Name of the end station
- `usertype`: User type (Subscriber/Customer)
- `gender`: Gender of the user
- `birthyear`: Birth year of the user

### 2020 Q1 Format
- `ride_id`: Unique identifier for the trip
- `rideable_type`: Type of bike used
- `started_at`: Start time of the trip
- `ended_at`: End time of the trip
- `start_station_name`: Name of the start station
- `start_station_id`: ID of the start station
- `end_station_name`: Name of the end station
- `end_station_id`: ID of the end station
- `start_lat`: Latitude of start station
- `start_lng`: Longitude of start station
- `end_lat`: Latitude of end station
- `end_lng`: Longitude of end station
- `member_casual`: User type (member/casual)

## Data Privacy

The data has been processed to remove trips that are taken by staff as they service and inspect the system, and any trips below 60 seconds in length. Personal data that could be used to identify individual users has been removed.

## Usage

To use the data in your analysis:

```python
from src.data_utils import DataManager

# Initialize data manager
dm = DataManager()

# Create sample data if original files are not available
dm.create_sample_data()

# Use with the analyzer
from src.cyclistic_analyzer import CyclisticAnalyzer
analyzer = CyclisticAnalyzer()
analyzer.prepare_data(
    'data/raw/Divvy_Trips_2019_Q1.csv',
    'data/raw/Divvy_Trips_2020_Q1.csv'
)
```

## License

The data is made available under the [Divvy Data License Agreement](https://ride.divvybikes.com/data-license-agreement).
