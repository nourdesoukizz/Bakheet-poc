import pandas as pd
import numpy as np
import json
import pickle
from datetime import datetime, timedelta
import sys
import os
import warnings
import traceback
warnings.filterwarnings('ignore')

# Add algorithms to path
sys.path.append('algorithms')

class AlgorithmTester:
    def __init__(self, data_path: str = 'data/Sample_FiveYears_Sales_SpareParts.xlsx'):
        self.data_path = data_path
        self.results = {}
        self.test_summary = []
        
    def test_sarima(self, sample_size=5):
        """Test SARIMA algorithm"""
        print("Testing SARIMA...")
        try:
            from algorithms.classical.sarima import SARIMAForecasting
            
            sarima = SARIMAForecasting(
                seasonal_period=12,
                max_p=2, max_d=1, max_q=2,
                max_P=1, max_D=1, max_Q=1,
                auto_arima=True
            )
            
            # Load data using the algorithm's own loader
            df = sarima.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            # Use sample for testing
            test_df = df.head(sample_size)
            
            results = sarima.fit_and_forecast(test_df, forecast_periods=12)
            summary = sarima.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'SARIMA'
            }
            
        except Exception as e:
            print(f"SARIMA failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'SARIMA'
            }
    
    def test_sba(self, sample_size=5):
        """Test SBA algorithm"""
        print("Testing SBA...")
        try:
            from algorithms.classical.sba_forecasting import SBAForecasting
            
            sba = SBAForecasting(alpha=0.1, beta=0.1)
            
            # Load data using the algorithm's own loader
            df = sba.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            test_df = df.head(sample_size)
            results = sba.fit_and_forecast(test_df, forecast_periods=12)
            summary = sba.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'SBA'
            }
            
        except Exception as e:
            print(f"SBA failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'SBA'
            }
    
    def test_random_forest(self, sample_size=5):
        """Test Random Forest algorithm"""
        print("Testing Random Forest...")
        try:
            from algorithms.machine_learning.random_forest import RandomForestForecasting
            
            rf = RandomForestForecasting(
                n_estimators=50,
                optimize_hyperparams=False,
                forecast_strategy='recursive'
            )
            
            # Load data using the algorithm's own loader
            df = rf.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            test_df = df.head(sample_size)
            results = rf.fit_and_forecast(test_df, forecast_periods=12)
            summary = rf.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'Random_Forest'
            }
            
        except Exception as e:
            print(f"Random Forest failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'Random_Forest'
            }
    
    def test_xgboost(self, sample_size=5):
        """Test XGBoost algorithm"""
        print("Testing XGBoost...")
        try:
            from algorithms.machine_learning.xgboost import XGBoostForecasting
            
            xgb_model = XGBoostForecasting(
                n_estimators=100,
                optimize_hyperparams=False
            )
            
            # Load data using the algorithm's own loader
            df = xgb_model.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            test_df = df.head(sample_size)
            results = xgb_model.fit_and_forecast(test_df, forecast_periods=12)
            summary = xgb_model.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'XGBoost'
            }
            
        except Exception as e:
            print(f"XGBoost failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'XGBoost'
            }
    
    def test_lstm(self, sample_size=5):
        """Test LSTM algorithm"""
        print("Testing LSTM...")
        try:
            from algorithms.deep_learning.lstm import LSTMForecasting
            
            lstm = LSTMForecasting(
                sequence_length=12,
                lstm_units=[64, 32],
                epochs=20,
                ensemble_size=2,
                architecture='stacked'
            )
            
            # Load data using the algorithm's own loader
            df = lstm.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            test_df = df.head(sample_size)
            results = lstm.fit_and_forecast(test_df, forecast_periods=12)
            summary = lstm.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'LSTM'
            }
            
        except Exception as e:
            print(f"LSTM failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'LSTM'
            }
    
    def test_prophet(self, sample_size=5):
        """Test Prophet algorithm"""
        print("Testing Prophet...")
        try:
            from algorithms.time_series.prophet import ProphetForecasting
            
            prophet = ProphetForecasting(
                growth='linear',
                yearly_seasonality='auto',
                seasonality_mode='additive'
            )
            
            # Load data using the algorithm's own loader
            df = prophet.load_data(self.data_path)
            if df.empty:
                raise Exception("Failed to load data")
            
            test_df = df.head(sample_size)
            results = prophet.fit_and_forecast(test_df, forecast_periods=12)
            summary = prophet.create_forecast_summary(results)
            
            return {
                'status': 'success',
                'results': results,
                'summary': summary,
                'algorithm': 'Prophet'
            }
            
        except Exception as e:
            print(f"Prophet failed: {str(e)}")
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e),
                'algorithm': 'Prophet'
            }
    
    def validate_forecasts(self, results, algorithm_name):
        """Validate that forecasts contain exactly 12 months"""
        validation_results = {
            'algorithm': algorithm_name,
            'total_items': 0,
            'items_with_12_forecasts': 0,
            'items_with_errors': 0,
            'forecast_length_distribution': {}
        }
        
        if results['status'] != 'success':
            return validation_results
        
        item_forecasts = results['results']['item_forecasts']
        validation_results['total_items'] = len(item_forecasts)
        
        for item_id, forecast_data in item_forecasts.items():
            forecast_length = len(forecast_data['monthly_forecasts'])
            
            # Count forecast lengths
            if forecast_length not in validation_results['forecast_length_distribution']:
                validation_results['forecast_length_distribution'][forecast_length] = 0
            validation_results['forecast_length_distribution'][forecast_length] += 1
            
            # Check if exactly 12 forecasts
            if forecast_length == 12:
                validation_results['items_with_12_forecasts'] += 1
            else:
                validation_results['items_with_errors'] += 1
                print(f"  WARNING: {item_id} has {forecast_length} forecasts instead of 12")
        
        return validation_results
    
    def test_all_algorithms(self, sample_size=5):
        """Test all algorithms on a sample of data"""
        print("="*60)
        print("ALGORITHM TESTING STARTED")
        print("="*60)
        
        print(f"Testing on {sample_size} items")
        
        # Test algorithms
        algorithms_to_test = [
            ('SARIMA', self.test_sarima),
            ('SBA', self.test_sba),
            ('Random_Forest', self.test_random_forest),
            ('XGBoost', self.test_xgboost),
            ('LSTM', self.test_lstm),
            ('Prophet', self.test_prophet)
        ]
        
        for algo_name, test_func in algorithms_to_test:
            print(f"\n{'-'*40}")
            print(f"Testing {algo_name}")
            print(f"{'-'*40}")
            
            start_time = datetime.now()
            result = test_func(sample_size)
            end_time = datetime.now()
            
            result['execution_time'] = str(end_time - start_time)
            result['timestamp'] = datetime.now().isoformat()
            
            # Validate forecasts
            validation = self.validate_forecasts(result, algo_name)
            result['validation'] = validation
            
            self.results[algo_name] = result
            
            # Print summary
            if result['status'] == 'success':
                print(f"✅ {algo_name} completed successfully!")
                print(f"   Execution time: {result['execution_time']}")
                print(f"   Items processed: {validation['total_items']}")
                print(f"   Items with 12 forecasts: {validation['items_with_12_forecasts']}")
                if validation['items_with_errors'] > 0:
                    print(f"   ⚠️  Items with forecast errors: {validation['items_with_errors']}")
            else:
                print(f"❌ {algo_name} failed!")
                print(f"   Error: {result['error']}")
    
    def create_comparison_table(self):
        """Create a comparison table of all algorithm results"""
        comparison_data = []
        
        # Get all successfully processed items
        successful_algos = {name: data for name, data in self.results.items() 
                          if data['status'] == 'success'}
        
        if not successful_algos:
            print("No successful algorithms to compare!")
            return pd.DataFrame()
        
        # Get common items across all successful algorithms
        all_items = None
        for algo_name, algo_data in successful_algos.items():
            items = set(algo_data['results']['item_forecasts'].keys())
            if all_items is None:
                all_items = items
            else:
                all_items = all_items.intersection(items)
        
        if not all_items:
            print("No common items found across algorithms!")
            return pd.DataFrame()
        
        # Create comparison for each item
        for item_id in sorted(all_items):
            item_row = {
                'Item_ID': item_id,
                'Item_Name': '',
                'Category': '',
                'Historical_Total': 0
            }
            
            # Get item info from first successful algorithm
            first_algo = list(successful_algos.keys())[0]
            item_data = successful_algos[first_algo]['results']['item_forecasts'][item_id]
            item_row['Item_Name'] = item_data['item_name'][:30] + '...' if len(item_data['item_name']) > 30 else item_data['item_name']
            item_row['Category'] = item_data['category']
            item_row['Historical_Total'] = sum(item_data['historical_demand'])
            
            # Add forecast results from each algorithm
            for algo_name in successful_algos.keys():
                forecast_data = successful_algos[algo_name]['results']['item_forecasts'][item_id]
                annual_forecast = sum(forecast_data['monthly_forecasts'])
                item_row[f'{algo_name}_Annual_Forecast'] = round(annual_forecast, 2)
                item_row[f'{algo_name}_Monthly_Avg'] = round(annual_forecast / 12, 2)
            
            comparison_data.append(item_row)
        
        return pd.DataFrame(comparison_data)
    
    def save_results(self):
        """Save all test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        os.makedirs('outputs/test_results', exist_ok=True)
        
        # Save detailed results (for Streamlit app)
        with open(f'outputs/test_results/algorithm_results_{timestamp}.pkl', 'wb') as f:
            pickle.dump(self.results, f)
        
        # Save comparison table
        comparison_df = self.create_comparison_table()
        if not comparison_df.empty:
            comparison_df.to_csv(f'outputs/test_results/algorithm_comparison_{timestamp}.csv', index=False)
            print(f"Comparison table saved with {len(comparison_df)} items")
        
        # Save summary statistics
        summary_stats = {}
        for algo_name, result in self.results.items():
            summary_stats[algo_name] = {
                'status': result['status'],
                'execution_time': result.get('execution_time', 'N/A'),
                'validation': result.get('validation', {})
            }
        
        with open(f'outputs/test_results/test_summary_{timestamp}.json', 'w') as f:
            json.dump(summary_stats, f, indent=2)
        
        # Save individual algorithm forecasts for detailed analysis
        for algo_name, result in self.results.items():
            if result['status'] == 'success':
                # Save detailed forecasts
                detailed_forecasts = []
                for item_id, forecast_data in result['results']['item_forecasts'].items():
                    for month in range(12):
                        if month < len(forecast_data['monthly_forecasts']):
                            detailed_forecasts.append({
                                'Algorithm': algo_name,
                                'Item_ID': item_id,
                                'Item_Name': forecast_data['item_name'],
                                'Category': forecast_data['category'],
                                'Month': month + 1,
                                'Forecast_Value': forecast_data['monthly_forecasts'][month],
                                'Historical_Total': sum(forecast_data['historical_demand'])
                            })
                
                if detailed_forecasts:
                    pd.DataFrame(detailed_forecasts).to_csv(
                        f'outputs/test_results/{algo_name}_detailed_forecasts_{timestamp}.csv', 
                        index=False
                    )
        
        print(f"\n📁 All results saved to outputs/test_results/ with timestamp: {timestamp}")
        return timestamp

if __name__ == "__main__":
    print("🚀 Starting Algorithm Testing Suite")
    print("This will test all 6 forecasting algorithms and validate 12-month forecasts")
    
    tester = AlgorithmTester()
    
    # Test with first 5 items for quick testing
    tester.test_all_algorithms(sample_size=5)
    
    # Save results
    timestamp = tester.save_results()
    
    print("\n" + "="*60)
    print("TESTING COMPLETED!")
    print("="*60)
    
    # Print final summary
    successful_algos = [name for name, result in tester.results.items() if result['status'] == 'success']
    failed_algos = [name for name, result in tester.results.items() if result['status'] == 'failed']
    
    print(f"✅ Successful algorithms: {len(successful_algos)}")
    for algo in successful_algos:
        validation = tester.results[algo].get('validation', {})
        print(f"   - {algo}: {validation.get('items_with_12_forecasts', 0)}/{validation.get('total_items', 0)} items with 12 forecasts")
    
    if failed_algos:
        print(f"❌ Failed algorithms: {len(failed_algos)}")
        for algo in failed_algos:
            print(f"   - {algo}")
    
    print(f"\n📊 Results saved with timestamp: {timestamp}")
    print("Ready for Streamlit app integration!")