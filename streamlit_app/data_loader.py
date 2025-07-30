import pandas as pd
import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

class ForecastDataLoader:
    """
    Loads and consolidates forecasting results from all 6 algorithms
    """
    
    def __init__(self, results_directory: str = "outputs/test_results"):
        self.results_directory = results_directory
        self.algorithms = ["LSTM", "Prophet", "Random_Forest", "SARIMA", "SBA", "XGBoost"]
        self.consolidated_data = None
        
    def load_algorithm_data(self, algorithm: str) -> pd.DataFrame:
        """Load data for a specific algorithm"""
        try:
            # Find the most recent file for this algorithm
            pattern = os.path.join(self.results_directory, f"{algorithm}_detailed_forecasts_*.csv")
            files = glob.glob(pattern)
            
            if not files:
                print(f"⚠️  No files found for {algorithm}")
                return pd.DataFrame()
            
            # Get the most recent file
            latest_file = max(files, key=os.path.getctime)
            print(f"📊 Loading {algorithm}: {os.path.basename(latest_file)}")
            
            df = pd.read_csv(latest_file)
            return df
            
        except Exception as e:
            print(f"❌ Error loading {algorithm}: {e}")
            return pd.DataFrame()
    
    def consolidate_data(self) -> Dict[str, Any]:
        """Consolidate all algorithm data by Item_ID"""
        print("🔄 Consolidating forecast data from all algorithms...")
        
        all_data = {}
        
        # Load data from all algorithms
        for algorithm in self.algorithms:
            df = self.load_algorithm_data(algorithm)
            if not df.empty:
                all_data[algorithm] = df
        
        if not all_data:
            print("❌ No data loaded from any algorithm")
            return {}
        
        # Get unique items from the first available algorithm
        first_algo = list(all_data.keys())[0]
        unique_items = all_data[first_algo]['Item_ID'].unique()
        
        consolidated = {
            "metadata": {
                "total_items": len(unique_items),
                "algorithms_loaded": list(all_data.keys()),
                "load_timestamp": datetime.now().isoformat()
            },
            "items": []
        }
        
        # Process each item
        for item_id in unique_items:
            item_data = self._process_item(item_id, all_data)
            if item_data:
                consolidated["items"].append(item_data)
        
        self.consolidated_data = consolidated
        print(f"✅ Consolidated data for {len(consolidated['items'])} items")
        return consolidated
    
    def _process_item(self, item_id: str, all_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Process forecasting data for a single item"""
        try:
            item_info = {}
            monthly_forecasts = {}
            annual_totals = {}
            
            # Get item metadata from first available algorithm
            for algorithm, df in all_data.items():
                item_rows = df[df['Item_ID'] == item_id]
                if not item_rows.empty:
                    if not item_info:  # First time we see this item
                        item_info = {
                            "item_id": item_id,
                            "item_name": item_rows.iloc[0]['Item_Name'],
                            "category": item_rows.iloc[0]['Category'],
                            "historical_total": int(item_rows.iloc[0]['Historical_Total'])
                        }
                    
                    # Get monthly forecasts (months 1-12)
                    monthly_values = []
                    for month in range(1, 13):
                        month_row = item_rows[item_rows['Month'] == month]
                        if not month_row.empty:
                            monthly_values.append(float(month_row.iloc[0]['Forecast_Value']))
                        else:
                            monthly_values.append(0.0)
                    
                    monthly_forecasts[algorithm] = monthly_values
                    annual_totals[algorithm] = sum(monthly_values)
            
            if not item_info:
                return None
            
            # Select best algorithm and generate reasoning
            selected_algorithm, reasoning = self._select_best_algorithm(
                item_info, monthly_forecasts, annual_totals
            )
            
            return {
                **item_info,
                "monthly_forecasts": monthly_forecasts,
                "annual_totals": annual_totals,
                "selected_model": selected_algorithm,
                "selected_reasoning": reasoning,
                "algorithms_available": list(monthly_forecasts.keys())
            }
            
        except Exception as e:
            print(f"❌ Error processing item {item_id}: {e}")
            return None
    
    def _select_best_algorithm(self, item_info: Dict, monthly_forecasts: Dict, annual_totals: Dict) -> tuple:
        """Select the best algorithm for an item with reasoning"""
        
        item_id = item_info["item_id"]
        historical_total = item_info["historical_total"]
        
        # If no historical demand, any algorithm is fine (they should all predict 0)
        if historical_total == 0:
            available_algos = list(annual_totals.keys())
            return available_algos[0], "No historical demand - any algorithm suitable"
        
        # Remove algorithms with zero or negative annual forecasts for items with historical demand
        valid_algorithms = {k: v for k, v in annual_totals.items() if v > 0}
        
        if not valid_algorithms:
            # All algorithms predict zero for item with historical demand
            available_algos = list(annual_totals.keys())
            return available_algos[0], "All algorithms predict zero demand - choosing first available"
        
        # Calculate forecast ratios (forecast/historical)
        forecast_ratios = {k: v / historical_total for k, v in valid_algorithms.items()}
        
        # Identify outliers (too high or too low)
        ratios = list(forecast_ratios.values())
        median_ratio = np.median(ratios)
        std_ratio = np.std(ratios)
        
        # Algorithm selection logic
        reasonable_algorithms = {}
        outlier_info = []
        
        for algo, ratio in forecast_ratios.items():
            annual_forecast = valid_algorithms[algo]
            
            # Flag extreme outliers (more than 2 std deviations from median)
            if abs(ratio - median_ratio) > 2 * std_ratio and len(ratios) > 2:
                if ratio > median_ratio:
                    outlier_info.append(f"{algo} overestimates ({annual_forecast:.0f} vs historical {historical_total})")
                else:
                    outlier_info.append(f"{algo} underestimates significantly")
            else:
                reasonable_algorithms[algo] = {
                    'annual': annual_forecast,
                    'ratio': ratio,
                    'monthly_variance': np.std(monthly_forecasts[algo])
                }
        
        # Choose from reasonable algorithms
        if reasonable_algorithms:
            # Prefer algorithm with moderate variance (not too flat, not too spiky)
            variances = {k: v['monthly_variance'] for k, v in reasonable_algorithms.items()}
            median_variance = np.median(list(variances.values()))
            
            # Choose algorithm closest to median variance
            best_algo = min(reasonable_algorithms.keys(), 
                          key=lambda x: abs(variances[x] - median_variance))
            
            # Generate reasoning
            selected_annual = reasonable_algorithms[best_algo]['annual']
            selected_ratio = reasonable_algorithms[best_algo]['ratio']
            
            reasoning_parts = [
                f"Selected for balanced forecasting approach ({selected_annual:.0f} annual vs {historical_total} historical)"
            ]
            
            if outlier_info:
                reasoning_parts.append("Avoided: " + "; ".join(outlier_info[:2]))
            
            reasoning = ". ".join(reasoning_parts)
            
        else:
            # No reasonable algorithms found, choose the one closest to historical
            best_algo = min(forecast_ratios.keys(), key=lambda x: abs(forecast_ratios[x] - 1.0))
            reasoning = f"Closest to historical demand pattern among available algorithms"
        
        return best_algo, reasoning
    
    def save_consolidated_data(self, filename: str = None) -> str:
        """Save consolidated data to JSON file"""
        if not self.consolidated_data:
            raise ValueError("No consolidated data available. Run consolidate_data() first.")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"consolidated_forecast_data_{timestamp}.json"
        
        filepath = os.path.join("streamlit_app", filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.consolidated_data, f, indent=2)
        
        print(f"💾 Consolidated data saved to: {filepath}")
        return filepath
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the consolidated data"""
        if not self.consolidated_data:
            return {}
        
        items = self.consolidated_data["items"]
        algorithms = self.consolidated_data["metadata"]["algorithms_loaded"]
        
        # Algorithm selection distribution
        selection_counts = {}
        for item in items:
            selected = item["selected_model"]
            selection_counts[selected] = selection_counts.get(selected, 0) + 1
        
        # Items by category
        category_counts = {}
        for item in items:
            category = item["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Historical demand distribution
        historical_totals = [item["historical_total"] for item in items]
        
        return {
            "total_items": len(items),
            "algorithms_available": algorithms,
            "algorithm_selection_distribution": selection_counts,
            "category_distribution": category_counts,
            "historical_demand_stats": {
                "min": min(historical_totals),
                "max": max(historical_totals),
                "mean": np.mean(historical_totals),
                "median": np.median(historical_totals),
                "zero_demand_items": sum(1 for x in historical_totals if x == 0)
            }
        }

def main():
    """Main function for testing the data loader"""
    print("🚀 Starting Forecast Data Consolidation")
    print("=" * 50)
    
    # Initialize data loader
    loader = ForecastDataLoader()
    
    # Check if results directory exists
    if not os.path.exists(loader.results_directory):
        print(f"❌ Results directory not found: {loader.results_directory}")
        print("Please ensure the outputs/test_results directory exists with CSV files")
        return
    
    # Consolidate data
    consolidated = loader.consolidate_data()
    
    if not consolidated:
        print("❌ Failed to consolidate data")
        return
    
    # Save consolidated data
    saved_file = loader.save_consolidated_data()
    
    # Print summary statistics
    stats = loader.get_summary_stats()
    print("\n📊 Summary Statistics:")
    print(f"  Total Items: {stats['total_items']}")
    print(f"  Algorithms: {', '.join(stats['algorithms_available'])}")
    print(f"  Categories: {stats['category_distribution']}")
    print(f"  Algorithm Selections: {stats['algorithm_selection_distribution']}")
    print(f"  Historical Demand Range: {stats['historical_demand_stats']['min']} - {stats['historical_demand_stats']['max']}")
    
    # Show sample item
    if consolidated["items"]:
        sample_item = consolidated["items"][0]
        print(f"\n🔍 Sample Item: {sample_item['item_id']}")
        print(f"  Name: {sample_item['item_name'][:50]}...")
        print(f"  Selected Model: {sample_item['selected_model']}")
        print(f"  Reasoning: {sample_item['selected_reasoning']}")
        print(f"  Annual Totals: {sample_item['annual_totals']}")
    
    print(f"\n✅ Data consolidation complete! File saved: {saved_file}")

if __name__ == "__main__":
    main()