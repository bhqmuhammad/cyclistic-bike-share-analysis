"""
Cyclistic Data Visualization Module
=================================

This module provides visualization functions for Cyclistic bike-share data analysis.

Author: Muhammad Baihaqi
License: MIT
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

class CyclisticVisualizer:
    """
    Visualization class for Cyclistic bike-share data.
    """
    
    def __init__(self, analyzer=None):
        """
        Initialize the visualizer.
        
        Args:
            analyzer: CyclisticAnalyzer instance with prepared data
        """
        self.analyzer = analyzer
        self.df_combined = analyzer.df_combined if analyzer else None
        
        # Set style for better-looking plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_duration_comparison_chart(self, save_path=None):
        """
        Create ride duration comparison chart.
        
        Args:
            save_path (str): Optional path to save the chart
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        fig, ax = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart of average duration
        duration_means = self.df_combined.groupby('member_casual')['ride_length'].mean()
        bars = ax[0].bar(duration_means.index, duration_means.values, 
                        color=['#3B82F6', '#10B981'], alpha=0.8)
        ax[0].set_title('Average Ride Duration by User Type', fontsize=14, fontweight='bold')
        ax[0].set_ylabel('Average Duration (minutes)')
        ax[0].set_xlabel('User Type')
        
        # Add value labels on bars
        for i, v in enumerate(duration_means.values):
            ax[0].text(i, v + 1, f'{v:.1f}min', ha='center', fontweight='bold')
        
        # Box plot for distribution
        self.df_combined.boxplot(column='ride_length', by='member_casual', ax=ax[1])
        ax[1].set_title('Ride Duration Distribution by User Type', fontsize=14, fontweight='bold')
        ax[1].set_ylabel('Ride Duration (minutes)')
        ax[1].set_xlabel('User Type')
        ax[1].set_ylim(0, 100)  # Limit y-axis for better visibility
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()
    
    def create_weekly_usage_chart(self, save_path=None):
        """
        Create weekly usage pattern chart.
        
        Args:
            save_path (str): Optional path to save the chart
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        weekly_data = self.df_combined.groupby(['member_casual', 'day_name'])['ride_id'].count().reset_index()
        weekly_pivot = weekly_data.pivot(index='day_name', columns='member_casual', values='ride_id')
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_pivot = weekly_pivot.reindex(day_order)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        weekly_pivot.plot(kind='line', ax=ax, marker='o', linewidth=3, markersize=8)
        ax.set_title('Weekly Usage Patterns by User Type', fontsize=16, fontweight='bold')
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Number of Rides', fontsize=12)
        ax.legend(title='User Type', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Highlight weekends
        weekend_indices = [5, 6]  # Saturday, Sunday
        for idx in weekend_indices:
            ax.axvspan(idx-0.5, idx+0.5, alpha=0.2, color='yellow')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()
    
    def create_hourly_usage_chart(self, save_path=None):
        """
        Create hourly usage pattern chart.
        
        Args:
            save_path (str): Optional path to save the chart
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        hourly_data = self.df_combined.groupby(['member_casual', 'start_hour'])['ride_id'].count().reset_index()
        hourly_pivot = hourly_data.pivot(index='start_hour', columns='member_casual', values='ride_id')
        
        fig, ax = plt.subplots(figsize=(14, 6))
        hourly_pivot.plot(kind='area', ax=ax, alpha=0.7)
        ax.set_title('Hourly Usage Patterns by User Type', fontsize=16, fontweight='bold')
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Number of Rides', fontsize=12)
        ax.legend(title='User Type', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Highlight commute hours
        commute_hours = [(7, 9), (17, 19)]  # Morning and evening commute
        for start, end in commute_hours:
            ax.axvspan(start, end, alpha=0.2, color='red', 
                      label='Commute Hours' if start == 7 else "")
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()
    
    def create_monthly_usage_chart(self, save_path=None):
        """
        Create monthly usage pattern chart.
        
        Args:
            save_path (str): Optional path to save the chart
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        monthly_data = self.df_combined.groupby(['member_casual', 'month'])['ride_id'].count().reset_index()
        monthly_pivot = monthly_data.pivot(index='month', columns='member_casual', values='ride_id')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_pivot.plot(kind='bar', ax=ax, alpha=0.8)
        ax.set_title('Monthly Usage Patterns by User Type', fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Rides', fontsize=12)
        ax.legend(title='User Type', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Set month labels
        month_labels = ['Jan', 'Feb', 'Mar']
        ax.set_xticklabels(month_labels, rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()
    
    def create_comprehensive_dashboard(self, save_path=None):
        """
        Create a comprehensive dashboard with all key visualizations.
        
        Args:
            save_path (str): Optional path to save the dashboard
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        # Create a large figure with subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Duration comparison
        ax1 = plt.subplot(3, 2, 1)
        duration_means = self.df_combined.groupby('member_casual')['ride_length'].mean()
        bars = ax1.bar(duration_means.index, duration_means.values, 
                      color=['#3B82F6', '#10B981'], alpha=0.8)
        ax1.set_title('Average Ride Duration by User Type', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Duration (minutes)')
        for i, v in enumerate(duration_means.values):
            ax1.text(i, v + 1, f'{v:.1f}min', ha='center', fontweight='bold')
        
        # 2. Weekly patterns
        ax2 = plt.subplot(3, 2, 2)
        weekly_data = self.df_combined.groupby(['member_casual', 'day_name'])['ride_id'].count().reset_index()
        weekly_pivot = weekly_data.pivot(index='day_name', columns='member_casual', values='ride_id')
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_pivot = weekly_pivot.reindex(day_order)
        weekly_pivot.plot(kind='line', ax=ax2, marker='o', linewidth=2)
        ax2.set_title('Weekly Usage Patterns', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Rides')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Hourly patterns
        ax3 = plt.subplot(3, 2, 3)
        hourly_data = self.df_combined.groupby(['member_casual', 'start_hour'])['ride_id'].count().reset_index()
        hourly_pivot = hourly_data.pivot(index='start_hour', columns='member_casual', values='ride_id')
        hourly_pivot.plot(kind='area', ax=ax3, alpha=0.7)
        ax3.set_title('Hourly Usage Patterns', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Number of Rides')
        
        # 4. Duration distribution
        ax4 = plt.subplot(3, 2, 4)
        for user_type in ['casual', 'member']:
            data = self.df_combined[self.df_combined['member_casual'] == user_type]['ride_length']
            ax4.hist(data, bins=50, alpha=0.7, label=user_type, density=True)
        ax4.set_title('Ride Duration Distribution', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Duration (minutes)')
        ax4.set_ylabel('Density')
        ax4.set_xlim(0, 100)
        ax4.legend()
        
        # 5. Weekend vs Weekday
        ax5 = plt.subplot(3, 2, 5)
        weekend_stats = self.df_combined.groupby(['member_casual', 'is_weekend'])['ride_id'].count().unstack()
        weekend_stats_pct = weekend_stats.div(weekend_stats.sum(axis=1), axis=0) * 100
        weekend_stats_pct.plot(kind='bar', ax=ax5, stacked=True)
        ax5.set_title('Weekend vs Weekday Usage (%)', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Percentage')
        ax5.legend(['Weekday', 'Weekend'])
        ax5.tick_params(axis='x', rotation=0)
        
        # 6. Summary statistics table
        ax6 = plt.subplot(3, 2, 6)
        ax6.axis('tight')
        ax6.axis('off')
        
        # Create summary table
        summary_data = []
        for user_type in ['casual', 'member']:
            user_data = self.df_combined[self.df_combined['member_casual'] == user_type]
            summary_data.append([
                user_type.title(),
                f"{len(user_data):,}",
                f"{user_data['ride_length'].mean():.1f} min",
                f"{(user_data['is_weekend'].sum() / len(user_data) * 100):.1f}%"
            ])
        
        table = ax6.table(cellText=summary_data,
                         colLabels=['User Type', 'Total Rides', 'Avg Duration', 'Weekend %'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        ax6.set_title('Summary Statistics', fontsize=12, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()
    
    def generate_all_visualizations(self, output_dir="assets"):
        """
        Generate and save all visualizations.
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        if self.df_combined is None:
            print("No data available for visualization.")
            return
            
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        print("Generating visualizations...")
        
        # Generate individual charts
        self.create_duration_comparison_chart(f"{output_dir}/duration_comparison.png")
        self.create_weekly_usage_chart(f"{output_dir}/weekly_patterns.png")
        self.create_hourly_usage_chart(f"{output_dir}/hourly_patterns.png")
        self.create_monthly_usage_chart(f"{output_dir}/monthly_patterns.png")
        self.create_comprehensive_dashboard(f"{output_dir}/comprehensive_dashboard.png")
        
        print(f"All visualizations saved to {output_dir}/ directory")