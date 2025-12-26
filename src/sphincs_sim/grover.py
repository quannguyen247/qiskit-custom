from qiskit import QuantumCircuit
import numpy as np

class GroverDiffuser:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits

    def get_circuit(self):
        """
        Tạo mạch Diffuser (còn gọi là Inversion about the Mean).
        Công thức: H -> X -> MCZ -> X -> H
        """
        qc = QuantumCircuit(self.n_qubits, name="Diffuser")
        
        # 1. Apply H to all qubits
        qc.h(range(self.n_qubits))
        
        # 2. Apply X to all qubits
        qc.x(range(self.n_qubits))
        
        # 3. Apply Multi-Controlled Z
        qc.h(self.n_qubits - 1)
        qc.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        qc.h(self.n_qubits - 1)
        
        # 4. Apply X to all qubits
        qc.x(range(self.n_qubits))
        
        # 5. Apply H to all qubits
        qc.h(range(self.n_qubits))
        
        return qc

class GroverAttack:
    def __init__(self, oracle_circuit, n_qubits):
        self.oracle = oracle_circuit
        self.n_qubits = n_qubits
        self.diffuser = GroverDiffuser(n_qubits).get_circuit()

    def build_circuit(self, optimal_iterations=None):
        """
        Xây dựng mạch Grover hoàn chỉnh.
        """
        # Tính số lần lặp tối ưu nếu không được cung cấp
        # R ~ (pi/4) * sqrt(N)
        if optimal_iterations is None:
            N = 2**self.n_qubits
            optimal_iterations = int(np.floor(np.pi/4 * np.sqrt(N)))
        
        print(f"--- Cấu hình Grover ---")
        print(f"Search Space (N): 2^{self.n_qubits} = {2**self.n_qubits}")
        print(f"Optimal Iterations: {optimal_iterations}")
        
        qc = QuantumCircuit(self.n_qubits)
        
        # 1. Khởi tạo siêu chồng chất (Superposition)
        qc.h(range(self.n_qubits))
        
        # 2. Lặp lại Oracle và Diffuser
        for _ in range(optimal_iterations):
            qc.append(self.oracle, range(self.n_qubits))
            qc.append(self.diffuser, range(self.n_qubits))
            
        # 3. Đo lường
        qc.measure_all()
        
        return qc, optimal_iterations
