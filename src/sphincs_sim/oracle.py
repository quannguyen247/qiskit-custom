from qiskit import QuantumCircuit
import numpy as np

class ToyHashOracle:
    def __init__(self, n_qubits, target_state_str):
        """
        Khởi tạo Oracle cho một hàm băm giả lập.
        
        Args:
            n_qubits (int): Số lượng qubit dùng cho đầu vào (input register).
            target_state_str (str): Chuỗi bit mục tiêu (Secret Key) cần tìm (ví dụ: '101').
        """
        self.n_qubits = n_qubits
        self.target_state = target_state_str
        # Đảm bảo độ dài chuỗi target khớp với số qubit
        if len(self.target_state) != self.n_qubits:
            raise ValueError(f"Target state length ({len(self.target_state)}) must match n_qubits ({self.n_qubits})")

    def get_circuit(self):
        """
        Tạo mạch Oracle. 
        Oracle này sẽ đảo pha (phase flip) trạng thái khớp với target_state.
        Đây là mô phỏng của việc kiểm tra: Hash(x) == Target_Hash?
        """
        oracle_qc = QuantumCircuit(self.n_qubits, name="ToyHash_Oracle")
        
        # Ý tưởng: Để đảo pha trạng thái |x>, ta dùng Multi-Controlled Z (MCZ).
        # Tuy nhiên, MCZ chỉ đảo pha trạng thái |11...1>.
        # Do đó, ta cần bọc các cổng X quanh các qubit có giá trị '0' trong target_state.
        
        # 1. Apply X gates to qubits that are '0' in target string
        # Lưu ý: Qiskit dùng little-endian (bit 0 là bên phải cùng), nên ta đảo ngược chuỗi để dễ xử lý
        reversed_target = self.target_state[::-1]
        
        for i, char in enumerate(reversed_target):
            if char == '0':
                oracle_qc.x(i)
        
        # 2. Apply Multi-Controlled Z gate
        # Trong Qiskit, ta có thể dùng mcp (Multi-controlled Phase) với góc PI, hoặc h-mcx-h
        # Ở đây dùng phương pháp h-mcx-h lên qubit cuối cùng để tạo hiệu ứng Z
        oracle_qc.h(self.n_qubits - 1)
        oracle_qc.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        oracle_qc.h(self.n_qubits - 1)
        
        # 3. Uncompute X gates (trả lại trạng thái cũ cho các qubit 0)
        for i, char in enumerate(reversed_target):
            if char == '0':
                oracle_qc.x(i)
                
        return oracle_qc
