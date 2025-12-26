import sys
import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator

# Import modules từ src
from src.sphincs_sim.oracle import ToyHashOracle
from src.sphincs_sim.grover import GroverAttack

def main():
    print("============================================================")
    print("   MÔ PHỎNG TẤN CÔNG PRE-IMAGE TRÊN SPHINCS+ (TOY MODEL)    ")
    print("   Kỹ thuật: Grover's Algorithm                             ")
    print("============================================================")
    
    # 1. Cấu hình bài toán
    # SPHINCS+ thực tế dùng SHA-256 (256 bits). 
    # Với máy tính lượng tử hiện tại và simulator, ta chỉ mô phỏng "Toy Hash"
    # Ta dùng 12 qubits cho không gian tìm kiếm (Search Space = 4096)
    # Để đảm bảo chạy nhanh trên Laptop.
    
    N_QUBITS = 12 
    
    # Giả sử ta biết Hash(Secret) và muốn tìm lại Secret.
    # Trong mô phỏng này, ta chọn trước Secret để tạo Oracle.
    # Secret ngẫu nhiên 12 bit.
    secret_int = np.random.randint(0, 2**N_QUBITS)
    secret_bin = format(secret_int, f'0{N_QUBITS}b')
    
    print(f"[+] Cấu hình:")
    print(f"    - Số Qubits: {N_QUBITS}")
    print(f"    - Không gian tìm kiếm: {2**N_QUBITS}")
    print(f"    - Secret Key (Target) cần tìm: {secret_bin} (Decimal: {secret_int})")
    print("-" * 60)

    # 2. Xây dựng Oracle (Hàm Hash giả lập)
    print("[+] Đang xây dựng Oracle (Black Box)...")
    oracle = ToyHashOracle(N_QUBITS, secret_bin).get_circuit()

    # 3. Xây dựng mạch Grover
    print("[+] Đang xây dựng mạch Grover...")
    grover = GroverAttack(oracle, N_QUBITS)
    qc, iterations = grover.build_circuit()

    # 4. Chạy mô phỏng
    print(f"[+] Bắt đầu chạy mô phỏng trên AerSimulator (Method: automatic)...")
    simulator = AerSimulator(method='automatic')
    
    # Transpile
    compiled_qc = transpile(qc, simulator)
    
    # Run
    shots = 1024
    job = simulator.run(compiled_qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # 5. Phân tích kết quả
    print("-" * 60)
    print("[+] KẾT QUẢ TẤN CÔNG:")
    
    # Sắp xếp kết quả theo số lần xuất hiện giảm dần
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    
    top_candidate = sorted_counts[0][0]
    top_count = sorted_counts[0][1]
    probability = (top_count / shots) * 100
    
    print(f"    - Ứng viên số 1 (Found): {top_candidate}")
    print(f"    - Độ tin cậy: {probability:.2f}% ({top_count}/{shots} shots)")
    
    if top_candidate == secret_bin:
        print("\n>>> THÀNH CÔNG! Đã tìm ra Pre-image của hàm Hash.")
        print(">>> Đây là minh chứng cho việc Grover giảm độ phức tạp từ O(N) xuống O(sqrt(N)).")
    else:
        print("\n>>> THẤT BẠI. Có thể do nhiễu hoặc số lần lặp chưa tối ưu.")

if __name__ == "__main__":
    main()
