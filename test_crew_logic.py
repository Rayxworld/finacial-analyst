import re
import warnings
import matplotlib
import matplotlib.pyplot as plt
from financial_engine import run_deterministic_analysis, SharedState

# Suppress Pydantic and Tcl/Tk noise
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="pydantic")
matplotlib.use('Agg')

def main():
    print("--- Starting Zero-Stress Predictive Analysis Test ---")
    try:
        # Test Multi-Stock Comparison
        query_comp = "Compare NVDA and TSLA"
        print(f"\n--- Testing Comparison: '{query_comp}' ---")
        result_comp = run_deterministic_analysis(query_comp)
        print(result_comp)
        
        # Test Single Analysis
        query_single = "Analyze Apple"
        print(f"\n--- Testing Single: '{query_single}' ---")
        result_single = run_deterministic_analysis(query_single)
        print(result_single)
        
        if SharedState.latest_fig:
             print("\n[SUCCESS] Viz figure detected.")
        else:
             print("\n[WARNING] No visualization was generated.")
             
        print("\n--- Test Completed ---")
    except Exception as e:
        print(f"\n--- Test Failed ---")
        print(f"Error detail: {e}")

if __name__ == "__main__":
    main()
