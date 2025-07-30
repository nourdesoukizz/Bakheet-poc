import sys
sys.path.append('algorithms')

print("Testing XGBoost specifically...")

try:
    from algorithms.machine_learning.xgboost import XGBoostForecasting
    print("✅ Import successful")
    
    # Initialize
    xgb_model = XGBoostForecasting(
        n_estimators=100,
        optimize_hyperparams=False
    )
    print("✅ Initialization successful")
    
    # Load data
    df = xgb_model.load_data('data/Sample_FiveYears_Sales_SpareParts.xlsx')
    print(f"✅ Data loading successful: {len(df)} items")
    
    # Test on just 1 item
    test_df = df.head(1)
    print(f"✅ Testing on 1 item: {test_df.iloc[0]['item_id']}")
    
    # Try forecasting
    results = xgb_model.fit_and_forecast(test_df, forecast_periods=12)
    print("✅ XGBoost forecasting successful!")
    
    # Check results
    for item_id, forecast_data in results['item_forecasts'].items():
        print(f"   Item {item_id}: {len(forecast_data['monthly_forecasts'])} forecasts")
    
except Exception as e:
    print(f"❌ XGBoost failed: {e}")
    import traceback
    traceback.print_exc()
