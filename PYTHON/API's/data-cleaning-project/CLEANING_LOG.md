# Data Cleaning Log

## 1. Dataset Overview

- **Dataset:** `messy_sales.csv`
- **Original shape:** 16 rows and 8 columns
- **Purpose:** To improve data quality and make the dataset reliable for analysis.

- **Problems identified:**
  - Missing or placeholder values in `age` (3) and `amount` (1).
  - One invalid date: `2026-02-30`.
  - One exact duplicate row.
  - Invalid age value (`150`).
  - Inconsistent city-name capitalization.
  - Incorrect data formats, including currency symbols and text placeholders in numeric columns.

  ## 2. Missing Values

- **Age:** Invalid or missing ages were converted to missing values. Age 150 was treated as invalid. I used median imputation because the median is less affected by extreme values than the mean.
- **Amount:** The missing amount was filled with the median because unusually large sales could distort the mean.
- **Missing-value flag:** I created `age_was_missing` before imputation to record which ages were originally missing. This preserves information about missingness for later analysis.

## 3. Data Types and Invalid Values

- **Age:** I converted the age column to numeric using `pd.to_numeric(errors="coerce")`. Invalid text values became missing values. I treated age 150 as invalid and used median imputation for missing ages.
- **Amount:** I removed the rupee symbol and unwanted characters, then converted the amount column to numeric so that mathematical calculations could be performed.
- **Order date:** I converted the order-date column using `pd.to_datetime(errors="coerce")`. The invalid date `2026-02-30` became `NaT`, and I identified it as a parsing failure.

## 4. Categorical Data Normalization

- **Column:** `city`
- **Method:** I used `str.strip()` to remove leading and trailing spaces and `str.title()` to standardize capitalization.
- **Reason:** Inconsistent city names can cause the same city to be counted as separate categories during grouping and analysis.
- **Result:** The number of distinct city values decreased from 6 to 4 after normalization.

## 5. Outlier Detection and Decisions

- **Methods used:** IQR and z-score.
- **Age 150:** This age was implausible for the dataset, so I treated it as missing and replaced it with the median.
- **Amount 200000:** I kept this value because it could represent a legitimate large sale. It should be investigated before deciding whether to change or remove it.
- **Amount 50000:** I kept this value because it could also represent a legitimate transaction. It should be investigated before deciding whether to change or remove it.
- **Method comparison:** IQR and z-score use different criteria to detect outliers, so they may disagree. A value flagged by one method but not the other requires investigation rather than automatic removal.

## 6. Data Reshaping and Sales Summary

- **Pivot table:** I used `pivot_table()` to summarize total sales by city and category. This helps compare sales performance across cities and product categories.
- **Melt:** I used `melt()` to convert the `age` and `amount` columns from wide format into long format. The `metric` column stores the original column names, while `value` stores their values.
- **Purpose:** The pivot table supports grouped sales analysis, while the melted dataset provides a long-format structure that can be useful for visualization and further analysis.

## 7. Final Results

- **Row count:** Reduced from 16 to 15 after removing one exact duplicate.
- **Column count:** Increased from 8 to 9 after adding the `age_was_missing` flag.
- **cleaned_sales.csv:** Contains the cleaned dataset.
- **sales_long.csv:** Contains the reshaped data produced using `melt()`.
- **Original data:** The original `messy_sales.csv` file remains unchanged because the cleaned data was saved to a separate file.

If a column has 40% missing values, I would not immediately delete it or fill all missing values with the mean.

First, I would investigate why the values are missing. I would consider whether the missingness is MCAR, MAR, or MNAR, using available data and domain knowledge. For example, customers might deliberately avoid providing their ages.

Next, I would assess how important the column is to the business problem. If it is not useful, dropping the column may be reasonable. If it contains important information, I would consider retaining it.

For numerical data, I might use median imputation when appropriate, especially if the data contains extreme values. Other options include mean imputation, model-based imputation, or leaving values missing if the chosen analysis or model supports that. I could also add a missingness indicator to preserve information about which values were originally missing.

I would choose the approach based on the data, the likely missingness mechanism, and the analysis objective.

Finally, I would validate the result by checking distributions, comparing results before and after imputation, and assessing potential bias. I would document my decision and its limitations.

The goal is not simply to eliminate missing values, but to preserve useful information and produce reliable analysis.