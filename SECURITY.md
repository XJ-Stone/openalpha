# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in OpenAlpha, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email the maintainers directly or use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability).

### What to include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix or mitigation**: Depends on severity, but we aim for 30 days for critical issues

## Scope

This policy covers the OpenAlpha codebase, including:

- Backend API (`backend/`)
- Frontend application (`frontend/`)
- Data ingestion pipeline (`backend/ingestion/`)

This policy does **not** cover:

- Third-party dependencies (report to the respective projects)
- The content of investor knowledge base files (`investors/`)

## API Keys and Secrets

- Never commit API keys, tokens, or credentials to the repository
- Use `.env` files for local configuration (`.env` is in `.gitignore`)
- See `.env.example` for the expected environment variables
