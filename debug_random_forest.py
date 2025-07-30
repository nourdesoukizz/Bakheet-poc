import sys
sys.path.append('algorithms')

print("Testing Random Forest specifically...")

try:
    from algorithms.machine_learning.random_forest import RandomForestForecasting
    
    print("✅ Import successful")
    
    # Initialize
    rf = RandomForestForecasting(
        n_estimators=50,
        optimize_hyperparams=False,
        forecast_strategy='recursive'
    )
    print("✅ Initialization successful")
    
    # Load data
    df = rf.load_data('data/Sample_FiveYears_Sales_SpareParts.xlsx')
    print(f"✅ Data loading successful: {len(df)} items")
    print(f"✅ time_columns set: {hasattr(rf, 'time_columns')}")
    if hasattr(rf, 'time_columns'):
        print(f"   Number of time columns: {len(rf.time_columns)}")
    
    # Test on just 1 item
    test_df = df.head(1)
    print(f"✅ Testing on 1 item: {test_df.iloc[0]['item_id']}")
    
    # Try forecasting
    results = rf.fit_and_forecast(test_df, forecast_periods=12)
    print("✅ Random Forest forecasting successful!")
    
    # Check results
    for item_id, forecast_data in results['item_forecasts'].items():
        print(f"   Item {item_id}: {len(forecast_data['monthly_forecasts'])} forecasts")
    
except Exception as e:
    print(f"❌ Random Forest failed: {e}")
    import traceback
    traceback.print_exc()
