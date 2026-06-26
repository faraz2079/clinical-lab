import requests

BASE_URL = "http://localhost:8042"
AUTH = ("orthanc", "orthanc")


def upload_dicom(filepath):
    with open(filepath, "rb") as f:
        r = requests.post(f"{BASE_URL}/instances", data=f.read(),
                          headers={"Content-Type": "application/dicom"}, auth=AUTH)
    r.raise_for_status()
    return r.json()


def list_studies():
    r = requests.get(f"{BASE_URL}/studies", auth=AUTH)
    r.raise_for_status()
    return r.json()


def get_study(study_id):
    r = requests.get(f"{BASE_URL}/studies/{study_id}", auth=AUTH)
    r.raise_for_status()
    return r.json()


def list_instances():
    r = requests.get(f"{BASE_URL}/instances", auth=AUTH)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    print("=== Upload DICOM ===")
    result = upload_dicom("sample.dcm")
    print(f"  Status : {result['Status']}")
    print(f"  ID     : {result['ID']}")

    print("\n=== List Studies ===")
    studies = list_studies()
    for sid in studies:
        study = get_study(sid)
        tags = study["MainDicomTags"]
        patient = study["PatientMainDicomTags"]
        print(f"  Patient : {patient['PatientName']} ({patient['PatientID']})")
        print(f"  Study   : {tags['StudyDescription']} on {tags['StudyDate']}")
        print(f"  ID      : {sid}")

    print("\n=== List Instances ===")
    instances = list_instances()
    print(f"  Total instances in Orthanc: {len(instances)}")
