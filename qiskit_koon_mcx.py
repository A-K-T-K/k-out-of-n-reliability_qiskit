"""
Quantum Reliability Model for k-out-of-n Systems
Author: Abhinav Krishnan T K
License: MIT
"""

import numpy as np
from itertools import combinations, product
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import scipy.stats


def reliability_circuit_variable_p(p_list, k):
    """Creates a quantum circuit to model k-out-of-n system reliability."""
    n = len(p_list)
    q_components = QuantumRegister(n, "comp")
    q_out = QuantumRegister(1, "out")
    c_out = ClassicalRegister(1, "c")
    qc = QuantumCircuit(q_components, q_out, c_out)

    # Encode component probabilities
    for i, p_i in enumerate(p_list):
        theta = 2 * np.arcsin(np.sqrt(p_i))
        qc.ry(theta, q_components[i])

    # Logic for k-out-of-n
    for r in range(k, n + 1):
        for success_subset in combinations(range(n), r):
            fail_subset = [i for i in range(n) if i not in success_subset]
            for f in fail_subset:
                qc.x(q_components[f])
            qc.mcx([q_components[i] for i in range(n)], q_out[0])
            for f in fail_subset:
                qc.x(q_components[f])

    qc.measure(q_out, c_out)
    return qc


def k_out_of_n_variable_p_reliability(p_list, k):
    """Classical benchmark calculation."""
    n = len(p_list)
    total_prob = 0.0
    for bits in product([0, 1], repeat=n):
        if sum(bits) >= k:
            prob = 1.0
            for bit, p_i in zip(bits, p_list):
                prob *= p_i if bit == 1 else (1 - p_i)
            total_prob += prob
    return total_prob


def run_simulation(p_list, k, num_simulations=100, numshots=8192, 
                   confidence_level=0.95, print_circuit=True):
    """Run simulation with statistical analysis."""
    # Classical result
    classical_prob = k_out_of_n_variable_p_reliability(p_list, k)
    
    # Quantum simulation
    qc = reliability_circuit_variable_p(p_list, k)
    
    # Print circuit if requested
    if print_circuit:
        print("\n" + "="*60)
        print("QUANTUM CIRCUIT DIAGRAM")
        print("="*60)
        print(qc.draw(output='text'))
        print("="*60 + "\n")
    
    backend = AerSimulator()
    quantum_probs = []
    
    for sim_idx in range(num_simulations):
        compiled_circuit = transpile(qc, backend)
        job = backend.run(compiled_circuit, shots=numshots)
        result = job.result()
        counts = result.get_counts()
        quantum_prob = counts.get('1', 0) / numshots
        quantum_probs.append(quantum_prob)
    
    # Statistics
    quantum_probs_array = np.array(quantum_probs)
    mean_quantum = np.mean(quantum_probs_array)
    std_quantum = np.std(quantum_probs_array, ddof=1) if num_simulations > 1 else 0
    
    if num_simulations > 1:
        t_value = scipy.stats.t.ppf((1 + confidence_level) / 2.0, 
                                    df=num_simulations - 1)
        se = std_quantum / np.sqrt(num_simulations)
        ci_length = t_value * se
        ci_lower = mean_quantum - ci_length
        ci_upper = mean_quantum + ci_length
    else:
        ci_lower = ci_upper = mean_quantum
    
    relative_error = (abs(mean_quantum - classical_prob) / classical_prob) * 100
    
    return {
        'classical': classical_prob,
        'quantum_mean': mean_quantum,
        'quantum_std': std_quantum,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'relative_error': relative_error
    }


if __name__ == "__main__":
    # Example: 3-out-of-4 system
    print("\n" + "="*60)
    print("QUANTUM RELIABILITY SIMULATION")
    print("System: 3-out-of-4 (k=3, n=4)")
    print("Component Reliability: p = 0.97 for all components")
    print("="*60)
    
    p_list = [0.97, 0.97, 0.97, 0.97]
    k = 3
    
    results = run_simulation(p_list, k, num_simulations=100, numshots=8192, 
                            print_circuit=True)
    
    print("SIMULATION RESULTS")
    print("="*60)
    print(f"Classical Reliability: {results['classical']:.6f}")
    print(f"Mean Quantum Reliability: {results['quantum_mean']:.6f}")
    print(f"Std Dev: {results['quantum_std']:.6f}")
    print(f"95% CI: [{results['ci_lower']:.6f}, {results['ci_upper']:.6f}]")
    print(f"Relative Error: {results['relative_error']:.4f}%")
    print("="*60 + "\n")
