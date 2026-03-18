# Project Summary — NASA IMS Bearing Degradation Analysis with Python and Tableau

## Overview

This project analyses the **NASA IMS bearing run-to-failure dataset** using **Python** for preprocessing and **Tableau** for visualisation.

The raw dataset contains timestamped vibration signal files collected from bearing experiments. These raw files were transformed into structured analytical datasets by extracting vibration features such as **RMS, kurtosis, peak amplitude, standard deviation, and crest factor**.

The final output includes:

- **3 individual dashboards** for Test 1, Test 2, and Test 3
- **1 cross-test comparison dashboard**
- reusable Python preprocessing scripts
- processed CSV datasets for dashboarding and further analysis

---

## Objective

The objective of this project was to turn raw machine vibration data into meaningful dashboards that could help identify:

- bearing degradation trends over time
- dominant failure behaviour in each test
- differences between multiple run-to-failure experiments
- comparative severity across tests using feature-based analysis

---

## Dataset

The dataset used in this project is the **IMS Bearings dataset**, originally provided by the:

- **Center for Intelligent Maintenance Systems (IMS), University of Cincinnati**
- distributed through **NASA / Prognostics Center of Excellence (PCoE)**

The data consists of timestamp-based vibration files collected during bearing run-to-failure experiments.

---

## Tools Used

- **Python**
  - pandas
  - numpy
- **Tableau Public**
- **Excel** for quick file inspection and validation
- **GitHub** for project documentation and version control

---

## Project Workflow

### 1. Raw Data Inspection
The project began by understanding the folder structure, file naming format, and signal layout of the raw vibration files.

### 2. Python Preprocessing
Python scripts were developed to:
- read timestamp-named files
- parse timestamps
- calculate elapsed test duration
- extract vibration features
- generate both channel-level and bearing-level datasets

### 3. Feature Engineering
The following features were calculated:
- Mean
- Standard Deviation
- RMS
- Peak Absolute Value
- Minimum Value
- Maximum Value
- Kurtosis
- Crest Factor

### 4. Tableau Dashboarding
The processed bearing-level datasets were used to build:
- Test 1 dashboard
- Test 2 dashboard
- Test 3 dashboard
- Cross-test comparison dashboard

---

## Dashboard Outputs

### Test 1 Dashboard
Key pattern:
- **Bearing 3** showed the strongest late-stage degradation
- **Bearing 4** showed secondary elevation
- Test 1 produced the **highest max kurtosis**, indicating strong impulsive behaviour

### Test 2 Dashboard
Key pattern:
- **Bearing 1** was the dominant degradation case
- Test 2 had the **shortest duration**
- severe degradation became visible in a shorter operational window

### Test 3 Dashboard
Key pattern:
- **Bearing 3** was again the dominant degradation case
- Test 3 produced the **highest max RMS**
- it also ran for the **longest duration**

### Cross-Test Comparison Dashboard
The final dashboard compares all three tests using:
- test duration
- highest max RMS
- highest max kurtosis
- bearing severity by test
- RMS trends using **normalised test progress**

---

## Main Findings

Across the three IMS tests:

- **Test 3** had the highest overall max RMS
- **Test 1** had the highest overall max kurtosis
- **Test 3** had the longest duration
- **Test 2** reached strong degradation much faster than the others
- **Bearing 3** was dominant in Tests 1 and 3
- **Bearing 1** was dominant in Test 2

These findings show that degradation behaviour differed meaningfully across experiments, making cross-test comparison valuable.

---

## Skills Demonstrated

This project demonstrates skills in:

- data preprocessing with Python
- feature engineering from raw sensor data
- time-series analysis
- Tableau dashboard development
- comparative analytical thinking
- predictive maintenance storytelling
- portfolio-ready project documentation

---

## Why This Project Matters

This project is more than a dashboard exercise. It shows the full workflow of:
- reading messy real-world data
- transforming it into usable features
- building analytical outputs
- drawing interpretable conclusions from multiple experiments

It also demonstrates the ability to work on a predictive maintenance use case using engineering data rather than standard business datasets.

---

## Next Improvements

Possible future improvements include:
- anomaly threshold overlays
- more advanced vibration features
- predictive modelling on degradation progression
- more polished Tableau public presentation
- interactive portfolio integration

---

## Repository

This project is documented and version-controlled on GitHub, with:
- raw and processed data structure
- Python scripts
- Tableau dashboards
- README documentation
- dashboard screenshots
