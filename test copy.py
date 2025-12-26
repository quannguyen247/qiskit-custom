import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import sys

# Global config
current_mode = 'statevector'
n_qubits = 15

def run_simulation():
    """Chạy mô phỏng với cấu hình hiện tại."""
    global current_mode, n_qubits
    print(f"\n>>> Đang chạy mô phỏng (Mode: {current_mode}, Qubits: {n_qubits}) ...")
    
    # 1. Khởi tạo mạch
    # Tạo mạch n_qubits, áp dụng cổng H cho tất cả để tạo siêu chồng chất, sau đó đo
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits)) 
    qc.measure_all()

    # 2. Khởi tạo Simulator
    try:
        simulator = AerSimulator(method=current_mode) 
    except Exception as e:
        print(f"Lỗi khởi tạo simulator: {e}")
        return

    # 3. Transpile 
    compiled_circuit = transpile(qc, simulator)

    # 4. Chạy
    # shots=1000: thực hiện đo 1000 lần
    try:
        job = simulator.run(compiled_circuit, shots=1000)
        result = job.result()

        print("Done!")
        counts = result.get_counts()
        
        # In ra một phần kết quả để tránh quá dài
        print(f"Số lượng trạng thái đo được: {len(counts)}")
        print("5 kết quả đầu tiên:", dict(list(counts.items())[:5]))
    except Exception as e:
        print(f"Lỗi trong quá trình chạy: {e}")
    print("--------------------------------------------------\n")

def change_mode():
    """Thay đổi chế độ mô phỏng."""
    global current_mode
    
    # Danh sách các mode phổ biến trong Qiskit Aer
    modes = [
        ("automatic", "Tự động chọn phương pháp tối ưu (Default)"),
        ("statevector", "Mô phỏng vector trạng thái đầy đủ (Wavefunction)"),
        ("stabilizer", "Tối ưu cho mạch Clifford (Cổng H, S, CNOT, đo lường)"),
        ("matrix_product_state", "Dùng cho mạch có entanglement thấp (MPS)"),
        ("extended_stabilizer", "Mạch Clifford + vài cổng non-Clifford"),
        ("density_matrix", "Mô phỏng ma trận mật độ (có nhiễu) - Tốn RAM"),
        ("unitary", "Tính ma trận Unitary (chỉ cho số qubit nhỏ)")
    ]
    
    print("\n--- Chọn chế độ mô phỏng (Simulation Mode) ---")
    for i, (mode, desc) in enumerate(modes, 1):
        print(f"{i}. {mode:<22} : {desc}")
    
    try:
        choice = input("Nhập số thứ tự mode muốn chọn: ")
        idx = int(choice) - 1
        if 0 <= idx < len(modes):
            current_mode = modes[idx][0]
            print(f"--> Đã chuyển sang mode: {current_mode}")
        else:
            print("Lựa chọn không hợp lệ.")
    except ValueError:
        print("Vui lòng nhập số.")
    print("----------------------------------------------\n")

def main():
    while True:
        print(f"=== Qiskit Simulator Menu (Mode: {current_mode}) ===")
        print("1. Run")
        print("2. Mode")
        print("3. Advanced Config")
        print("4. Exit")
        choice = input("Chọn chức năng: ")
        
        if choice == '1':
            run_simulation()
        elif choice == '2':
            change_mode()
        elif choice == '3':
            print("Tạm biệt!")
            sys.exit()
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại.\n")

if __name__ == "__main__":
    main()