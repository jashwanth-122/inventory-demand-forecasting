# Inventory Demand Forecasting & Reorder Optimization

An end-to-end supply chain analytics project that forecasts product demand and converts forecast results into actionable inventory recommendations such as safety stock and reorder points.

## Project Overview

The goal of this project is to build a complete demand forecasting and inventory optimization workflow using historical retail sales data.

The project covers:

Data Understanding and Cleaning

Exploratory Data Analysis (EDA)

Feature Engineering

Baseline Forecasting

Classical Time-Series Forecasting

LightGBM Forecasting

LSTM Deep Learning

Model Comparison

Inventory Optimization

SQL Business Analysis

Interactive Power BI Dashboard

## Business Problem

Retail businesses need to maintain enough inventory to meet customer demand while avoiding excess stock.

This project uses historical sales patterns to forecast future product demand and converts those forecasts into practical inventory recommendations.

The final outputs include:

Average Daily Demand

Forecast Uncertainty

Safety Stock

Reorder Point

Forecast Error Analysis

Item-Level Inventory Recommendations

## Dataset

The project uses the M5 retail forecasting dataset containing historical Walmart product sales, calendar information, and selling prices.

The dataset contains more than 56 million daily sales observations across 30,490 item-store combinations.

Because several raw dataset files are too large for GitHub's normal browser upload limits, the complete raw dataset is not stored in this repository.

## Technologies Used

Python

Pandas

NumPy

Scikit-learn

LightGBM

TensorFlow / Keras

Statsmodels

SQL

Power BI

Matplotlib

## Data Preparation

The raw sales, calendar, and pricing data were prepared for time-series forecasting.

Sales data was transformed into a structure suitable for model training and analysis.

Data quality checks were performed to identify missing values, duplicates, and other potential data issues.

## Feature Engineering

Time-series and business features were created to help the forecasting models understand historical demand patterns.

Important features included:

Sales Lag Features

Rolling Sales Averages

Selling Price

Day of Week

Calendar Information

Events and Holidays

Store Information

Product Information

These features allow the models to use both recent demand behavior and additional business information when forecasting future sales.

## Modeling Approach

### Baseline Model

A simple rolling-average forecast was created first to establish a benchmark.

The baseline provides a reference point for determining whether more advanced forecasting models actually improve prediction accuracy.

### Classical Time-Series Model

ETS was evaluated as a traditional statistical time-series forecasting approach.

This provided a comparison between classical forecasting techniques and machine-learning models.

### LightGBM

LightGBM was trained using engineered time-series, pricing, calendar, product, and store features.

The model was able to capture nonlinear relationships between historical demand and the engineered features.

### LSTM

A Long Short-Term Memory neural network was developed to explore deep-learning-based demand forecasting.

The LSTM was designed to learn sequential patterns from historical sales data.

## Model Evaluation

Four forecasting approaches were compared using MAE, RMSE, and WAPE.

LightGBM achieved the best performance with 34.4% WAPE on the common evaluation set.

LightGBM reduced forecast error by approximately 15% compared with the baseline model.

The forecasting approaches evaluated were:

Baseline Forecast

ETS Time-Series Model

LightGBM

LSTM

### Evaluation Metrics

MAE — Mean Absolute Error

RMSE — Root Mean Squared Error

WAPE — Weighted Absolute Percentage Error

These metrics measure forecast errors from different perspectives and make it possible to compare model performance consistently.

## Inventory Optimization

After selecting the forecasting approach, forecast outputs were converted into inventory recommendations.

Inventory recommendations were generated for more than 30,000 item-store combinations.

### Average Daily Demand

Average daily demand represents the expected number of units required per day based on historical and forecast demand.

### Safety Stock

Safety stock provides additional inventory to protect against unexpected demand and forecasting uncertainty.

A 95% service-level target was used for the inventory recommendation framework.

### Reorder Point

The reorder point represents the inventory level at which a new order should be placed.

It combines expected demand during the assumed lead time with safety stock to reduce the risk of running out of inventory.

## Power BI Dashboard

An interactive Power BI dashboard was developed to present the final forecasting and inventory recommendations.

![Power BI Inventory Dashboard](Power%20BI%20Dashboard.png)

The dashboard includes:

Average Daily Demand

Average Safety Stock

Average Reorder Point

Item ID Filtering

Top 20 Items by Forecast Error

Inventory Recommendations Table

Users can select an individual item using the Item ID slicer and dynamically view its demand, safety stock, reorder point, forecast error, and inventory recommendations.

## Project Workflow

Data Understanding

↓

Data Cleaning & EDA

↓

Feature Engineering

↓

Baseline Forecasting

↓

ETS, LightGBM and LSTM

↓

Model Evaluation & Comparison

↓

Inventory Optimization

↓

Power BI Dashboard

## Repository Contents

01_data_understanding.py — Initial dataset exploration

02_eda.py — Exploratory data analysis

02b data cleaning checks .PY — Data cleaning and quality checks

03 feature engineering . PY — Time-series feature engineering

04 baseline model . PY — Baseline demand forecasting

05_sql_business_analysis.py — SQL business analysis

06 classical timeseries . PY — Classical time-series forecasting

07 lightgbm model . PY — LightGBM forecasting model

08 lstm model . PY — LSTM deep-learning model

09 model comparison . PY — Model evaluation and comparison

10 inventory optimization . PY — Safety stock and reorder point calculations

Inventory_Demand_Forecast_Dashboard.pbix — Interactive Power BI dashboard

Power BI Dashboard.png — Power BI dashboard preview

calendar.csv — Calendar information used in the forecasting pipeline

## Key Results

Processed more than 56 million sales observations across 30,490 item-store combinations.

Compared four forecasting approaches including Baseline, ETS, LightGBM, and LSTM.

LightGBM achieved the best performance with 34.4% WAPE.

Reduced forecast error by approximately 15% compared with the baseline model.

Generated safety stock and reorder-point recommendations for more than 30,000 item-store combinations.

Developed an interactive Power BI dashboard for item-level inventory analysis.

## Key Outcome

This project demonstrates an end-to-end data science workflow that moves beyond simply predicting future demand.

The forecasting results are translated into practical inventory decisions that help determine how much inventory should be maintained and when products should be reordered.

The project combines data preparation, exploratory analysis, feature engineering, statistical forecasting, machine learning, deep learning, model evaluation, inventory optimization, SQL, and business intelligence into a single end-to-end supply chain analytics solution.

## Author

**Jashwanth Alasyam**

B.S. Computer Science — Data Science
