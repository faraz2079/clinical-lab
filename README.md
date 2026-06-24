# Project 2 — CI/CD + Helm Chart for a Medical Microservice

A Flask HTTP API that wraps a FHIR R4 client, containerized and deployed to
Kubernetes via a Helm chart, with a GitHub Actions CI pipeline.

---

## What it does

Exposes four endpoints over HTTP:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/patients` | Search patients (query params forwarded to FHIR) |
| GET | `/patients/<id>` | Read a patient by ID |
| POST | `/observations` | Create a new FHIR Observation |

The API talks to a HAPI FHIR R4 server. The base URL is configured via the
`FHIR_BASE_URL` environment variable.

---

## Stack

- Python 3.12 + Flask
- Docker image: `ghcr.io/faraz2079/fhir-client:latest`
- Kubernetes + Helm
- GitHub Actions CI (builds and pushes image on every push to `project-2/**`)

---

## Deploy with Helm

```bash
# Create pull secret (one-time)
kubectl create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=faraz2079 \
  --docker-password=$(gh auth token) \
  -n fhir-lab

# Install
helm install fhir-client helm/fhir-client -n fhir-lab

# Verify
kubectl get pods -n fhir-lab
kubectl port-forward svc/fhir-client 5001:5001 -n fhir-lab
curl http://localhost:5001/health
```

---

## CI Pipeline

`.github/workflows/ci-project2.yaml` triggers on pushes that change `project-2/app/**`,
`project-2/Dockerfile`, or the workflow file itself. Builds the Docker image and pushes
it to `ghcr.io/faraz2079/fhir-client:latest`.
