"""
Cyclistic Bike-Share Analysis Package
===================================

A comprehensive data analysis package for Cyclistic bike-share data.

Author: Muhammad Baihaqi
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Muhammad Baihaqi"
__email__ = "bhqmuhammad@example.com"

from .cyclistic_analyzer import CyclisticAnalyzer
from .visualizations import CyclisticVisualizer
from .data_utils import DataManager

__all__ = ['CyclisticAnalyzer', 'CyclisticVisualizer', 'DataManager']