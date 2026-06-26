# Project 3 — DICOM + PACS on Kubernetes (Orthanc)

Deploy an Orthanc PACS server to Kubernetes, upload a DICOM image via the REST API,
and query it back programmatically.

---

## What it does

- Runs Orthanc (open-source PACS) in Kubernetes with persistent storage
- Generates a synthetic DICOM CT file with Python
- Uploads it to Orthanc via `POST /instances`
- Queries studies and instances back via the Orthanc REST API

---

## Key concepts

- **DICOM** — the standard file format for medical images (MRI, CT, X-ray)
- **PACS** — Picture Archiving and Communication System; the server that stores and serves medical images in a hospital
- **Orthanc** — lightweight open-source PACS server with a REST API and DICOMweb support

---

## Stack

- Orthanc (`jodogne/orthanc-plugins`) running in Kubernetes
- Python + pydicom for generating and uploading DICOM files
- Helm chart for repeatable deployment

---

## Deploy with Helm

```bash
# Create namespace
kubectl create namespace dicom-lab

# Install
helm install orthanc helm/orthanc -n dicom-lab

# Verify
kubectl get pods -n dicom-lab
kubectl port-forward svc/orthanc 8042:8042 -n dicom-lab
curl -u orthanc:orthanc http://localhost:8042/system
```

---

## Upload and query a DICOM file

```bash
# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate a synthetic DICOM file
python generate_dicom.py

# Run the client (upload + query)
python dicom-client.py
```
