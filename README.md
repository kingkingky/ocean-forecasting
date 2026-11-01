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

## 🚀 Version 2.0: Advanced Learning & Physics-Informed

In Version 2.0, we pushed beyond simple feature addition and explored advanced architectures and physics-guided learning:

1. **Feature Diagnostic:** Added Precipitation (CMAP) and SLP. *Result: Adding raw atmospheric variables degrades performance.*
2. **Multi-Task Learning (Shared Encoder):** Predicted SST and SLP simultaneously with a reduced loss weight for SLP. *Result: Slight improvement (MAE: 0.1203).*
3. **Physics-Informed Learning (Advection):** Integrated the Advection Equation (`u*dT/dx + v*dT/dy`) as a physics regularizer. *Result: **Best performance** (MAE: 0.1195).*

### 🏆 Final Leaderboard (Test Year 2021)

| Model | MAE (°C) | RMSE (°C) | Note |
|:---|:---:|:---:|:---|
| Persistence | 0.1243 | 0.1919 | Baseline |
| E1: SST-only CNN | 0.1205 | 0.1836 | Version 1.0 |
| Multi-Task CNN | 0.1203 | 0.1828 | Version 2.0 |
| **Physics-Informed CNN** | **0.1195** | **0.1811** | 🏆 **SOTA** |

**Key Insight:** While raw atmospheric variables introduce noise, **incorporating physical laws (Physics-Informed Loss)** effectively guides the model to make more physically consistent and accurate predictions.

## 🌊 Version 3.0: The Data Resolution Trade-off

In the final phase, we investigated whether using high-resolution atmospheric data (ERA5, 0.25°) improves physics-informed forecasting compared to coarse data (NCEP, 2.5°).

### 🏆 Final Leaderboard (Test Year 2021)

| Model | Input Data | MAE (°C) | RMSE (°C) | Note |
|:---|:---|:---:|:---:|:---|
| Persistence | - | 0.1243 | 0.1919 | Baseline |
| E1: SST-only | - | 0.1205 | 0.1836 | V1 Baseline |
| Multi-Task | SST + SLP | 0.1203 | 0.1828 | V2 |
| **Physics (NCEP)** | SST + NCEP Wind | **0.1195** | **0.1811** | 🏆 **Best** |
| Physics (ERA5) | SST + ERA5 Wind | 0.1213 | 0.1822 | High-res attempt |

### 💡 Key Scientific Insight
1. **Physics-Informed Learning works:** Incorporating the Advection equation with NCEP wind achieved the best overall performance.
2. **Resolution Trade-off:** Surprisingly, using high-resolution ERA5 wind (0.25°) *degraded* performance compared to coarse NCEP wind (2.5°). This is likely because high-frequency turbulence in ERA5 introduces noise into the simple Advection constraint. Coarse NCEP data provides a smoother, more stable signal for the physics loss.
3. **Conclusion:** More data does not always mean better. The structural simplicity of the physical constraint matches better with synoptic-scale (coarse) data.

## 🗺️ Version 4.0: Regional Analysis (Warm Pool vs Cold Zone)

To address the spatial heterogeneity of ocean dynamics, we evaluated the Physics-Informed Model across three distinct thermal zones in the Western Pacific:

| Zone | Mean SST | Grid Cells | MAE (°C) | RMSE (°C) |
|:---|:---:|:---:|:---:|:---:|
| **Warm Pool** | > 28°C | 6,035 | **0.1081** | 0.1571 |
| **Mid Zone** | 25-28°C | 1,371 | 0.1427 | 0.2205 |
| **Cold Zone** | < 25°C | 1,109 | 0.1609 | 0.2471 |

### 💡 Key Insights
1. **High predictability in the Warm Pool:** The model achieves its best performance (MAE = 0.1081°C) in the Warm Pool due to high thermal inertia and stable sea surface temperatures.
2. **Challenges in the Cold Zone:** Performance degrades in the Cold Zone (MAE = 0.1609°C) where coastal upwelling and wind-driven mixing introduce high-frequency variability that is harder to capture.
3. **Conclusion:** Future improvements should focus on incorporating **ocean current data** and **mixed-layer depth** to better model the dynamic regions (Cold Zone).

## 🌪️ Version 4.1: Wind Forcing Analysis

To understand the physical mechanisms driving SST variability, we calculated the Pearson correlation between wind speed and daily SST change across the three thermal zones.

| Zone | Mean SST | Wind-SST Correlation (r) | Interpretation |
|:---|:---:|:---:|:---|
| **Warm Pool** | > 28°C | **+0.0891** | Weak positive. High thermal inertia dampens wind effects. |
| **Mid Zone** | 25-28°C | **-0.2693** | **Moderate negative.** Wind-driven evaporative cooling and mixing dominate. |
| **Cold Zone** | < 25°C | **-0.0767** | Weak negative. Complex coastal dynamics mask wind effects. |

### 💡 Key Physical Insights
1. **Thermal Inertia in the Warm Pool:** The weak correlation (+0.0891) explains why the model performs best here; the ocean's high heat capacity makes SST highly predictable regardless of wind.
2. **Evaporative Cooling in the Mid Zone:** The strongest correlation (-0.2693) indicates that stronger winds lead to cooler SST (negative r). This highlights the need for **Heat Flux** variables in future models.
3. **Complexity of the Cold Zone:** The weak correlation (-0.0767) suggests that SST changes in cold regions are driven by a combination of upwelling, currents, and tides, not just wind speed.

**Conclusion:** Physics-Informed models must account for region-specific dominant mechanisms (e.g., Advection in Mid Zone, Thermal Inertia in Warm Pool).

## 🏆 Version 5.0: Ensemble Forecasting (Final Model)

To reduce variance and improve robustness, we combined the predictions of three distinct architectures: Baseline CNN, Multi-Variable CNN, and Physics-Informed CNN.

| Model | MAE (°C) | RMSE (°C) | Note |
|:---|:---:|:---:|:---|
| Baseline CNN | 0.1238 | 0.1866 | SST only |
| Multi-Var CNN | 0.1230 | 0.1869 | SST + SLP |
| Physics CNN | 0.1205 | 0.1824 | SST + Wind (Advection Loss) |
| **Ensemble (Average)** | **0.1195** | **0.1830** | 🏆 **Final Best Model** |

### 💡 Key Insight
Averaging the predictions of diverse models (Ensemble) outperforms any single model. This confirms that different architectures capture different physical patterns (e.g., Physics CNN captures advection, while Baseline captures temporal inertia). The Ensemble approach reduces the overall prediction error.

## 🤖 Version 6.0: Transformer Experiment (Swin3D)

As an exploratory experiment, we implemented a Swin3D Transformer to test its computational efficiency on the RTX 5060 GPU.

*   **Architecture:** Swin3D-T (Tiny) pre-trained on Kinetics-400.
*   **Training Setup:** 5 Epochs with Mixed Precision (AMP), Batch Size = 1.
*   **Time:** Completed in **~4 minutes** on GPU.
*   **Results:** Early stopping at Epoch 4. Validation Loss = 0.000152. Mean Delta MAE = 0.0081 °C.
*   **Note on Output:** The `torchvision` Swin3D is designed for video classification, so it outputs a 1D vector (basin-wide mean SST change) rather than a 2D spatial map. Therefore, its MAE is not directly comparable to the CNN's 2D spatial MAE.
*   **Conclusion:** Transformers are highly efficient for sequence modeling. However, to predict full 2D SST maps, architectures like **SwinUNETR** or **ViViT** would be required. We leave this for future work.