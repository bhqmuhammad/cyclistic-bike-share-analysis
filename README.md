
# Cyclistic Bike-Share Analysis: Converting Casual Riders to Annual Members

[![HTML](https://img.shields.io/badge/HTML-Interactive%20Presentation-orange)](https://github.com/bhqmuhammad/cyclistic-bike-share-analysis)
[![Data Analysis](https://img.shields.io/badge/Data%20Analysis-Python%20%7C%20Pandas-blue)](https://github.com/bhqmuhammad/cyclistic-bike-share-analysis)
[![Google Data Analytics](https://img.shields.io/badge/Google%20Data%20Analytics-Capstone%20Project-green)](https://www.coursera.org/professional-certificates/google-data-analytics)

**A comprehensive data analysis project demonstrating the complete data analytics process from Ask to Act, with actionable marketing recommendations for a bike-share company.**

---

## 🎯 Project Overview

This capstone project for the Google Data Analytics Professional Certificate analyzes how casual riders and annual members use Cyclistic bikes differently. The goal is to design marketing strategies aimed at converting casual riders into annual members.

### 🏢 Business Scenario
- **Company**: Cyclistic, a fictional bike-share company in Chicago
- **Challenge**: Maximize annual memberships by converting casual riders
- **Stakeholders**: Director of Marketing Lily Moreno, Marketing Team, Executive Team

---

## 📊 Key Findings

### 🚴‍♀️ Finding #1: Ride Duration Differences
- **Annual Members**: Average 12-minute rides (functional, commute-focused)
- **Casual Riders**: Average 36-minute rides (3x longer, leisure-focused)

### 📅 Finding #2: Weekly Usage Patterns
- **Annual Members**: Consistent weekday usage with morning/evening peaks
- **Casual Riders**: Massive weekend spikes (Saturday & Sunday)

---

## 💡 Strategic Recommendations

### 1. 🎯 Weekend Warrior Membership
Create a discounted weekend-focused membership tier targeting casual riders' primary usage pattern.

### 2. 🚇 Commuter Benefits Campaign
Market cost-effectiveness and convenience of annual membership for daily commuting during weekdays.

### 3. 📈 Tiered Membership Options
Develop flexible, lower-priced membership tiers with set monthly rides as low-commitment entry points.

---

## 🛠️ Technical Implementation

### Data Sources
- **Period**: Q1 2019 & Q1 2020 (January - March)
- **Provider**: Motivate International Inc.
- **Files**: `Divvy_Trips_2019_Q1.csv` & `Divvy_Trips_2020_Q1.csv`

### Tools & Technologies
- **Data Analysis**: Python, Pandas
- **Visualization**: Chart.js
- **Presentation**: HTML5, Tailwind CSS, JavaScript
- **Data Processing**: CSV file combination, duplicate removal, data validation

### 📝 Complete Data Analysis Code

#### Data Import and Initial Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the datasets
df_2019_q1 = pd.read_csv('Divvy_Trips_2019_Q1.csv')
df_2020_q1 = pd.read_csv('Divvy_Trips_2020_Q1.csv')

# Display basic information about datasets
print("2019 Q1 Dataset Shape:", df_2019_q1.shape)
print("2020 Q1 Dataset Shape:", df_2020_q1.shape)
print("\n2019 Q1 Columns:", df_2019_q1.columns.tolist())
print("2020 Q1 Columns:", df_2020_q1.columns.tolist())
```

#### Data Cleaning and Preparation
```python
# Standardize column names between datasets
def standardize_columns(df, year):
    """Standardize column names for consistency"""
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

# Apply standardization
df_2019_q1_clean = standardize_columns(df_2019_q1.copy(), 2019)
df_2020_q1_clean = df_2020_q1.copy()

# Convert datetime columns
datetime_columns = ['started_at', 'ended_at']
for col in datetime_columns:
    df_2019_q1_clean[col] = pd.to_datetime(df_2019_q1_clean[col])
    df_2020_q1_clean[col] = pd.to_datetime(df_2020_q1_clean[col])

# Standardize member_casual values
df_2019_q1_clean['member_casual'] = df_2019_q1_clean['member_casual'].map({
    'Subscriber': 'member',
    'Customer': 'casual'
})
```

#### Key Data Transformations
```python
def add_calculated_columns(df):
    """Add calculated columns for analysis"""
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

# Apply transformations
df_2019_q1_clean = add_calculated_columns(df_2019_q1_clean)
df_2020_q1_clean = add_calculated_columns(df_2020_q1_clean)
```

#### Data Quality Checks and Cleaning
```python
def clean_data(df):
    """Remove invalid data and outliers"""
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
    print(f"Removed {initial_rows - final_rows} invalid records ({((initial_rows - final_rows) / initial_rows * 100):.2f}%)")
    
    return df

# Clean both datasets
df_2019_q1_final = clean_data(df_2019_q1_clean)
df_2020_q1_final = clean_data(df_2020_q1_clean)

# Combine datasets
df_combined = pd.concat([df_2019_q1_final, df_2020_q1_final], ignore_index=True)
print(f"Combined dataset shape: {df_combined.shape}")
```

#### Comprehensive Analysis Functions
```python
def analyze_ride_duration(df):
    """Analyze ride duration by user type"""
    duration_stats = df.groupby('member_casual')['ride_length'].agg([
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
    
    return duration_stats

def analyze_weekly_patterns(df):
    """Analyze usage patterns by day of week"""
    weekly_stats = df.groupby(['member_casual', 'day_name'])['ride_id'].count().reset_index()
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
        weekend_rides = weekly_pivot.loc[weekend_days, user_type].sum()
        weekday_rides = weekly_pivot.loc[weekday_days, user_type].sum()
        weekend_pct = (weekend_rides / (weekend_rides + weekday_rides)) * 100
        
        print(f"\n{user_type.title()} riders:")
        print(f"Weekend usage: {weekend_pct:.1f}%")
        print(f"Weekday usage: {100-weekend_pct:.1f}%")
    
    return weekly_pivot

def analyze_hourly_patterns(df):
    """Analyze usage patterns by hour of day"""
    hourly_stats = df.groupby(['member_casual', 'start_hour'])['ride_id'].count().reset_index()
    hourly_pivot = hourly_stats.pivot(index='start_hour', columns='member_casual', values='ride_id')
    
    # Find peak hours
    for user_type in ['casual', 'member']:
        peak_hour = hourly_pivot[user_type].idxmax()
        peak_count = hourly_pivot[user_type].max()
        print(f"{user_type.title()} peak hour: {peak_hour}:00 ({peak_count} rides)")
    
    return hourly_pivot

def analyze_seasonal_patterns(df):
    """Analyze usage patterns by month"""
    monthly_stats = df.groupby(['member_casual', 'month'])['ride_id'].count().reset_index()
    monthly_pivot = monthly_stats.pivot(index='month', columns='member_casual', values='ride_id')
    
    print("Monthly Usage Patterns:")
    print(monthly_pivot)
    
    return monthly_pivot
```

#### Execute Analysis
```python
# Run comprehensive analysis
print("="*50)
print("CYCLISTIC BIKE-SHARE ANALYSIS RESULTS")
print("="*50)

# Basic dataset statistics
print(f"Total rides analyzed: {len(df_combined):,}")
print(f"Date range: {df_combined['started_at'].min()} to {df_combined['started_at'].max()}")
print(f"Casual riders: {len(df_combined[df_combined['member_casual'] == 'casual']):,}")
print(f"Annual members: {len(df_combined[df_combined['member_casual'] == 'member']):,}")

print("\n" + "="*50)
duration_analysis = analyze_ride_duration(df_combined)

print("\n" + "="*50)
weekly_analysis = analyze_weekly_patterns(df_combined)

print("\n" + "="*50)
hourly_analysis = analyze_hourly_patterns(df_combined)

print("\n" + "="*50)
monthly_analysis = analyze_seasonal_patterns(df_combined)
```

#### Data Visualization Code
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_duration_comparison_chart():
    """Create ride duration comparison chart"""
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart of average duration
    duration_means = df_combined.groupby('member_casual')['ride_length'].mean()
    ax[0].bar(duration_means.index, duration_means.values, 
              color=['#3B82F6', '#10B981'], alpha=0.8)
    ax[0].set_title('Average Ride Duration by User Type', fontsize=14, fontweight='bold')
    ax[0].set_ylabel('Average Duration (minutes)')
    ax[0].set_xlabel('User Type')
    
    # Add value labels on bars
    for i, v in enumerate(duration_means.values):
        ax[0].text(i, v + 1, f'{v:.1f}min', ha='center', fontweight='bold')
    
    # Box plot for distribution
    df_combined.boxplot(column='ride_length', by='member_casual', ax=ax[1])
    ax[1].set_title('Ride Duration Distribution by User Type', fontsize=14, fontweight='bold')
    ax[1].set_ylabel('Ride Duration (minutes)')
    ax[1].set_xlabel('User Type')
    ax[1].set_ylim(0, 100)  # Limit y-axis for better visibility
    
    plt.tight_layout()
    plt.show()

def create_weekly_usage_chart():
    """Create weekly usage pattern chart"""
    weekly_data = df_combined.groupby(['member_casual', 'day_name'])['ride_id'].count().reset_index()
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
    plt.show()

def create_hourly_usage_chart():
    """Create hourly usage pattern chart"""
    hourly_data = df_combined.groupby(['member_casual', 'start_hour'])['ride_id'].count().reset_index()
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
        ax.axvspan(start, end, alpha=0.2, color='red', label='Commute Hours' if start == 7 else "")
    
    plt.tight_layout()
    plt.show()

# Generate all visualizations
create_duration_comparison_chart()
create_weekly_usage_chart()
create_hourly_usage_chart()
```

#### Export Results for Presentation
```python
def export_analysis_results():
    """Export key metrics for presentation"""
    results = {}
    
    # Duration analysis
    duration_stats = df_combined.groupby('member_casual')['ride_length'].agg(['mean', 'count'])
    results['casual_avg_duration'] = duration_stats.loc['casual', 'mean']
    results['member_avg_duration'] = duration_stats.loc['member', 'mean']
    results['duration_ratio'] = results['casual_avg_duration'] / results['member_avg_duration']
    
    # Weekly patterns
    weekly_stats = df_combined.groupby(['member_casual', 'is_weekend'])['ride_id'].count()
    
    # Calculate weekend percentage for each user type
    for user_type in ['casual', 'member']:
        weekend_rides = weekly_stats[user_type][True] if True in weekly_stats[user_type] else 0
        total_rides = weekly_stats[user_type].sum()
        results[f'{user_type}_weekend_pct'] = (weekend_rides / total_rides) * 100
    
    # Total rides
    results['total_rides'] = len(df_combined)
    results['casual_rides'] = len(df_combined[df_combined['member_casual'] == 'casual'])
    results['member_rides'] = len(df_combined[df_combined['member_casual'] == 'member'])
    
    return results

# Export results
analysis_results = export_analysis_results()
print("\nKey Metrics for Presentation:")
for key, value in analysis_results.items():
    if isinstance(value, float):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value:,}")
```

#### Summary Statistics
```python
def generate_summary_report():
    """Generate comprehensive summary report"""
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY - CYCLISTIC BIKE-SHARE ANALYSIS")
    print("="*60)
    
    total_rides = len(df_combined)
    casual_rides = len(df_combined[df_combined['member_casual'] == 'casual'])
    member_rides = len(df_combined[df_combined['member_casual'] == 'member'])
    
    print(f"📊 DATASET OVERVIEW:")
    print(f"   • Total rides analyzed: {total_rides:,}")
    print(f"   • Casual rider trips: {casual_rides:,} ({casual_rides/total_rides*100:.1f}%)")
    print(f"   • Member trips: {member_rides:,} ({member_rides/total_rides*100:.1f}%)")
    
    # Duration insights
    casual_avg = df_combined[df_combined['member_casual'] == 'casual']['ride_length'].mean()
    member_avg = df_combined[df_combined['member_casual'] == 'member']['ride_length'].mean()
    
    print(f"\n🚴‍♀️ RIDE DURATION INSIGHTS:")
    print(f"   • Casual rider average: {casual_avg:.1f} minutes")
    print(f"   • Member average: {member_avg:.1f} minutes")
    print(f"   • Casual riders take {casual_avg/member_avg:.1f}x longer rides")
    
    # Weekly patterns
    weekend_data = df_combined[df_combined['is_weekend'] == True]
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

# Generate the summary report
generate_summary_report()
```

---

## 📈 Expected Impact

| Metric | Projected Outcome |
|--------|------------------|
| Weekend Membership Conversion | 15-25% |
| Commuter Campaign ROI | 200-300% |
| Tiered Membership Uptake | 30-40% |

### Implementation Timeline
- **Q1**: Launch Weekend Warrior Membership
- **Q2**: Deploy Commuter Benefits Campaign  
- **Q3**: Introduce Tiered Membership Options

---

## 🎨 Interactive Presentation

This project includes a professional, interactive HTML presentation with:

- ✨ **Responsive Design**: Works on desktop and mobile
- 📊 **Live Charts**: Interactive data visualizations
- 🎯 **Navigation**: Keyboard shortcuts and button controls
- 🎭 **Animations**: Smooth slide transitions

### 🚀 How to View

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bhqmuhammad/cyclistic-bike-share-analysis.git
   ```

2. **Open the presentation**:
   ```bash
   cd cyclistic-bike-share-analysis
   open index.html  # or double-click the file
   ```

3. **Navigate through slides**:
   - Use arrow keys or spacebar
   - Click navigation buttons
   - 8 comprehensive slides covering the entire analysis

---

## 📁 Repository Structure

```
cyclistic-bike-share-analysis/
├── index.html                     # Interactive presentation deck
├── README.md                      # Project documentation
├── analysis.py                    # Complete Python analysis code
├── data_processing.py             # Data cleaning and transformation
├── visualizations.py              # Chart generation code
├── Case Study 1_How does a bike-share navigate speedy success.html
├── Case Study 1_How does a bike-share navigate speedy success.pdf
├── Divvy_Trips_2019_Q1.html      # Q1 2019 data visualization
├── Divvy_Trips_2020_Q1.html      # Q1 2020 data visualization
└── data/                          # Raw data files (if included)
    ├── Divvy_Trips_2019_Q1.csv
    └── Divvy_Trips_2020_Q1.csv
```

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

- **Ask**: Defining clear business questions and stakeholder needs
- **Prepare**: Data collection, organization, and validation
- **Process**: Data cleaning, transformation, and integrity checks
- **Analyze**: Statistical analysis and pattern identification
- **Share**: Professional presentation and data visualization
- **Act**: Actionable recommendations based on data insights

---

## 📄 Data Ethics & Licensing

- Data provided under [Divvy Data License Agreement](https://ride.divvybikes.com/data-license-agreement)
- No personally identifiable information (PII) used
- Analysis focused on aggregate usage patterns
- Compliant with data privacy regulations

---
