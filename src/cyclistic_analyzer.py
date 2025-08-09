"""
Cyclistic Bike-Share Data Analysis
================================

This module provides comprehensive data analysis tools for Cyclistic bike-share data.
It includes functions for data cleaning, analysis, and visualization.

Author: Muhammad Baihaqi
License: MIT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CyclisticAnalyzer:
    """
    Main analyzer class for Cyclistic bike-share data analysis.
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.df_combined = None
        self.analysis_results = {}
        
    def load_data(self, file_2019, file_2020):
        """
        Load and combine Q1 data from 2019 and 2020.
        
        Args:
            file_2019 (str): Path to 2019 Q1 CSV file
            file_2020 (str): Path to 2020 Q1 CSV file
            
        Returns:
            tuple: (df_2019, df_2020) DataFrames
        """
        try:
            df_2019 = pd.read_csv(file_2019)
            df_2020 = pd.read_csv(file_2020)
            
            print(f"2019 Q1 Dataset Shape: {df_2019.shape}")
            print(f"2020 Q1 Dataset Shape: {df_2020.shape}")
            print(f"2019 Q1 Columns: {df_2019.columns.tolist()}")
            print(f"2020 Q1 Columns: {df_2020.columns.tolist()}")
            
            return df_2019, df_2020
            
        except FileNotFoundError as e:
            print(f"Error loading data files: {e}")
            print("Please ensure the CSV files are in the data/ directory")
            return None, None
    
    def standardize_columns(self, df, year):
        """
        Standardize column names between datasets.
        
        Args:
            df (DataFrame): Input DataFrame
            year (int): Year of the dataset (2019 or 2020)
            
        Returns:
            DataFrame: DataFrame with standardized columns
        """
        if year == 2019:
            df = df.rename(columns={
                'trip_id': 'ride_id',
                'start_time': 'started_at',
                'end_time': 'ended_at',
                'bikeid': 'bike_id',
                'tripduration': 'trip_duration',
                'from_station_id': 'start_station_id',
                'from_station_name': 'start_station_name',
                'to_station_id': 'end_station_id',
                'to_station_name': 'end_station_name',
                'usertype': 'member_casual',
                'gender': 'gender',
                'birthyear': 'birth_year'
            })
        return df
    
    def add_calculated_columns(self, df):
        """
        Add calculated columns for analysis.
        
        Args:
            df (DataFrame): Input DataFrame
            
        Returns:
            DataFrame: DataFrame with additional calculated columns
        """
        # Calculate ride length in minutes
        df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
        
        # Extract day of week (0=Monday, 6=Sunday)
        df['day_of_week'] = df['started_at'].dt.dayofweek
        df['day_name'] = df['started_at'].dt.day_name()
        
        # Extract hour for time-based analysis
        df['start_hour'] = df['started_at'].dt.hour
        
        # Extract month and year
        df['month'] = df['started_at'].dt.month
        df['year'] = df['started_at'].dt.year
        
        # Create weekend indicator
        df['is_weekend'] = df['day_of_week'].isin([5, 6])  # Saturday and Sunday
        
        return df
    
    def clean_data(self, df):
        """
        Remove invalid data and outliers.
        
        Args:
            df (DataFrame): Input DataFrame
            
        Returns:
            DataFrame: Cleaned DataFrame
        """
        initial_rows = len(df)
        
        # Remove rides with negative or zero duration
        df = df[df['ride_length'] > 0]
        
        # Remove extremely long rides (likely data errors) - over 24 hours
        df = df[df['ride_length'] <= 1440]  # 24 hours in minutes
        
        # Remove extremely short rides (likely false starts) - under 1 minute
        df = df[df['ride_length'] >= 1]
        
        # Remove rides with missing station information
        df = df.dropna(subset=['start_station_id', 'end_station_id'])
        
        final_rows = len(df)
        removed_pct = ((initial_rows - final_rows) / initial_rows * 100)
        print(f"Removed {initial_rows - final_rows} invalid records ({removed_pct:.2f}%)")
        
        return df
    
    def prepare_data(self, file_2019=None, file_2020=None):
        """
        Complete data preparation pipeline.
        
        Args:
            file_2019 (str): Path to 2019 Q1 CSV file
            file_2020 (str): Path to 2020 Q1 CSV file
        """
        # Use sample data if files not provided
        if file_2019 is None or file_2020 is None:
            print("Using sample data for demonstration...")
            self._create_sample_data()
            return
            
        # Load data
        df_2019, df_2020 = self.load_data(file_2019, file_2020)
        if df_2019 is None or df_2020 is None:
            print("Failed to load data. Using sample data instead...")
            self._create_sample_data()
            return
        
        # Standardize columns
        df_2019_clean = self.standardize_columns(df_2019.copy(), 2019)
        df_2020_clean = df_2020.copy()
        
        # Convert datetime columns
        datetime_columns = ['started_at', 'ended_at']
        for col in datetime_columns:
            df_2019_clean[col] = pd.to_datetime(df_2019_clean[col])
            df_2020_clean[col] = pd.to_datetime(df_2020_clean[col])
        
        # Standardize member_casual values
        df_2019_clean['member_casual'] = df_2019_clean['member_casual'].map({
            'Subscriber': 'member',
            'Customer': 'casual'
        })
        
        # Add calculated columns
        df_2019_clean = self.add_calculated_columns(df_2019_clean)
        df_2020_clean = self.add_calculated_columns(df_2020_clean)
        
        # Clean data
        df_2019_final = self.clean_data(df_2019_clean)
        df_2020_final = self.clean_data(df_2020_clean)
        
        # Combine datasets
        self.df_combined = pd.concat([df_2019_final, df_2020_final], ignore_index=True)
        print(f"Combined dataset shape: {self.df_combined.shape}")
    
    def _create_sample_data(self):
        """Create sample data for demonstration purposes."""
        np.random.seed(42)
        
        # Create sample data with realistic patterns
        n_samples = 10000
        start_dates = pd.date_range('2019-01-01', '2020-03-31', periods=n_samples)
        
        # Create member_casual with realistic distribution
        member_casual = np.random.choice(['member', 'casual'], n_samples, p=[0.75, 0.25])
        
        # Create ride_length with different patterns for members vs casual
        ride_length = []
        for mc in member_casual:
            if mc == 'member':
                # Members: shorter rides, normal distribution around 12 minutes
                length = np.random.normal(12, 5)
            else:
                # Casual: longer rides, normal distribution around 36 minutes
                length = np.random.normal(36, 15)
            ride_length.append(max(1, length))  # Ensure positive values
        
        self.df_combined = pd.DataFrame({
            'ride_id': [f'sample_{i}' for i in range(n_samples)],
            'started_at': start_dates,
            'ended_at': start_dates + pd.to_timedelta(ride_length, unit='minutes'),
            'member_casual': member_casual,
            'ride_length': ride_length,
            'start_station_id': np.random.randint(1, 100, n_samples),
            'end_station_id': np.random.randint(1, 100, n_samples)
        })
        
        # Add calculated columns
        self.df_combined = self.add_calculated_columns(self.df_combined)
        
        print("Sample data created successfully!")
        print(f"Sample dataset shape: {self.df_combined.shape}")
    
    def analyze_ride_duration(self):
        """
        Analyze ride duration by user type.
        
        Returns:
            DataFrame: Duration statistics by user type
        """
        if self.df_combined is None:
            print("No data available. Please run prepare_data() first.")
            return None
            
        duration_stats = self.df_combined.groupby('member_casual')['ride_length'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        
        print("Ride Duration Analysis:")
        print(duration_stats)
        
        # Calculate percentage difference
        casual_avg = duration_stats.loc['casual', 'mean']
        member_avg = duration_stats.loc['member', 'mean']
        percentage_diff = ((casual_avg - member_avg) / member_avg) * 100
        
        print(f"\nCasual riders take {percentage_diff:.1f}% longer rides than members")
        print(f"Casual avg: {casual_avg:.1f} minutes")
        print(f"Member avg: {member_avg:.1f} minutes")
        
        # Store results
        self.analysis_results['duration_stats'] = duration_stats
        self.analysis_results['casual_avg_duration'] = casual_avg
        self.analysis_results['member_avg_duration'] = member_avg
        
        return duration_stats
    
    def analyze_weekly_patterns(self):
        """
        Analyze usage patterns by day of week.
        
        Returns:
            DataFrame: Weekly usage patterns by user type
        """
        if self.df_combined is None:
            print("No data available. Please run prepare_data() first.")
            return None
            
        weekly_stats = self.df_combined.groupby(['member_casual', 'day_name'])['ride_id'].count().reset_index()
        weekly_pivot = weekly_stats.pivot(index='day_name', columns='member_casual', values='ride_id')
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_pivot = weekly_pivot.reindex(day_order)
        
        print("Weekly Usage Patterns:")
        print(weekly_pivot)
        
        # Calculate weekend vs weekday usage
        weekend_days = ['Saturday', 'Sunday']
        weekday_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for user_type in ['casual', 'member']:
            if user_type in weekly_pivot.columns:
                weekend_rides = weekly_pivot.loc[weekend_days, user_type].sum()
                weekday_rides = weekly_pivot.loc[weekday_days, user_type].sum()
                weekend_pct = (weekend_rides / (weekend_rides + weekday_rides)) * 100
                
                print(f"\n{user_type.title()} riders:")
                print(f"Weekend usage: {weekend_pct:.1f}%")
                print(f"Weekday usage: {100-weekend_pct:.1f}%")
                
                # Store results
                self.analysis_results[f'{user_type}_weekend_pct'] = weekend_pct
        
        return weekly_pivot
    
    def analyze_hourly_patterns(self):
        """
        Analyze usage patterns by hour of day.
        
        Returns:
            DataFrame: Hourly usage patterns by user type
        """
        if self.df_combined is None:
            print("No data available. Please run prepare_data() first.")
            return None
            
        hourly_stats = self.df_combined.groupby(['member_casual', 'start_hour'])['ride_id'].count().reset_index()
        hourly_pivot = hourly_stats.pivot(index='start_hour', columns='member_casual', values='ride_id')
        
        # Find peak hours
        for user_type in ['casual', 'member']:
            if user_type in hourly_pivot.columns:
                peak_hour = hourly_pivot[user_type].idxmax()
                peak_count = hourly_pivot[user_type].max()
                print(f"{user_type.title()} peak hour: {peak_hour}:00 ({peak_count} rides)")
        
        return hourly_pivot
    
    def run_complete_analysis(self):
        """
        Run the complete analysis pipeline.
        
        Returns:
            dict: Analysis results summary
        """
        print("="*50)
        print("CYCLISTIC BIKE-SHARE ANALYSIS RESULTS")
        print("="*50)
        
        if self.df_combined is None:
            print("No data available. Please run prepare_data() first.")
            return None
        
        # Basic dataset statistics
        total_rides = len(self.df_combined)
        casual_rides = len(self.df_combined[self.df_combined['member_casual'] == 'casual'])
        member_rides = len(self.df_combined[self.df_combined['member_casual'] == 'member'])
        
        print(f"Total rides analyzed: {total_rides:,}")
        print(f"Date range: {self.df_combined['started_at'].min()} to {self.df_combined['started_at'].max()}")
        print(f"Casual riders: {casual_rides:,}")
        print(f"Annual members: {member_rides:,}")
        
        # Store basic stats
        self.analysis_results.update({
            'total_rides': total_rides,
            'casual_rides': casual_rides,
            'member_rides': member_rides
        })
        
        print("\n" + "="*50)
        self.analyze_ride_duration()
        
        print("\n" + "="*50)
        self.analyze_weekly_patterns()
        
        print("\n" + "="*50)
        self.analyze_hourly_patterns()
        
        return self.analysis_results
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        if self.df_combined is None:
            print("No data available. Please run prepare_data() first.")
            return
            
        print("\n" + "="*60)
        print("EXECUTIVE SUMMARY - CYCLISTIC BIKE-SHARE ANALYSIS")
        print("="*60)
        
        total_rides = len(self.df_combined)
        casual_rides = len(self.df_combined[self.df_combined['member_casual'] == 'casual'])
        member_rides = len(self.df_combined[self.df_combined['member_casual'] == 'member'])
        
        print(f"📊 DATASET OVERVIEW:")
        print(f"   • Total rides analyzed: {total_rides:,}")
        print(f"   • Casual rider trips: {casual_rides:,} ({casual_rides/total_rides*100:.1f}%)")
        print(f"   • Member trips: {member_rides:,} ({member_rides/total_rides*100:.1f}%)")
        
        # Duration insights
        casual_avg = self.df_combined[self.df_combined['member_casual'] == 'casual']['ride_length'].mean()
        member_avg = self.df_combined[self.df_combined['member_casual'] == 'member']['ride_length'].mean()
        
        print(f"\n🚴‍♀️ RIDE DURATION INSIGHTS:")
        print(f"   • Casual rider average: {casual_avg:.1f} minutes")
        print(f"   • Member average: {member_avg:.1f} minutes")
        print(f"   • Casual riders take {casual_avg/member_avg:.1f}x longer rides")
        
        # Weekly patterns
        weekend_data = self.df_combined[self.df_combined['is_weekend'] == True]
        casual_weekend_pct = len(weekend_data[weekend_data['member_casual'] == 'casual']) / casual_rides * 100
        member_weekend_pct = len(weekend_data[weekend_data['member_casual'] == 'member']) / member_rides * 100
        
        print(f"\n📅 WEEKLY USAGE PATTERNS:")
        print(f"   • Casual riders - Weekend usage: {casual_weekend_pct:.1f}%")
        print(f"   • Members - Weekend usage: {member_weekend_pct:.1f}%")
        print(f"   • Weekend preference ratio: {casual_weekend_pct/member_weekend_pct:.1f}x higher for casual riders")
        
        print(f"\n💡 KEY BUSINESS INSIGHTS:")
        print(f"   • Casual riders prefer recreational, longer rides")
        print(f"   • Members use bikes for functional, shorter commutes")
        print(f"   • Weekend marketing could target casual riders effectively")
        print(f"   • Commuter benefits should be marketed to convert casual riders")