# Cyclistic Bike-Share Analysis: A Capstone Project

**Note:** This project is a case study for the Google Data Analytics Professional Certificate on Coursera. It demonstrates the completion of the data analysis process from ask to act, culminating in actionable business recommendations.

## 1. Introduction: The Scenario

This project follows the scenario of a junior data analyst working for Cyclistic, a fictional bike-share company in Chicago. The Director of Marketing believes the company's future success depends on maximizing the number of annual memberships.

The primary goal is to understand how casual riders and annual members use Cyclistic bikes differently. From these insights, we will derive a new marketing strategy to convert casual riders into paying annual members.

## 2. The Ask: The Business Task

The central business task is to answer the following question:

**"How do annual members and casual riders use Cyclistic bikes differently?"**

This question will guide our data-driven marketing recommendations to the Cyclistic executive team.

## 3. The Data Analysis Process

We followed the six steps of data analysis to structure our approach: Ask, Prepare, Process, Analyze, Share, and Act.

### Step 1: Ask

*   **Business Objective:** Increase the number of annual members by converting casual riders.
*   **Key Stakeholders:** The Cyclistic marketing team and company executives.
*   **Guiding Question:** What are the behavioral differences between casual riders and annual members?

### Step 2: Prepare

*   **Data Source:** We used historical trip data from Q1 2019 and Q1 2020. The data was provided by Motivate International Inc. under this [license](https://ride.divvybikes.com/data-license-agreement).
*   **Data Organization:** The data was provided in two separate CSV files (`Divvy_Trips_2019_Q1.csv` and `Divvy_Trips_2020_Q1.csv`).
*   **Data Cleaning:** The initial preparation involved combining the two files, checking for and removing duplicate entries, and ensuring data consistency across all columns.

### Step 3: Process

*   **Tools:** Python (with the Pandas library) was used for data cleaning, transformation, and analysis. The final visualizations were created using HTML, Tailwind CSS, and Chart.js.
*   **Data Transformation:**
    *   A `ride_length` column was created to calculate the duration of each trip.
    *   A `day_of_week` column was created to analyze usage patterns across the week.
    *   Rows with invalid `ride_length` (e.g., negative duration) were removed.

### Step 4 & 5: Analyze & Share (Key Findings)

Our analysis revealed two significant trends that differentiate casual riders from annual members:

*   **Finding 1: Casual riders take much longer rides than annual members.**
    *   Annual members typically use the bikes for shorter, more functional trips, with an average ride length of around 12 minutes.
    *   Casual riders, in contrast, take much longer, more leisurely rides, averaging around 36 minutes per trip.
*   **Finding 2: Usage patterns differ significantly throughout the week.**
    *   Annual members show consistent usage on weekdays, with peaks during morning and evening commute times. This suggests they primarily use the service for work-related travel.
    *   Casual riders show a massive spike in usage during the weekends (Saturday and Sunday), indicating they use the bikes for recreational or leisure activities.

#### Visualizations

*   This chart shows that casual riders' average trip duration is nearly 3x that of annual members.
*   This chart highlights the weekday commuter pattern for members versus the weekend leisure pattern for casual riders.

### Step 6: Act (Top Recommendations)

Based on the analysis, we propose the following top three recommendations to the marketing team:

1.  **Launch a "Weekend Warrior" Membership:** Create a discounted membership tier aimed specifically at weekend riders. This would appeal directly to the primary usage pattern of casual riders and offer them a cost-effective alternative to single-ride passes for their leisure trips.
2.  **Market Commuter Benefits:** For weekdays, marketing campaigns should highlight the cost-effectiveness and convenience of an annual membership for daily commuting. Campaigns could show a direct comparison of the cost of an annual membership versus paying for two single rides every workday.
3.  **Introduce Tiered Memberships:** Develop a flexible, lower-priced membership tier that offers a set number of rides per month. This could serve as a low-commitment entry point for casual riders who aren't ready for a full annual membership, acting as a stepping stone for future conversion.

## How to View This Project

This repository includes an interactive presentation deck created with HTML and Chart.js. To view it, download the repository and open the `index.html` file in a web browser.
