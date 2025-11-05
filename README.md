
# Quantum Reliability Model for k-out-of-n Systems

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

A quantum circuit implementation for computing k-out-of-n system reliability using Qiskit. This code models systems where at least k out of n components must be operational for the system to function.

## Features

- **Variable component probabilities**: Each component can have a different reliability
- **Quantum circuit approach**: Uses Ry gates and multi-controlled gates for reliability logic
- **Classical benchmarking**: Provides exact classical solution for comparison
- **Statistical validation**: Includes confidence intervals and error analysis
- **Circuit visualization**: Displays the quantum circuit diagram in ASCII format

## Installation

Install the required dependencies:

```bash
pip install qiskit qiskit-aer numpy scipy
```

## Quick Start

```python
from qiskit_koon_mcx import run_simulation

# Example: 3-out-of-4 system with component reliability 0.97
p_list = [0.97, 0.97, 0.97, 0.97]
k = 3

results = run_simulation(p_list, k, num_simulations=100, numshots=8192)

print(f"System Reliability: {results['quantum_mean']:.6f}")
print(f"95% CI: [{results['ci_lower']:.6f}, {results['ci_upper']:.6f}]")
```

## Usage

### Basic Example

```python
import qiskit_koon_mcx

# Define system parameters
n = 4  # Number of components
k = 3  # Minimum working components needed
p_list = [0.97, 0.97, 0.97, 0.97]  # Component reliabilities

# Run simulation with circuit visualization
results = qiskit_koon_mcx.run_simulation(p_list, k, print_circuit=True)
```

### Variable Component Reliabilities

```python
import qiskit_koon_mcx

# Different reliability for each component
p_list = [0.95, 0.97, 0.98, 0.99]
k = 2

results = qiskit_koon_mcx.run_simulation(p_list, k, num_simulations=100)
```

### Disable Circuit Printing

```python
import qiskit_koon_mcx

# ... setup p_list and k ...

results = qiskit_koon_mcx.run_simulation(p_list, k, print_circuit=False)
```

## How It Works

1. **Encoding**: Component reliabilities are encoded using Ry rotation gates: $\theta_i = 2 \cdot \arcsin(\sqrt{p_i})$
2. **Logic**: Multi-controlled X gates implement the k-out-of-n logic by checking all valid component combinations
3. **Measurement**: The output qubit indicates system success ($|1\rangle$) or failure ($|0\rangle$)
4. **Analysis**: Statistical validation compares quantum results against classical benchmarks

## Function Reference

### `reliability_circuit_variable_p(p_list, k)`
Constructs the quantum circuit for k-out-of-n reliability calculation.

**Parameters:**
- `p_list` (list): Component reliability probabilities
- `k` (int): Minimum number of working components needed

**Returns:**
- `QuantumCircuit`: Qiskit quantum circuit

### `k_out_of_n_variable_p_reliability(p_list, k)`
Calculates exact classical reliability for comparison.

**Parameters:**
- `p_list` (list): Component reliability probabilities
- `k` (int): Minimum number of working components needed

**Returns:**
- `float`: Exact system reliability

### `run_simulation(p_list, k, num_simulations=100, numshots=8192, confidence_level=0.95, print_circuit=True)`
Runs quantum simulation with statistical analysis.

**Parameters:**
- `p_list` (list): Component reliability probabilities
- `k` (int): Minimum number of working components needed
- `num_simulations` (int): Number of independent simulation runs
- `numshots` (int): Number of shots per simulation
- `confidence_level` (float): Confidence level for interval (default 0.95)
- `print_circuit` (bool): Whether to display circuit diagram

**Returns:**
- `dict`: Results containing classical and quantum reliability estimates, confidence intervals, and error metrics

## Citation

If you use this software in your research, please cite it using the information below or from the `CITATION.cff` file:

```bibtex
@software{quantum_reliability_model,
  author = {Abhinav Krishnan T K},
  title = {Quantum Reliability Model for k-out-of-n Systems},
  year = {2025},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://github.com/your-github-username/quantum-reliability-model}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or feedback, please open an issue on GitHub.

## Acknowledgments

Built using [Qiskit](https://qiskit.org/), the open-source quantum computing framework.
