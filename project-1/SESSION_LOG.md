# Session Log — FHIR Lab

---

## Session 1 — 2026-06-05

### Accomplished

- **Phase 1 (FHIR concepts):** Covered the core mental model — resources, RESTful
  API pattern, references, Bundles, LOINC vs SNOMED CT, and German clinical IT
  context (MII Kerndatensatz, ISiK, KBV Basisprofile).

- **Phase 0 (cluster check):** Single-node K8s v1.32 on Ubuntu 24.04 Proxmox VM.
  No control-plane taint. Calico CNI healthy. `local-path` storage class default.
  No ingress controller (using port-forward). Identified CRI-O 1.24.6 quirk:
  Docker Hub images require `docker.io/` prefix.

- **Phase 2 (deploy PostgreSQL):** Namespace `fhir-lab` created. PostgreSQL 15
  deployed via Deployment + PVC (10Gi, local-path) + Service. Pod Running, PVC Bound.

- **Phase 2 (deploy HAPI FHIR):** ConfigMap with `application.yaml` (Spring Boot
  config, PostgreSQL datasource, FHIR R4). Deployment + Service applied.
  Fixed three issues along the way:
  1. YAML block scalar indentation bug in the ConfigMap (`hapi:` not aligned with `spring:`)
  2. `matchlabels` → `matchLabels` (case-sensitive Kubernetes field)
  3. CRI-O short-name resolution: changed image to `docker.io/hapiproject/hapi:v7.2.0`

### Status at end of session

All Phase 2 issues resolved. HAPI FHIR confirmed healthy:
`curl /fhir/metadata` returned `"fhirVersion": "4.0.1"`, HAPI 7.2.0. Both
pods (`postgres`, `hapi-fhir`) running in `fhir-lab` namespace.

Phase 3 started: Synthea downloaded and run (`-p 10`), generated 10 patient
Bundles + `hospitalInformation` + `practitionerInformation` in `~/output/fhir/`.
Bundle loading into HAPI started but left running in background via
`nohup ~/load-fhir.sh` to survive logout. Progress in `~/fhir-load.log`.

---

### TODO — Next Session

- [ ] Check `~/fhir-load.log` — confirm all 12 Bundles loaded without errors
- [ ] Verify data: `curl "http://localhost:8080/fhir/Patient?_count=10"` (after port-forward)
- [ ] **Phase 4:** Build Python FHIR client
  - Read a Patient by ID
  - Search patients by name / gender / birthdate
  - Create a new Observation referencing an existing Patient
  - Parse and iterate a searchset Bundle
- [ ] Containerize the Python client (sets up Project 2)

---

## Session 2 — 2026-06-07

### Accomplished

- **Phase 3 (load synthetic data):** Debugged background nohup load — port-forward
  had died silently, so all bundles failed. Re-ran load in foreground. One patient
  (Ahmad985) hit a conflict from a prior partial attempt; 10/10 others loaded
  successfully. Verified with `curl /fhir/Patient?_count=10` → `total: 10`.

- **Phase 4 (Python FHIR client):** Built `client/fhir_client.py` with:
  - `search_patients(**params)` — search by gender, name, birthdate
  - `get_patient(patient_id)` — read by ID
  - `create_observation(...)` — POST a new Observation with LOINC code referencing a Patient
  - `get_bundle_entries(bundle)` — parse searchset Bundle entries
  - Successfully created `Observation/12959` (systolic BP 118 mm[Hg]) for Patient/6552
    and verified it via `GET /fhir/Observation/12959`

- **Phase 5 (GitHub repo):** Restructured project into `~/clinical-lab/` with
  per-project subdirectories. Created GitHub repo `clinical-lab` with:
  - `main` branch: full directory structure + overview README
  - `project-1` branch: project-1 files at root level (via `git subtree push`)
  - `.gitignore` excluding `01-postgres-secret.yaml` (real credentials)
  - `01-postgres-secret.yaml.example` committed as safe template
  - `docker-compose.yml` for running HAPI + PostgreSQL without Kubernetes
  - Rewrote `README.md` as a proper GitHub README (FHIR concepts, quick start,
    both Docker Compose and K8s options, manifest structure, 5-project plan table)

### Status at end of session

**Project 1 complete.** All 5 phases done. Repo live on GitHub (`clinical-lab`,
`project-1` branch). Old `~/fhir-lab/` directory removed.

---

### TODO — Next Session

- [ ] **Project 2:** CI/CD + Helm chart for a medical microservice
  - Containerize the Python FHIR client (Dockerfile)
  - Write a Helm chart for it
  - Set up GitHub Actions CI pipeline
  - Deploy to K8s via the Helm chart

---

## Session 3 — 2026-06-24

### Accomplished

- **Project 2 complete:** CI/CD + Helm chart for a medical microservice.

- **Flask API:** Wrapped the Project 1 Python FHIR client in a Flask HTTP API (`main.py`)
  with four endpoints: `GET /health`, `GET /patients`, `GET /patients/<id>`, `POST /observations`.
  Fixed port conflict (5000 → 5001).

- **Dockerfile:** Containerized the Flask app (`python:3.12-slim`). User wrote the Dockerfile
  manually for learning. Image built and pushed to `ghcr.io/faraz2079/fhir-client:latest`.

- **Helm chart:** Authored a full Helm chart (`helm/fhir-client/`) with `Chart.yaml`,
  `values.yaml`, `templates/deployment.yaml`, `templates/service.yaml`. Includes
  readiness/liveness probes on `/health` and `imagePullSecrets` for CRI-O.

- **K8s deploy:** Deployed via `helm install`. Pod reached 1/1 Running. Verified
  `GET /health`, `GET /patients?gender=male&_count=3` via port-forward.

- **GitHub Actions CI:** Wrote `.github/workflows/ci-project2.yaml` — triggers on push
  to `project-2/**`. Builds and pushes image to ghcr.io on every commit.
  Fixed two issues: typo in `actions/checkout`, then `write_package` permission denial
  (resolved by using a Classic PAT stored as `GHCR_TOKEN` secret).
  Narrowed path filter to `project-2/app/**` and `project-2/Dockerfile` so README
  edits don't trigger unnecessary image rebuilds.

- **`project-2` branch:** Pushed project-2 subtree to its own branch on GitHub.

### Status at end of session

**Project 2 complete.** Flask FHIR API running in K8s, Helm chart authored, CI pipeline
green. Repo has `main`, `project-1`, and `project-2` branches live on GitHub.

---

### TODO — Next Session

- [ ] **Project 3:** DICOM + PACS on Kubernetes (Orthanc)
  - Deploy Orthanc PACS to K8s
  - Upload a DICOM file via DICOMweb
  - Query and retrieve it

