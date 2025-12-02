# 🚀 4.5 Deployment & Infra Specification

## Purpose
Define WHAT the deployment layer must produce.

## Functional Requirements

1. Book deployment:
   - MUST deploy to **GitHub Pages**
   - OPTIONAL: Vercel deployment preset

2. Backend deployment:
   - MUST include:
     - `Dockerfile`
     - `docker-compose.yml`
     - `.env` template

3. MUST generate:
   - Public UI URL
   - Public Backend URL

4. Environment variables MUST be handled safely.

## Non-Functional
- Easy reproduction: Project setup and deployment can be fully reproduced with a single `docker-compose up` command or equivalent script.
- Simple onboarding: A `SETUP.md` document provides clear, step-by-step instructions for new developers to get the project running locally.
- Deployment steps clearly documented: All deployment steps for both UI and backend are comprehensively detailed in `DEPLOYMENT.md`.
