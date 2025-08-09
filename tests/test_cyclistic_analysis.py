"""
Test suite for Cyclistic Analysis
===============================

Basic tests to ensure the analysis modules work correctly.

Author: Muhammad Baihaqi
License: MIT
"""

import unittest
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from cyclistic_analyzer import CyclisticAnalyzer
from visualizations import CyclisticVisualizer
from data_utils import DataManager


class TestCyclisticAnalyzer(unittest.TestCase):
    """Test cases for CyclisticAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CyclisticAnalyzer()
        
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        self.assertIsInstance(self.analyzer, CyclisticAnalyzer)
        self.assertIsNone(self.analyzer.df_combined)
        self.assertIsInstance(self.analyzer.analysis_results, dict)
    
    def test_sample_data_creation(self):
        """Test sample data creation."""
        self.analyzer.prepare_data()  # This should create sample data
        
        self.assertIsNotNone(self.analyzer.df_combined)
        self.assertGreater(len(self.analyzer.df_combined), 0)
        
        # Check required columns exist
        required_columns = ['ride_id', 'started_at', 'ended_at', 'member_casual', 'ride_length']
        for col in required_columns:
            self.assertIn(col, self.analyzer.df_combined.columns)
    
    def test_standardize_columns(self):
        """Test column standardization."""
        # Create test dataframe with 2019 format
        test_df = pd.DataFrame({
            'trip_id': ['1', '2'],
            'start_time': ['2019-01-01 00:00:00', '2019-01-01 01:00:00'],
            'usertype': ['Subscriber', 'Customer']
        })
        
        standardized = self.analyzer.standardize_columns(test_df, 2019)
        
        self.assertIn('ride_id', standardized.columns)
        self.assertIn('started_at', standardized.columns)
        self.assertIn('member_casual', standardized.columns)
    
    def test_duration_analysis(self):
        """Test ride duration analysis."""
        self.analyzer.prepare_data()  # Create sample data
        results = self.analyzer.analyze_ride_duration()
        
        self.assertIsNotNone(results)
        self.assertIn('casual', results.index)
        self.assertIn('member', results.index)
        self.assertIn('mean', results.columns)


class TestDataManager(unittest.TestCase):
    """Test cases for DataManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = DataManager(data_dir="test_data")
    
    def test_data_manager_initialization(self):
        """Test that data manager initializes correctly."""
        self.assertIsInstance(self.data_manager, DataManager)
        self.assertEqual(self.data_manager.data_dir.name, "test_data")
    
    def test_sample_data_creation(self):
        """Test sample data creation."""
        df_2019, df_2020 = self.data_manager.create_sample_data(n_samples=100)
        
        self.assertIsInstance(df_2019, pd.DataFrame)
        self.assertIsInstance(df_2020, pd.DataFrame)
        self.assertGreater(len(df_2019), 0)
        self.assertGreater(len(df_2020), 0)
    
    def test_data_validation(self):
        """Test data validation function."""
        # Create test dataframe
        test_df = pd.DataFrame({
            'ride_id': ['1', '2', '3'],
            'started_at': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-03']),
            'ended_at': pd.to_datetime(['2019-01-01 01:00:00', '2019-01-02 01:00:00', '2019-01-03 01:00:00']),
            'member_casual': ['member', 'casual', 'member']
        })
        
        validation_results = self.data_manager.validate_data(test_df)
        
        self.assertIsInstance(validation_results, dict)
        self.assertIn('is_valid', validation_results)
        self.assertIn('statistics', validation_results)


class TestCyclisticVisualizer(unittest.TestCase):
    """Test cases for CyclisticVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CyclisticAnalyzer()
        self.analyzer.prepare_data()  # Create sample data
        self.visualizer = CyclisticVisualizer(self.analyzer)
    
    def test_visualizer_initialization(self):
        """Test that visualizer initializes correctly."""
        self.assertIsInstance(self.visualizer, CyclisticVisualizer)
        self.assertIsNotNone(self.visualizer.df_combined)
        self.assertEqual(self.visualizer.analyzer, self.analyzer)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete analysis pipeline."""
    
    def test_complete_analysis_pipeline(self):
        """Test the complete analysis pipeline."""
        # Initialize components
        data_manager = DataManager(data_dir="test_data")
        analyzer = CyclisticAnalyzer()
        
        # Run analysis
        analyzer.prepare_data()  # Use sample data
        results = analyzer.run_complete_analysis()
        
        # Check results
        self.assertIsNotNone(results)
        self.assertIsInstance(results, dict)
        self.assertIn('total_rides', results)
        self.assertIn('casual_rides', results)
        self.assertIn('member_rides', results)
        
        # Verify data integrity
        total = results['total_rides']
        casual = results['casual_rides']
        member = results['member_rides']
        
        self.assertEqual(total, casual + member)
        self.assertGreater(total, 0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)