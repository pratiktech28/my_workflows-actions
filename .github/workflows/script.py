print("This is my dedications")
import h5py
import numpy as np
import matplotlib.pyplot as plt

class GprMaxRegressionEngine:
    def __init__(self, golden_file, test_output_file):
        """
        Initializes the regression engine.
        :param golden_file: Path to the validated baseline HDF5 file.
        :param test_output_file: Path to the current simulation output file.
        """
        self.golden_file = golden_file
        self.test_output_file = test_output_file
        self.threshold = 1e-5 # Precision threshold for scientific accuracy

    def extract_trace(self, file_path, component='Ez'):
        """Extracts the A-scan trace from the HDF5 file."""
        with h5py.File(file_path, 'r') as f:
            # Accessing the Rx trace data
            data = f['rxs/rx1/' + component][:]
        return data

    def compare_physics(self):
        """Calculates the deviation between Golden Model and Current PR."""
        golden_trace = self.extract_trace(self.golden_file)
        current_trace = self.extract_trace(self.test_output_file)

        # Calculating Normalized Root Mean Square Error (NRMSE)
        error = np.sqrt(np.mean((golden_trace - current_trace)**2)) / (np.max(golden_trace) - np.min(golden_trace))
        
        status = "PASSED" if error < self.threshold else "FAILED"
        return status, error

# Example Usage for GitHub Actions Pipeline
if __name__ == "__main__":
    engine = GprMaxRegressionEngine("benchmarks/half_space_gold.out", "output/current_test.out")
    status, error_val = engine.compare_physics()
    
    print(f"Regression Status: {status} | Error: {error_val:.8f}")
    if status == "FAILED":
        exit(1) # Signal failure to GitHub Actions runner   