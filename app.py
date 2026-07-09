from flask import Flask, render_template, request
from parser_engine import tokenize, validate_and_parse
from quantum_bridge import build_circuit, get_ascii_diagram
from ai_tutor import get_ai_explanation

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Show the main editor page."""
    return render_template("index.html")


@app.route("/compile", methods=["POST"])
def compile_nql():
    """
    Receives the NQL script from the form.
    Runs the full pipeline.
    Sends results to the result page.
    """
    # Get the script from the HTML form
    script = request.form.get("nql_script", "")

    # Run the parser
    tokens = tokenize(script)
    payload, error, num_qubits = validate_and_parse(tokens)

    circuit_diagram = ""
    if not error and payload:
        circuit = build_circuit(payload, num_qubits)
        circuit_diagram = get_ascii_diagram(circuit)

    # Get AI explanation
    ai_explanation = get_ai_explanation(payload, error)

    return render_template(
        "result.html",
        script=script,
        error=error,
        circuit_diagram=circuit_diagram,
        ai_explanation=ai_explanation,
        payload=payload,
        num_qubits=num_qubits
    )


if __name__ == "__main__":
    app.run(debug=True)
