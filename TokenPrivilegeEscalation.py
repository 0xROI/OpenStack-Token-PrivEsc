import requests
import sys

# Disable warnings for insecure HTTPS (optional)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_projects(auth_base_url, token):
    headers = {'X-Auth-Token': token}
    url = f"{auth_base_url}/projects"
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        return resp.json().get('projects', [])
    else:
        print(f"[-] Failed to get projects: {resp.status_code} {resp.text}")
        return []

def get_domains(auth_base_url, token):
    headers = {'X-Auth-Token': token}
    url = f"{auth_base_url}/domains"
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        return resp.json().get('domains', [])
    else:
        print(f"[-] Failed to get domains: {resp.status_code} {resp.text}")
        return []

def request_scoped_token(auth_url, token, project_id=None, domain_id=None):
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }
    scope = {}
    if project_id:
        scope['project'] = {'id': project_id}
    if domain_id:
        scope['domain'] = {'id': domain_id}
    data = {
        "auth": {
            "identity": {
                "methods": ["token"],
                "token": {"id": token}
            },
            "scope": scope if scope else None
        }
    }
    # Clean up None scope if empty
    if not scope:
        data['auth'].pop('scope')
    resp = requests.post(auth_url, json=data, headers=headers, verify=False)
    return resp

def list_servers(nova_url, token):
    headers = {'X-Auth-Token': token}
    url = f"{nova_url}/servers/detail"
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        servers = resp.json().get('servers', [])
        return servers
    return None

def main():
    print("=== OpenStack Token Privilege Escalation & Token Reuse Tester ===")
    auth_url = input("Enter Keystone Auth URL (e.g. http://openstack:5000/v3/auth/tokens): ").strip()
    token = input("Enter existing token: ").strip()

    auth_base_url = auth_url.rsplit('/auth/tokens', 1)[0]

    print("\n[+] Enumerating projects...")
    projects = get_projects(auth_base_url, token)
    print(f"Found {len(projects)} projects.")

    print("\n[+] Enumerating domains...")
    domains = get_domains(auth_base_url, token)
    print(f"Found {len(domains)} domains.")

    # Try to get scoped tokens for each project (token reuse test)
    for project in projects:
        proj_id = project['id']
        proj_name = project.get('name', 'N/A')
        print(f"\n[*] Trying to get scoped token for project '{proj_name}' ({proj_id}) ...")
        resp = request_scoped_token(auth_url, token, project_id=proj_id)
        if resp.status_code == 201:
            scoped_token = resp.headers.get('X-Subject-Token')
            print(f"[+] Success! Scoped token obtained for project '{proj_name}': {scoped_token}")

            # Attempt to list servers in this project (example chained API call)
            # User must provide or infer the Nova endpoint URL
            nova_url = input(f"Enter Nova API URL to try list servers for project '{proj_name}' (or press enter to skip): ").strip()
            if nova_url:
                servers = list_servers(nova_url, scoped_token)
                if servers is not None:
                    print(f"  Found {len(servers)} servers:")
                    for srv in servers:
                        print(f"   - {srv.get('name')} ({srv.get('id')})")
                else:
                    print("  Failed to list servers or no permission.")
        else:
            print(f"[-] Failed to get scoped token for project '{proj_name}': {resp.status_code}")

    # Domain token scoped test (optional)
    for domain in domains:
        domain_id = domain['id']
        domain_name = domain.get('name', 'N/A')
        print(f"\n[*] Trying to get scoped token for domain '{domain_name}' ({domain_id}) ...")
        resp = request_scoped_token(auth_url, token, domain_id=domain_id)
        if resp.status_code == 201:
            scoped_token = resp.headers.get('X-Subject-Token')
            print(f"[+] Success! Scoped token obtained for domain '{domain_name}': {scoped_token}")
        else:
            print(f"[-] Failed to get scoped token for domain '{domain_name}': {resp.status_code}")

if __name__ == "__main__":
    main()
