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

## 📥 Inputs Required

- **Keystone Authentication URL**  
  e.g., `http://<openstack>:5000/v3/auth/tokens`

- **Existing Keystone Token**  
  Can be scoped or unscoped.

- **Optional Nova API URL**  
  Used to attempt server enumeration in accessible projects.

---

## ⚙️ How It Works

- Queries Keystone API using the provided token to enumerate all visible projects and domains.
- Tries to obtain new scoped tokens for each project/domain using the original token (re-authentication by reuse).
- If successful, uses the newly scoped token to access chained APIs like Nova for additional resource enumeration.

---

## 🔍 Attack Paths Explored

- 🧭 Automated discovery of other projects or domains  
- 🔁 Token reuse across tenants  
- ⛓️ Chaining with other OpenStack API calls for resource access

---

## 📌 Example Output

```text
[+] Found 3 projects in domain 'default'
[+] Attempting to scope token for project 'demo'...
[+] Success. Scoped token acquired.
[+] Nova URL provided. Fetching server list...
[+] Server: ubuntu-test (ID: abc123...)

## ⚠️ Important Notes

- **Security & Ethics**: Use only in environments where you have explicit permission.
- **SSL Warnings**: The script disables SSL certificate verification (`verify=False`) for testing convenience. Modify as needed.
- **API Endpoints**: You may need to know or enumerate other service endpoints (like Nova, Glance, Cinder) for further chaining.
- **Use Case**: This is for educational use and red team assessments of OpenStack environments.
