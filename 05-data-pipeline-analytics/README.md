# AURA-X 2.0 — Data Pipeline & Analytics

## Purpose
CSV profiling, basic validation and descriptive statistics for data supplied by the user.

## Important status
This is a **starter service**, not a complete production AI system. It does not include API keys, paid model access, a live agent swarm, or a deployed cloud service. Connectors and authentication must be configured and security-reviewed before internet exposure.

## Requirements
- Python 3.11 or newer (recommended: 3.12/3.13 for broad package compatibility)
- Internet only for installing dependencies and any online integrations
- Windows, macOS, or Linux

## Run locally
1. Extract this ZIP into a separate folder.
2. Install Python and confirm `python --version`.
3. Open a terminal in this folder.
4. Create a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Start the service: `uvicorn app:app --host 127.0.0.1 --port 8105`
7. Open `http://127.0.0.1:8105/docs` in your browser.
8. Health check: `http://127.0.0.1:8105/health`

## Environment configuration
Copy `.env.example` to `.env` if you later add a dotenv loader or deployment-specific environment variables. Do not place real credentials in source code or upload them to GitHub. This starter does not automatically load `.env`.

## Deploying to a cloud host
- Create a separate repository for this package.
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Configure secrets in the hosting provider's environment settings, not in Git.
- Add authentication, HTTPS, request limits, audit logging, and a trusted admin identity before public deployment.
- Free hosting limits, sleep behavior, RAM, CPU, and availability depend on the provider and can change.

## Security and integration
- Do not use multiple accounts to evade provider quotas or access restrictions.
- Use only authorized API accounts, approved MCP servers, and permitted data sources.
- Keep admin-only operations behind authentication and role-based access.
- Do not expose this starter service publicly without adding authentication and network controls.
- Treat web pages and retrieved documents as untrusted input.
- Paid services require explicit project-owner approval.

## Roadmap
1. Test the service locally.
2. Add authentication and persistent audit records.
3. Define an authenticated service-to-service contract.
4. Connect this service to the central orchestrator.
5. Add automated tests and observability.
6. Review privacy, retention, backup, and deployment settings.

## License
No third-party model, website, API, or media rights are granted by this starter. Choose a license for your own code before public distribution.
