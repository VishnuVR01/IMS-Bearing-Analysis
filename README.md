NASA IMS Bearing Degradation Analysis using Python and Tableau

This README has sections in this order:
Project Title
Project Overview
Dataset Source
Problem Statement
Tools Used
Project Workflow
Python Feature Engineering
Dashboard Outputs
Cross-Test Comparison Insights
Repository Structure
How to Run the Project
Key Learnings
Future Improvements

# NASA IMS Bearing Degradation Analysis with Python and Tableau

This project analyses the **NASA IMS bearing run-to-failure dataset** using **Python** and **Tableau**.  
Raw vibration snapshot files were processed into feature-based datasets using metrics such as **RMS, kurtosis, peak amplitude, standard deviation, and crest factor**.

The project includes:

- **3 individual dashboards** for IMS **Test 1**, **Test 2**, and **Test 3**
- **1 cross-test comparison dashboard**
- a **Python feature extraction pipeline**
- processed CSV outputs for reuse and further analysis

---
For a quick overview, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).
---
## Project Objective

The goal of this project was to turn raw bearing vibration files into meaningful analytical outputs that can be used to monitor degradation trends and compare failure behaviour across multiple run-to-failure experiments.

This project was built to demonstrate:

- data preprocessing from raw text-based sensor files
- feature engineering for vibration analysis
- dashboard design in Tableau
- time-series trend interpretation
- cross-test comparison using normalised progress

---
## Dashboard Previews

### Test 1 Dashboard
![Test 1 Dashboard](docs/README_images/test1_dashboard.png)

### Test 2 Dashboard
![Test 2 Dashboard](docs/README_images/test2_dashboard.png)

### Test 3 Dashboard
![Test 3 Dashboard](docs/README_images/test3_dashboard.png)

### Cross-Test Comparison Dashboard
![Cross-Test Comparison Dashboard](docs/README_images/cross_test_dashboard.png) 

---
## Dataset Source

The dataset used in this project is the **IMS Bearings dataset**, originally provided by the:

- **Center for Intelligent Maintenance Systems (IMS), University of Cincinnati**
- distributed through **NASA / Prognostics Center of Excellence (PCoE)**
- official link https://data.nasa.gov/dataset/ims-bearings 
This is a well-known **run-to-failure bearing dataset** used in predictive maintenance and condition monitoring studies.


---

## Problem Statement

Each IMS test contains a sequence of timestamped vibration files captured during a bearing run-to-failure experiment.  
The raw files are not directly suitable for dashboarding, so the main challenge was to:

1. read and interpret the raw text files
2. extract meaningful vibration features
3. create clean analysis-ready datasets
4. build dashboards to identify degradation behaviour
5. compare patterns across all three tests

---

## Tools Used

- **Python**
  - pandas
  - numpy
- **Tableau Public**
- **Excel** for quick validation and inspection
- **GitHub** for project versioning and portfolio presentation

---

## Project Workflow

### 1. Raw Data Understanding
The raw dataset consists of timestamp-named vibration files such as:

- `2003.10.22.12.06.24`
- `2004.02.12.10.32.39`
- `2004.03.04.09.27.46`

Each file contains vibration readings captured at a specific time snapshot.

### 2. Feature Extraction with Python
A Python script was created to:

- read all valid timestamp files
- parse timestamps from filenames
- calculate elapsed test time
- compute vibration features for each channel
- aggregate channel-level data into bearing-level data

### 3. Processed Outputs
The pipeline produces:

- channel-level feature datasets
- bearing-level feature datasets
- combined all-tests datasets
- processing error log

### 4. Dashboard Development
Using Tableau, four dashboards were built:

- **Dashboard 1 — Test 1**
- **Dashboard 2 — Test 2**
- **Dashboard 3 — Test 3**
- **Dashboard 4 — Cross-Test Comparison**

---

## Python Feature Engineering

The following features were extracted from the raw vibration signals:

- **Mean**
- **Standard Deviation**
- **RMS**
- **Peak Absolute Value**
- **Minimum Value**
- **Maximum Value**
- **Kurtosis**
- **Crest Factor**

### Why these features matter
- **RMS** helps measure overall vibration severity
- **Kurtosis** helps detect impulsive / shock-like behaviour
- **Peak amplitude** highlights extreme spikes
- **Crest factor** gives a peak-to-energy relationship

These features help translate raw sensor readings into meaningful degradation indicators.

---

## Key Terms Explained

### Bearing
A bearing is a machine component that supports rotating motion and reduces friction between moving parts.

**In simple terms:**  
A bearing helps a shaft or rotating part move smoothly without too much friction or damage.

---

### Run-to-Failure
Run-to-failure means the machine or component is allowed to operate until a fault becomes severe or failure occurs.

**In simple terms:**  
The test keeps running until the bearing shows clear failure behaviour.

---

### Vibration Signal
A vibration signal is the recorded motion or oscillation of a machine part over time.

**In simple terms:**  
It is the raw sensor data that tells us how much the bearing is shaking.

---

### RMS (Root Mean Square)
RMS is a measure of the overall energy or magnitude of the vibration signal.

**In simple terms:**  
RMS tells us how strong the vibration is overall. Higher RMS usually means stronger vibration severity.

---

### Kurtosis
Kurtosis measures how extreme or spiky the signal is compared with a normal pattern.

**In simple terms:**  
Kurtosis helps detect shocks, impacts, or sudden abnormal spikes in vibration.

---

### Peak Amplitude
Peak amplitude is the highest absolute vibration value recorded in the signal.

**In simple terms:**  
It shows the biggest vibration spike in that snapshot.

---

### Standard Deviation
Standard deviation measures how spread out the vibration values are around the average.

**In simple terms:**  
It shows how much the vibration is fluctuating.

---

### Crest Factor
Crest factor is the ratio between the peak value and the RMS value.

**In simple terms:**  
It compares the biggest spike to the overall vibration level. A high crest factor can suggest sharp impacts or fault-like behaviour.

---

### Bearing-Level Features
Bearing-level features are summary metrics created for each bearing at each time step.

**In simple terms:**  
Instead of using all raw vibration values, we convert them into easier-to-analyse summary numbers like RMS and kurtosis.

---

### Channel-Level Features
Channel-level features are summary metrics calculated separately for each raw sensor channel.

**In simple terms:**  
These are feature values calculated directly from each sensor column before grouping them by bearing.

---

### Elapsed Hours
Elapsed hours represent how much time has passed since the beginning of the test.

**In simple terms:**  
It tells us where we are in the test timeline.

---

### Normalised Progress
Normalised progress scales each test from 0% to 100%, regardless of total duration.

**In simple terms:**  
It helps compare tests fairly even if one test lasted much longer than another.

---

## Test-Level Dashboard Summary

### Dashboard 1 — Test 1
Key observations:
- **Bearing 3** showed the strongest late-stage increase in RMS
- **Bearing 4** showed secondary elevation
- Test 1 recorded the **highest overall kurtosis** across the three tests

### Dashboard 2 — Test 2
Key observations:
- **Bearing 1** showed the strongest degradation behaviour
- Test 2 had the **shortest duration**
- Degradation became visible more quickly than in Tests 1 and 3

### Dashboard 3 — Test 3
Key observations:
- **Bearing 3** showed the highest vibration severity in the test
- Test 3 recorded the **highest max RMS**
- It also ran for the **longest duration**

### Dashboard 4 — Cross-Test Comparison
The comparison dashboard highlights:
- longest test duration
- highest max RMS
- highest max kurtosis
- dominant bearing by test
- RMS trends across tests using **normalised progress**

---

## Main Findings

Across the three tests:

- **Test 3** had the **highest overall max RMS**
- **Test 1** had the **highest overall max kurtosis**
- **Test 3** ran the longest
- **Test 2** reached strong degradation in a much shorter time window
- **Bearing 3** was the dominant degradation case in **Tests 1 and 3**
- **Bearing 1** was dominant in **Test 2**

This shows that the degradation pattern was **not identical across tests**, which makes cross-test comparison valuable.

---

## Repository Structure

```text
IMS-Bearing-Analysis/
├── raw_data/
│   ├── 1st_test/
│   ├── 2nd_test/
│   └── 3rd_test/
├── processed_data/
│   ├── ims_1st_test_bearing_features.csv
│   ├── ims_1st_test_channel_features.csv
│   ├── ims_2nd_test_bearing_features.csv
│   ├── ims_2nd_test_channel_features.csv
│   ├── ims_3rd_test_bearing_features.csv
│   ├── ims_3rd_test_channel_features.csv
│   ├── ims_all_tests_bearing_features.csv
│   ├── ims_all_tests_channel_features.csv
│   └── ims_processing_errors.csv
├── scripts/
│   ├── ims_all_tests_feature_extraction.py
│   └── ims_2nd_test_feature_extraction.py
├── tableau/
│   ├── Test 1 Workbook.twb
│   ├── Test 2 Workbook.twb
│   ├── Test 3 Workbook.twb
│   └── Cross-Test Comparison Workbook.twb
├── docs/
│   ├── README_images/
│   └── Readme Document for IMS Bearing Data.pdf
├── README.md
├── requirements.txt
└── .gitignore
