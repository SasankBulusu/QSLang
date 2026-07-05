from constants import MAX_QUBITS, ALLOWED_GATES, INIT_KEYWORD

def tokenize(script: str) -> list[str]:
    """Raw NQL script to indivigual instruction tokens"""
    lines = script.strip().split("\n")
    tokens = []
    for line in lines:
        clean = line.strip()
        if clean:
            tokens.append(clean)
    return tokens

def validate_and_parse(tokens: list[str]) -> tuple[list[dict], str, int]:
    """ Validates tokens and converts it to payload"""
    if not tokens:
        return [], "Error: Script is empty. Start with INIT <number>.", 0
    first = tokens[0].split()
    if first[0] != INIT_KEYWORD:
        return [], f"Error on Line 1: Expected 'INIT <number>' but got '{tokens[0]}'.", 0

    if len(first) != 2:
        return [], "Error on Line 1: INIT requires exactly one number. Example: INIT 3", 0

    try:
        num_qubits = int(first[1])
    except ValueError:
        return [], f"Error on Line 1: '{first[1]}' is not a valid number.", 0

    if num_qubits < 1 or num_qubits > MAX_QUBITS:
        return [], f"Error on Line 1: Qubit count must be between 1 and {MAX_QUBITS}. Got {num_qubits}.", 0
    
    # Parsing
    payload = []
    for i, token in enumerate(tokens[1:], start=2):  # line numbers start from 2
        parts = token.split()

        if len(parts) != 2:
            return [], f"Error on Line {i}: Each gate instruction must be 'GATE QUBIT'. Got '{token}'.", 0

        gate, qubit_str = parts[0], parts[1]

        if gate not in ALLOWED_GATES:
            return [], f"Error on Line {i}: '{gate}' is not a valid gate. Valid gates: {ALLOWED_GATES}", 0

        try:
            qubit = int(qubit_str)
        except ValueError:
            return [], f"Error on Line {i}: '{qubit_str}' is not a valid qubit number.", 0

        if qubit < 0 or qubit >= num_qubits:
            return [], f"Error on Line {i}: Qubit {qubit} does not exist. You only have qubits 0 to {num_qubits - 1}.", 0

        if gate == "CNOT" and qubit == 0:
            return [], f"Error on Line {i}: CNOT on qubit 0 is invalid. CNOT needs a control qubit before it (qubit must be >= 1).", 0

        payload.append({"gate": gate, "target": qubit})

    return payload, "", num_qubits

if __name__ == "__main__":
    test_script = """
    INIT 3
    H 0
    CNOT 1
    X 5
    """
    tokens = tokenize(test_script)
    print("Tokens:", tokens)
    payload, error, qubits = validate_and_parse(tokens)
    print("Payload:", payload)
    print("Error:", error)