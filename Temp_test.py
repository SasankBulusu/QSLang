from parser_engine import tokenize, validate_and_parse
from quantum_bridge import build_circuit, get_ascii_diagram
from ai_tutor import get_ai_explanation

def run_test(script):
    print("=" * 50)
    print("INPUT SCRIPT:")
    print(script.strip())
    print("=" * 50)

    # Step 1: Parse
    tokens = tokenize(script)
    payload, error, num_qubits = validate_and_parse(tokens)

    if error:
        print("COMPILATION ERROR:", error)
        ai_response = get_ai_explanation([], error)
    else:
        # Step 2: Build circuit
        circuit = build_circuit(payload, num_qubits)
        diagram = get_ascii_diagram(circuit)
        print("CIRCUIT DIAGRAM:")
        print(diagram)
        ai_response = get_ai_explanation(payload, "")

    print("\nAI TUTOR SAYS:")
    print(ai_response)
    print()

# Test 1: Valid Bell State circuit
run_test("""
INIT 2
H 0
CNOT 1
""")

# Test 2: Invalid — qubit out of range
run_test("""
INIT 2
H 5
""")

# Test 3: Missing INIT
run_test("""
H 0
X 1
""")