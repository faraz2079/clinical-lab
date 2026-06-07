import requests
import json

BASE_URL = "http://localhost:8080/fhir"
HEADERS = {"Content-Type": "application/fhir+json"}


def get_patient(patient_id):
    r = requests.get(f"{BASE_URL}/Patient/{patient_id}", headers=HEADERS)
    r.raise_for_status()
    return r.json()


def search_patients(**params):
    r = requests.get(f"{BASE_URL}/Patient", params=params, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_bundle_entries(bundle):
    return [e["resource"] for e in bundle.get("entry", [])]


def create_observation(patient_id, loinc_code, display, value, unit):
    obs = {
        "resourceType": "Observation",
        "status": "final",
        "subject": {"reference": f"Patient/{patient_id}"},
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": loinc_code,
                    "display": display,
                }
            ]
        },
        "valueQuantity": {
            "value": value,
            "unit": unit,
            "system": "http://unitsofmeasure.org",
            "code": unit,
        },
    }
    r = requests.post(f"{BASE_URL}/Observation", json=obs, headers=HEADERS)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    # 1. Search patients
    print("=== Search: male patients ===")
    bundle = search_patients(gender="male", _count=3)
    patients = get_bundle_entries(bundle)
    for p in patients:
        name = p["name"][0]
        print(f"  {p['id']} | {name['family']}, {name['given'][0]} | {p.get('birthDate')}")

    # 2. Read first patient by ID
    first_id = patients[0]["id"]
    print(f"\n=== Read patient {first_id} ===")
    patient = get_patient(first_id)
    print(f"  Name   : {patient['name'][0]['family']}, {patient['name'][0]['given'][0]}")
    print(f"  Gender : {patient.get('gender')}")
    print(f"  DOB    : {patient.get('birthDate')}")

    # 3. Create an Observation for that patient
    print(f"\n=== Create Observation for patient {first_id} ===")
    obs = create_observation(
        patient_id=first_id,
        loinc_code="8480-6",
        display="Systolic blood pressure",
        value=118,
        unit="mm[Hg]",
    )
    print(f"  Created: {obs['resourceType']}/{obs['id']}")
    print(f"  Status : {obs['status']}")
    print(f"  Value  : {obs['valueQuantity']['value']} {obs['valueQuantity']['unit']}")

    # 4. Verify - search observations for this patient
    print(f"\n=== Observations for patient {first_id} ===")
    obs_bundle = requests.get(
        f"{BASE_URL}/Observation",
        params={"subject": f"Patient/{first_id}", "_count": 3},
        headers=HEADERS,
    ).json()
    for o in get_bundle_entries(obs_bundle):
        code = o["code"]["coding"][0]["display"]
        val = o.get("valueQuantity", {})
        print(f"  {code}: {val.get('value')} {val.get('unit')}")
