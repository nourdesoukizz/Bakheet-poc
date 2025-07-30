import sys
import os
import traceback

# Add current directory to path
sys.path.append('.')
sys.path.append('algorithms')

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

print("\n" + "="*50)
print("TESTING IMPORTS")
print("="*50)

# Test each import individually
algorithms_to_test = [
    ('SARIMA', 'algorithms.classical.sarima', 'SARIMAForecasting'),
    ('SBA', 'algorithms.classical.sba_forecasting', 'SBAForecasting'),
    ('Random Forest', 'algorithms.machine_learning.random_forest', 'RandomForestForecasting'),
    ('XGBoost', 'algorithms.machine_learning.xgboost', 'XGBoostForecasting'),
    ('LSTM', 'algorithms.deep_learning.lstm', 'LSTMForecasting'),
    ('Prophet', 'algorithms.time_series.prophet', 'ProphetForecasting')
]

for name, module_path, class_name in algorithms_to_test:
    print(f"\n--- Testing {name} ---")
    try:
        print(f"Importing {module_path}")
        module = __import__(module_path, fromlist=[class_name])
        print(f"Getting class {class_name}")
        algorithm_class = getattr(module, class_name)
        print(f"✅ {name} import successful!")
        
        # Try to instantiate
        print(f"Instantiating {class_name}")
        instance = algorithm_class()
        print(f"✅ {name} instantiation successful!")
        
    except Exception as e:
        print(f"❌ {name} failed:")
        print(f"Error: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

print("\n" + "="*50)
print("TESTING DATA LOADING")
print("="*50)

try:
    import pandas as pd
    data_path = 'data/Sample_FiveYears_Sales_SpareParts.xlsx'
    print(f"Checking if data file exists: {data_path}")
    print(f"File exists: {os.path.exists(data_path)}")
    
    if os.path.exists(data_path):
        print("Attempting to read Excel file...")
        xl_file = pd.ExcelFile(data_path)
        print(f"✅ Excel file loaded successfully!")
        print(f"Sheet names: {xl_file.sheet_names}")
    else:
        print("❌ Data file not found!")
        print("Current directory contents:")
        print(os.listdir('.'))
        if os.path.exists('data'):
            print("Data directory contents:")
            print(os.listdir('data'))
        
except Exception as e:
    print(f"❌ Data loading failed: {str(e)}")
    traceback.print_exc()
