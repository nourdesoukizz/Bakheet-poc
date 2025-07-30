# Bakheet Forecasting POC

A proof of concept for forecasting spare parts sales using various time series forecasting methods.

## Project Structure

```
bakheet-forecasting-poc/
├── data/
│   └── Sample_FiveYears_Sales_SpareParts.xlsx
├── algorithms/
│   ├── classical/       # Classical statistical models
│   ├── machine_learning/ # ML-based forecasting models
│   ├── deep_learning/   # LSTM and other DL models
│   └── time_series/     # Prophet and other specialized models
├── streamlit_app/
│   ├── app.py           # Main Streamlit application
│   ├── components/      # UI components
│   └── results/         # Output storage
├── outputs/             # Model outputs and visualizations
├── requirements.txt     # Package dependencies
└── README.md           # This file
```

## Environment Setup

### Prerequisites
- Python 3.10 (recommended for compatibility)
- Conda (recommended for macOS installations)

### Setup Instructions for macOS

1. **Create and activate a conda environment**:
   ```bash
   conda create -n bakheet-env python=3.10
   conda activate bakheet-env
   ```

2. **Install Prophet via conda** (recommended for macOS):
   ```bash
   conda install -c conda-forge prophet
   ```

3. **Install other dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Setup Instructions for Windows/Linux

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv bakheet_env
   # On Windows
   bakheet_env\Scripts\activate
   # On Linux
   source bakheet_env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **For Prophet on Windows** (if installation fails):
   ```bash
   pip install pystan==2.19.1.1
   pip install prophet
   ```

## Running the Application

```bash
cd streamlit_app
streamlit run app.py
```

## Troubleshooting

### macOS Specific Issues
- For M1/M2 Macs, TensorFlow is installed using `tensorflow-macos` and `tensorflow-metal` packages
- If Prophet installation fails with pip, use conda: `conda install -c conda-forge prophet`

### Python Version Compatibility
- This project requires Python 3.10 for optimal compatibility with all dependencies
- Using Python 3.13+ may cause issues with certain packages