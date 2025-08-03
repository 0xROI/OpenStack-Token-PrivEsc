# OpenStack Token Privilege Escalation & Token Reuse Tester

A Python script to automate discovery of OpenStack projects and domains, test token reuse for privilege escalation, and chain with other OpenStack API calls (e.g., list servers).  
Designed for **educational and authorized security testing** of OpenStack deployments.

---

## Features

- Enumerates projects and domains using an existing Keystone token.
- Attempts to reuse the token to request scoped tokens for each project/domain.
- Supports chaining with other OpenStack service APIs (example: Nova servers list).
- Helps identify privilege escalation and token abuse vulnerabilities in multi-tenant OpenStack environments.

---

## Requirements

- Python 3.x
- `requests` library

Install dependencies with:

```bash
pip install requests
