"""
Data Utilities for Cyclistic Analysis
====================================

This module provides utility functions for data handling and processing.

Author: Muhammad Baihaqi
License: MIT
"""

import pandas as pd
import numpy as np
from pathlib import Path
import requests
import zipfile
import os

class DataManager:
    """
    Data management class for Cyclistic bike-share data.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize the data manager.
        
        Args:
            data_dir (str): Directory for data files
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.sample_dir = self.data_dir / "sample"
        
        # Create directories if they don't exist
        for dir_path in [self.data_dir, self.raw_dir, self.processed_dir, self.sample_dir]:
            dir_path.mkdir(exist_ok=True, parents=True)
    
    def create_sample_data(self, n_samples=10000):
        """
        Create sample data for demonstration purposes.
        
        Args:
            n_samples (int): Number of sample records to create
        """
        np.random.seed(42)
        
        print(f"Creating sample data with {n_samples:,} records...")
        
        # Create realistic sample data
        start_dates = pd.date_range('2019-01-01', '2020-03-31', periods=n_samples)
        
        # Create member_casual with realistic distribution (75% members, 25% casual)
        member_casual = np.random.choice(['member', 'casual'], n_samples, p=[0.75, 0.25])
        
        # Create ride_length with different patterns for members vs casual
        ride_length = []
        day_of_week = []
        start_hour = []
        
        for i, (date, mc) in enumerate(zip(start_dates, member_casual)):
            # Extract day of week and hour for realistic patterns
            dow = date.dayofweek
            day_of_week.append(dow)
            
            if mc == 'member':
                # Members: more rides on weekdays, peak hours 7-9am and 5-7pm
                if dow < 5:  # Weekday
                    hour = np.random.choice([7, 8, 17, 18], p=[0.3, 0.3, 0.25, 0.15])
                else:  # Weekend
                    hour = np.random.choice(range(24))
                # Shorter rides for members
                length = np.random.normal(12, 5)
            else:
                # Casual: more rides on weekends, more evenly distributed hours
                if dow >= 5:  # Weekend
                    hour = np.random.choice(range(10, 20))
                else:  # Weekday
                    hour = np.random.choice(range(24))
                # Longer rides for casual users
                length = np.random.normal(36, 15)
            
            start_hour.append(hour)
            ride_length.append(max(1, length))  # Ensure positive values
        
        # Create station IDs with some popular stations
        popular_stations = list(range(1, 21))  # 20 popular stations
        other_stations = list(range(21, 101))  # 80 other stations
        
        # Create probability distribution that sums to 1
        popular_prob = 0.05
        other_prob = (1.0 - popular_prob * 20) / 80  # Remaining probability divided among other stations
        
        start_station_ids = np.random.choice(
            popular_stations + other_stations, 
            n_samples, 
            p=[popular_prob] * 20 + [other_prob] * 80  # Popular stations get more rides
        )
        
        end_station_ids = np.random.choice(
            popular_stations + other_stations, 
            n_samples, 
            p=[popular_prob] * 20 + [other_prob] * 80
        )
        
        # Create the sample dataset
        sample_data = pd.DataFrame({
            'ride_id': [f'sample_{i:06d}' for i in range(n_samples)],
            'rideable_type': np.random.choice(['electric_bike', 'classic_bike'], n_samples, p=[0.6, 0.4]),
            'started_at': start_dates,
            'ended_at': start_dates + pd.to_timedelta(ride_length, unit='minutes'),
            'start_station_name': [f'Station_{id}' for id in start_station_ids],
            'start_station_id': start_station_ids,
            'end_station_name': [f'Station_{id}' for id in end_station_ids],
            'end_station_id': end_station_ids,
            'start_lat': np.random.uniform(41.8, 42.0, n_samples),  # Chicago lat range
            'start_lng': np.random.uniform(-87.8, -87.5, n_samples),  # Chicago lng range
            'end_lat': np.random.uniform(41.8, 42.0, n_samples),
            'end_lng': np.random.uniform(-87.8, -87.5, n_samples),
            'member_casual': member_casual
        })
        
        # Save sample data
        sample_2019 = sample_data[sample_data['started_at'].dt.year == 2019]
        sample_2020 = sample_data[sample_data['started_at'].dt.year == 2020]
        
        sample_2019.to_csv(self.sample_dir / 'Divvy_Trips_2019_Q1_sample.csv', index=False)
        sample_2020.to_csv(self.sample_dir / 'Divvy_Trips_2020_Q1_sample.csv', index=False)
        
        print(f"Sample data saved:")
        print(f"  - 2019 Q1: {len(sample_2019):,} records")
        print(f"  - 2020 Q1: {len(sample_2020):,} records")
        print(f"  - Files saved to {self.sample_dir}/")
        
        return sample_2019, sample_2020
    
    def validate_data(self, df, year=None):
        """
        Validate data quality and structure.
        
        Args:
            df (DataFrame): Data to validate
            year (int): Expected year for the data
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'statistics': {}
        }
        
        # Check required columns
        required_columns = ['ride_id', 'started_at', 'ended_at', 'member_casual']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            validation_results['is_valid'] = False
            validation_results['issues'].append(f"Missing required columns: {missing_columns}")
        
        # Check data types
        if 'started_at' in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df['started_at']):
                validation_results['warnings'].append("started_at should be datetime type")
        
        if 'ended_at' in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df['ended_at']):
                validation_results['warnings'].append("ended_at should be datetime type")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            validation_results['warnings'].append(f"Found {duplicates} duplicate records")
        
        # Check for null values
        null_counts = df.isnull().sum()
        high_null_columns = null_counts[null_counts > len(df) * 0.1]  # More than 10% null
        if not high_null_columns.empty:
            validation_results['warnings'].append(f"High null values in: {high_null_columns.to_dict()}")
        
        # Calculate statistics
        validation_results['statistics'] = {
            'total_records': len(df),
            'duplicate_records': duplicates,
            'null_values': null_counts.to_dict(),
            'date_range': None
        }
        
        if 'started_at' in df.columns and pd.api.types.is_datetime64_any_dtype(df['started_at']):
            validation_results['statistics']['date_range'] = {
                'start': df['started_at'].min(),
                'end': df['started_at'].max()
            }
        
        return validation_results
    
    def create_data_readme(self):
        """Create a README file for the data directory."""
        readme_content = """# Cyclistic Data Directory

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
"""
        
        readme_path = self.data_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"Data README created at {readme_path}")
    
    def get_file_paths(self, use_sample=False):
        """
        Get paths to data files.
        
        Args:
            use_sample (bool): Whether to use sample data
            
        Returns:
            tuple: (path_2019, path_2020)
        """
        if use_sample:
            return (
                self.sample_dir / 'Divvy_Trips_2019_Q1_sample.csv',
                self.sample_dir / 'Divvy_Trips_2020_Q1_sample.csv'
            )
        else:
            return (
                self.raw_dir / 'Divvy_Trips_2019_Q1.csv',
                self.raw_dir / 'Divvy_Trips_2020_Q1.csv'
            )
    
    def check_data_availability(self):
        """
        Check which data files are available.
        
        Returns:
            dict: Availability status of data files
        """
        raw_2019, raw_2020 = self.get_file_paths(use_sample=False)
        sample_2019, sample_2020 = self.get_file_paths(use_sample=True)
        
        availability = {
            'raw_data': {
                '2019_q1': raw_2019.exists(),
                '2020_q1': raw_2020.exists()
            },
            'sample_data': {
                '2019_q1': sample_2019.exists(),
                '2020_q1': sample_2020.exists()
            }
        }
        
        return availability
    
    def setup_data(self, force_sample=False):
        """
        Set up data for analysis, using sample data if original is not available.
        
        Args:
            force_sample (bool): Force use of sample data even if original exists
            
        Returns:
            tuple: (path_2019, path_2020, is_sample)
        """
        availability = self.check_data_availability()
        
        # Create data README
        self.create_data_readme()
        
        # Use original data if available and not forced to use sample
        if not force_sample and availability['raw_data']['2019_q1'] and availability['raw_data']['2020_q1']:
            print("Using original data files...")
            return (*self.get_file_paths(use_sample=False), False)
        
        # Check if sample data exists
        if availability['sample_data']['2019_q1'] and availability['sample_data']['2020_q1']:
            print("Using existing sample data...")
            return (*self.get_file_paths(use_sample=True), True)
        
        # Create sample data
        print("Creating sample data...")
        self.create_sample_data()
        return (*self.get_file_paths(use_sample=True), True)