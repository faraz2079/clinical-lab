# FHIR Lab — Project 1: FHIR Playground

A hands-on project deploying a real FHIR R4 server (HAPI FHIR), loading synthetic
patient data (Synthea), and building a Python client that reads and writes FHIR
resources — all on Kubernetes.

Part of a 5-project upskilling plan targeting a clinical IT research role at
Universitätsklinikum Essen.

---

## What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is the modern standard for
exchanging healthcare data. Key concepts:

- **Resource**: the basic unit — Patient, Observation, Condition, Medication, etc.
- **RESTful API**: every resource type has a URL (`/fhir/Patient`, `/fhir/Observation`)
  with standard CRUD verbs (GET, POST, PUT, DELETE)
- **References**: resources link to each other — an Observation has a `subject` that
  points to a Patient (`Patient/6552`)
- **Bundle**: a collection of resources, used for transaction (write many at once)
  or searchset (search results)
- **LOINC**: standard codes for lab tests and observations (e.g. `8480-6` = Systolic
  blood pressure)
- **SNOMED CT**: standard codes for clinical findings, diagnoses, procedures

FHIR R4 is the version mandated by Germany's healthcare interoperability frameworks
(MII Kerndatensatz, ISiK, KBV Basisprofile).

---

## Stack

| Component | Version | Role |
|-----------|---------|------|
| HAPI FHIR JPA Server | v7.2.0 | FHIR R4 server |
| PostgreSQL | 15 | Persistent storage for HAPI |
| Synthea | latest | Synthetic patient data generator |
| Python + requests | 3.x | FHIR client |
| Kubernetes | v1.32 | Deployment platform |

---

## Quick Start

### Option A — Docker Compose (no Kubernetes needed)

```bash
docker compose up -d
# FHIR server available at http://localhost:8080/fhir
```

### Option B — Kubernetes

```bash
# 1. Copy and edit the secret
cp manifests/01-postgres-secret.yaml.example manifests/01-postgres-secret.yaml
nano manifests/01-postgres-secret.yaml   # set your credentials

# 2. Apply all manifests
kubectl apply -f manifests/

# 3. Wait for pods to be ready
kubectl get pods -n fhir-lab -w

# 4. Forward the port
kubectl port-forward svc/hapi-fhir 8080:8080 -n fhir-lab

# 5. Verify
curl -s http://localhost:8080/fhir/metadata | grep fhirVersion
```

---

## Loading Synthetic Data

Download and run Synthea to generate FHIR R4 Bundles:

```bash
wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
java -jar synthea-with-dependencies.jar -p 10
```

Load the generated Bundles into HAPI:

```bash
for f in ~/output/fhir/*.json; do
  echo "Loading $f"
  curl -s -X POST http://localhost:8080/fhir \
    -H "Content-Type: application/fhir+json" \
    -d @"$f" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('resourceType'), r.get('id',''))"
done
```

---

## Python Client

```bash
cd client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 fhir_client.py
```

The client demonstrates:
- `GET /fhir/Patient?gender=male` — search with query parameters
- `GET /fhir/Patient/{id}` — read a resource by ID
- `POST /fhir/Observation` — create a new resource referencing a Patient
- `GET /fhir/Observation?subject=Patient/{id}` — query by reference

---

## Manifest Structure

```
manifests/
├── 00-namespace.yaml                   # fhir-lab namespace
├── 01-postgres-secret.yaml.example     # DB credentials template (copy to .yaml, fill in)
├── 02-postgres.yaml                    # PVC + Deployment + Service for PostgreSQL 15
├── 03-hapi-configmap.yaml              # HAPI FHIR application.yaml (Spring Boot config)
└── 04-hapi-fhir.yaml                   # Deployment + Service for HAPI FHIR JPA v7.2.0
```

> `01-postgres-secret.yaml` is excluded from git. Never commit real credentials.

---

## Kubernetes Notes

- **CRI-O quirk**: Docker Hub images require the `docker.io/` prefix —
  e.g. `docker.io/hapiproject/hapi:v7.2.0`
- **Startup time**: HAPI takes ~2 minutes to start. The `startupProbe` gives it
  up to 7.5 minutes before Kubernetes marks it as failed
- **Resources**: HAPI requests 1Gi RAM, limits 2Gi

---

## The 5-Project Plan

| # | Project | Gaps closed |
|---|---------|-------------|
| 1 | **FHIR Playground** (this repo) | HL7, FHIR R4, LOINC, SNOMED, clinical IT landscape |
| 2 | CI/CD + Helm chart for a medical microservice | GitHub Actions, Helm chart authoring |
| 3 | DICOM + PACS on Kubernetes (Orthanc) | DICOM, PACS, DICOMweb |
| 4 | Hardened K8s namespace for clinical workloads | RBAC, NetworkPolicies, Sealed Secrets, Falco, DSGVO |
| 5 | GitOps capstone (ArgoCD) | GitOps, staging/prod environments |
