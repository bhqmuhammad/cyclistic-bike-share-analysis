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

### Data Transformations
```python
# Key columns created during analysis
ride_length = end_time - start_time  # Trip duration calculation
day_of_week = extract_day(start_time)  # Weekly pattern analysis
