from qiskit import QuantumCircuit

def build_circuit(payload: list[dict], no_qubits: int):
    circuit = QuantumCircuit(no_qubits)
    for instruction in payload:
        gate = instruction["gate"]
        target = instruction["target"]

        if gate == "H":
            circuit.h(target)          # Hadamard gate: creates superposition
        elif gate == "X":
            circuit.x(target)          # Pauli-X: quantum NOT gate (flips qubit)
        elif gate == "Y":
            circuit.y(target)          # Pauli-Y: phase + flip
        elif gate == "Z":
            circuit.z(target)          # Pauli-Z: phase flip
        elif gate == "CNOT":
            control = target - 1       # Control qubit is always one below target
            circuit.cx(control, target)  

    return circuit

def get_ascii_diagram(circuit: QuantumCircuit) -> str:
    # Returns a single line string that is dispayable on a webpage.
    return circuit.draw(output="text").single_string()

if __name__ == "__main__":
    test_payload = [
        {"gate": "H", "target": 0},
        {"gate": "CNOT", "target": 1}
    ]
    circuit = build_circuit(test_payload, 2)
    print(get_ascii_diagram(circuit))