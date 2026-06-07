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

## Session 2 — 
