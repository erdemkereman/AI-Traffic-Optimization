
# AI Traffic Optimization

Machine Learning-Based Traffic Congestion Prediction and Intelligent Signal Optimization

## 1. Project Overview

This project investigates whether machine learning can improve traffic signal timing under different traffic conditions.

A Random Forest Regression model is used to estimate vehicle waiting times for alternative green-light allocations.

The predicted waiting times are then used to select a signal timing configuration.

All experiments are based on synthetic traffic data and a simplified traffic simulation.

## 2. Objectives

- Generate synthetic traffic scenarios.
- Analyze traffic patterns.
- Simulate fixed and adaptive signal timing.
- Train Random Forest regression models.
- Optimize green-light durations using ML predictions.
- Compare different signal timing strategies.
- Generate an automated analysis report.

## 3. Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Git and GitHub
- Mistral AI API (integration attempted)

## 4. Project Structure

```text
AI-Traffic-Optimization/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── data_dictionary.md
│   ├── simulation_rules.md
│   └── ai_traffic_analysis_report.md
├── results/
│   ├── figures/
│   └── models/
├── src/
│   ├── analysis/
│   ├── data_generation/
│   ├── llm/
│   ├── models/
│   └── simulation/
├── main.py
└── README.md
```

## 5. Methodology

### Data Generation

The project uses 720 synthetic traffic scenarios.

Traffic conditions are represented through features such as vehicle counts, time-related variables, weather conditions and road capacity.

### Traffic Simulation

A simplified simulation estimates waiting times under different signal timing configurations.

The available green-light time is distributed between the main road and the side road.

### Machine Learning

Random Forest Regression is used to predict waiting times.

The optimization dataset contains 25,200 configurations generated from 720 scenarios and 35 candidate green-light allocations per scenario.

The optimization model is evaluated using 144 held-out scenarios.

### Signal Optimization

Four approaches are compared:

1. Fixed signal timing
2. Adaptive signal timing
3. ML-based signal timing
4. Simulation-derived optimum

The ML approach evaluates candidate green-light allocations and selects the configuration with the lowest predicted waiting time.

## 6. Experimental Results

| Method | Average Waiting Time |
|---|---:|
| Fixed | 16.746 seconds |
| Adaptive | 16.073 seconds |
| ML-based | 15.933 seconds |
| Simulation optimum | 15.844 seconds |

The ML-based approach reduced average waiting time by approximately **4.86%** compared with fixed signal timing.

The average difference between the ML-based solution and the simulation optimum was **0.089 seconds**.

These results apply only to the experimental simulation environment.

## 7. Installation

Clone the repository:

```bash
git clone https://github.com/erdemkereman/AI-Traffic-Optimization.git
cd AI-Traffic-Optimization
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required libraries:

```powershell
python -m pip install pandas numpy scikit-learn matplotlib joblib python-dotenv
```

## 8. Running the Project

Run the following commands from the project root.

Generate traffic scenarios:

```powershell
python -m src.data_generation.generate_traffic
```

Preprocess the data:

```powershell
python -m src.analysis.preprocess_traffic
```

Generate the optimization dataset:

```powershell
python -m src.models.generate_optimization_dataset
```

Train the optimization model:

```powershell
python -m src.models.train_optimization_model
```

Compare optimization strategies:

```powershell
python -m src.models.compare_ml_optimization
```

Generate the analysis report:

```powershell
python -m src.llm.generate_traffic_report
```

The report is saved to:

`docs/ai_traffic_analysis_report.md`

## 9. Mistral AI Integration

Mistral AI was considered as an optional component for generating natural-language interpretations of optimization results.

An API integration test was implemented using Python.

However, the API returned HTTP 429 (Rate limit exceeded), preventing the completion of the LLM-based analysis.

The final report is therefore generated locally using Python and Pandas.

The ML optimization pipeline does not depend on Mistral AI.

## 10. Limitations

- Traffic data is synthetic.
- The simulation simplifies real-world traffic behavior.
- The ML model has not been validated on real traffic measurements.
- Improvements observed in simulation do not guarantee equivalent real-world performance.
- Mistral-based report generation was not completed due to API limitations.

## 11. Conclusion

The project demonstrates how Random Forest Regression can be used to support traffic signal timing decisions.

Within the simulation, ML-based optimization achieved lower average waiting times than fixed and adaptive timing strategies.

Future work could include real traffic data, more realistic intersection simulations and additional optimization algorithms.
