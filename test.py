import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Global config
Sim_mode = 'statevector'


# 1. Khởi tạo mạch
n_qubits = 30
qc = QuantumCircuit(n_qubits)
qc.h(range(n_qubits)) 
qc.measure_all()

# 2. Khởi tạo Simulator
simulator = AerSimulator(method=Sim_mode) 

# 3. Transpile 
compiled_circuit = transpile(qc, simulator)

# 4. Chạy
job = simulator.run(compiled_circuit, shots=1000)
result = job.result()

print("Done dmm")
print(result.get_counts())