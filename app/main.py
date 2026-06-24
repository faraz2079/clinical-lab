from flask import Flask, request, jsonify
import fhir_client

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/patients")
def list_patients():
    params = request.args.to_dict()
    bundle = fhir_client.search_patients(**params)
    patients = fhir_client.get_bundle_entries(bundle)
    return jsonify({"total": bundle.get("total", 0), "patients": patients})


@app.route("/patients/<patient_id>")
def get_patient(patient_id):
    patient = fhir_client.get_patient(patient_id)
    return jsonify(patient)


@app.route("/observations", methods=["POST"])
def create_observation():
    body = request.get_json()
    obs = fhir_client.create_observation(
        patient_id=body["patient_id"],
        loinc_code=body["loinc_code"],
        display=body["display"],
        value=body["value"],
        unit=body["unit"],
    )
    return jsonify(obs), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
