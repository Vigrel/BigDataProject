
---

# Exploratory Data Analysis of Climate and Land-Use Data 🌍

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/downloads/release/python-390/)
[![Dask](https://img.shields.io/badge/Dask-Parallel%20Processing-orange)](https://www.dask.org/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green)](https://scikit-learn.org/stable/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)

This repository contains the code and documentation for a project exploring the relationship between climate change, land-use practices, and natural disasters. The study emphasizes Brazil while leveraging global datasets to provide insights into disaster trends and environmental factors.

## 📋 Summary

- **Objective**: Analyze trends and patterns of natural disasters in relation to environmental factors.
- **Datasets**:
  - [FAO Land Cover and Forest Area](https://www.fao.org/faostat/en/#data/RL) (1992-2020)
  - [EM-DAT Disaster Database](https://www.emdat.be/) (2023)
- **Techniques**:
  - Data cleaning and normalization
  - Exploratory data analysis (descriptive statistics and visualizations)
  - Predictive modeling using machine learning
  - Regional analysis focusing on Brazil

## 🛠 Project Structure

```
├── data/
│   ├── raw/                # Raw datasets
│   ├── interim/            # Intermediate datasets
│   └── processed/          # Final processed datasets
├── main.py                 # Main script for data processing and analysis
├── ANALISE_EXPLORATORIA.ipynb  # Jupyter Notebook for analysis and visualizations
├── Exploratory Data Analysis of Climate and Land-Use Data.pdf  # Final report
└── README.md               # Project documentation
```

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- Libraries: Dask, Pandas, NumPy, Matplotlib, Seaborn

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:
   ```bash
   python main.py
   ```

4. Explore the results in the output files:
   - Normalized data: `data/interim/dataConcat_silver.csv`
   - Processed data: `data/processed/dataConcat_gold.csv`

### Optional: Analyze in Jupyter Notebook
Open the `ANALISE_EXPLORATORIA.ipynb` file to explore the analysis and visualizations interactively.

## 📝 Key Findings

- **Increasing Disaster Frequency**: A clear trend of increasing natural disasters was observed, with a rate of 4.09 events/year (R²=0.37, p=0.0003).
- **Brazil Focus**: The analysis identified deforestation rates and forest area as critical predictors for temperature changes.
- **Best Predictive Model**: Random Forest achieved the best R² score with minimal prediction error.

## 🧠 Conclusions

The findings emphasize the importance of regional environmental policies and climate resilience strategies. Data science plays a crucial role in deriving actionable insights for sustainable decision-making.

## 👥 Contributors

- [@Vigrel](https://github.com/vinicius-eller) - Vinicius Grando Eller
- [@FabricioNL](https://github.com/FabricioNL) - Fabricio Neri Lima
- [@isabellemm](https://github.com/isabellemm) - Isabelle Moschini Murollo

## 💻 Languages Used

![Jupyter Notebook](https://img.shields.io/badge/Jupyter%20Notebook-91.2%25-yellow?logo=jupyter)
![Python](https://img.shields.io/badge/Python-8.8%25-blue?logo=python)

## ⚙️ Suggested Workflows

Based on the tech stack, the following workflows are recommended:
- **[Django](https://github.com/actions/starter-workflows/blob/main/ci/django.yml)**: Build and test a Django project.
- **[Python Package using Anaconda](https://github.com/actions/starter-workflows/blob/main/ci/python-package-conda.yml)**: Create and test a Python package with Anaconda.
- **[Python Package](https://github.com/actions/starter-workflows/blob/main/ci/python-package.yml)**: Create and test a Python package on multiple versions.

---
