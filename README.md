# 🌊 Regional Ocean Temperature Forecasting

A comprehensive Deep Learning project for forecasting Sea Surface Temperature (SST) in the South China Sea and Western North Pacific. This project rigorously evaluates the impact of incorporating atmospheric variables (Wind, SLP, Precipitation) and advanced architectures (Multi-Task, Physics-Informed) against a baseline SST-only model.

## 📌 Project Overview
Accurate ocean forecasting is critical for climate monitoring and disaster mitigation. While traditional Numerical Ocean Prediction (NOP) models are computationally expensive, Data-Driven Deep Learning (DLOF) offers a faster alternative. This project investigates: **"Does incorporating atmospheric physical variables improve deep learning-based SST forecasting?"**

## 📂 Repository Structure
```text
ocean-forecasting/
├── data/               # Raw and processed NetCDF files (ignored in git)
├── notebooks/          # Jupyter Notebooks for exploration & experiments
├── reports/            # Figures, metrics.csv, and ablation results
├── src/                # Source code (if applicable)
├── requirements.txt    # Dependencies
└── README.md

📊 Datasets & Features
Target Variable: Sea Surface Temperature (SST) - NOAA OISST v2.1

Atmospheric Variables:

10m Wind (U/V components) - NCEP Reanalysis

Sea Level Pressure (SLP) - NCEP Reanalysis

Precipitation - CMAP (NOAA)

Time Period: 2017 - 2021

Test Set: Entire year of 2021 (Unseen during training)

Spatial Resolution: 0.5° (downsampled from 0.25°)

🧠 Model Architectures & Experiments
Persistence Baseline: Predicts tomorrow's SST using today's SST.

Residual CNN: A Convolutional Neural Network that predicts the change (Delta) in SST to prevent error accumulation.

Multi-Task Learning: Predicts SST and SLP simultaneously to capture coupled dynamics.

Physics-Informed CNN: Incorporates the Advection Equation as a custom loss function to enforce physical consistency.

🔬 Ablation Study Results (Test Year 2021)
To isolate the impact of each variable, all experiments used the exact same data splits, ocean masks, and 7-day historical windows.

Experiment	Input Variables	MAE (°C)	RMSE (°C)	Result
E1 (Baseline)	SST only	0.1210	0.1845	🏆 Best
E2	SST + Wind	0.1238	0.1871	Degraded
E3	SST + SLP	0.1234	0.1865	Degraded
E4	SST + Wind + SLP	0.1259	0.1883	Worst
E6	SST + Precipitation	0.1245	0.1871	Degraded
(Note: Multi-Task and Physics-Informed models were also tested but did not outperform the SST-only baseline).

💡 Scientific Insight
The results demonstrate that adding atmospheric variables does not guarantee improved accuracy for short-term (1-day) SST forecasting. SST exhibits high temporal autocorrelation (inertia). Atmospheric variables (like wind and pressure) are highly volatile and can introduce noise, confusing the model. This aligns with recent literature (e.g., Hao et al., 2025) emphasizing that data-driven models must be carefully designed and not just fed with maximum variables.

🚀 How to Run
Clone the repository and create a virtual environment.

Install dependencies: pip install -r requirements.txt

Download the raw datasets (NOAA OISST, NCEP, CMAP) into data/raw/.

Run the Jupyter Notebooks in the notebooks/ directory sequentially.

📈 Future Work
Explore longer forecast horizons (3-day, 7-day) using autoregressive rolling.

Incorporate ocean current data (e.g., from HYCOM or Copernicus).

Apply Attention mechanisms (e.g., Transformers) to handle long-term dependencies.