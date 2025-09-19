"""
Football Analytics Dashboard Utilities

This package contains data processing, visualization, and metrics calculation
utilities for comprehensive football match analysis.
"""

from .data_processor import FootballDataProcessor, AdvancedMetrics
from .visualizations import FootballVisualizer
from .metrics_calculator import AdvancedMetricsCalculator, PredictiveMetrics

__version__ = "1.0.0"
__author__ = "Football Analytics Team"

__all__ = [
    'FootballDataProcessor',
    'AdvancedMetrics', 
    'FootballVisualizer',
    'AdvancedMetricsCalculator',
    'PredictiveMetrics'
]