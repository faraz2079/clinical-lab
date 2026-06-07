# Clinical Lab — K8s Upskilling Plan

5 hands-on projects to close the gap between a DevOps background and a clinical
IT research role at Universitätsklinikum Essen.

Each project lives in its own branch on this repo.

---

## Projects

| # | Branch | Project | Gaps closed |
|---|--------|---------|-------------|
| 1 | `project-1` | **FHIR Playground** | HL7, FHIR R4, LOINC, SNOMED, clinical IT landscape |
| 2 | `project-2` | CI/CD + Helm chart for a medical microservice | GitHub Actions, Helm chart authoring |
| 3 | `project-3` | DICOM + PACS on Kubernetes (Orthanc) | DICOM, PACS, DICOMweb |
| 4 | `project-4` | Hardened K8s namespace for clinical workloads | RBAC, NetworkPolicies, Sealed Secrets, Falco, DSGVO |
| 5 | `project-5` | GitOps capstone (ArgoCD) | GitOps, staging/prod environments |

---

## Structure

Each branch contains only that project's files at the root level.
Switch branches on GitHub to browse individual projects.

Locally, all projects live under subdirectories:

```
clinical-lab/
├── project-1/    ← FHIR Playground (HAPI FHIR + PostgreSQL on K8s)
├── project-2/    ← coming soon
├── project-3/    ← coming soon
├── project-4/    ← coming soon
└── project-5/    ← coming soon
```
