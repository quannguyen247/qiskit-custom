import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 1. Khởi tạo mạch
n_qubits = 25
qc = QuantumCircuit(n_qubits)
qc.h(range(n_qubits)) 
qc.measure_all()

# 2. Khởi tạo Simulator
# Nếu máy có GPU NVIDIA, bạn có thể dùng device='GPU' để cực nhanh
simulator = AerSimulator(method='statevector') 

# 3. Transpile (Quan trọng: Chuyển mạch về tập lệnh mà simulator hiểu)
compiled_circuit = transpile(qc, simulator)

# 4. Chạy
job = simulator.run(compiled_circuit, shots=1000)
result = job.result()

print("Done dmm")
print(result.get_counts())