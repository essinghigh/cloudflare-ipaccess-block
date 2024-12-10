import os
from cloudflare import Cloudflare
import requests

API_EMAIL = os.environ.get("CF_API_EMAIL")
API_KEY = os.environ.get("CF_API_KEY")
ZONE_ID = os.environ.get("CF_ZONE_ID")
ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
LIST_ID = os.environ.get("CF_LIST_ID")

client = Cloudflare(
    api_email=API_EMAIL,
    api_key=API_KEY
)

def filter_subnets(file_content):
    filtered_subnets = []
    for line in file_content.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        subnet = line.strip()
        try:
            if '/' in subnet:
                ip, prefix = subnet.split('/')
                prefix_length = int(prefix)
                if prefix_length <= 31:
                    filtered_subnets.append(subnet)
        except ValueError:
            print(f"Invalid line skipped: {line.strip()}")
    return filtered_subnets

def add_subnets_to_list(subnets, list_id, account_id):
    body = [{"ip": subnet, "comment": "AbuseIPDB"} for subnet in subnets]
    item = client.rules.lists.items.update(
        list_id=list_id,
        account_id=account_id,
        body=body,
    )
    print(f"Update operation ID: {item.operation_id}")

url = 'https://github.com/essinghigh/blocklist-abuseipdb-compressed/raw/refs/heads/main/abuseipdb-s100-120d_compressed.ipv4'
response = requests.get(url)
response.raise_for_status()

file_content = response.text
filtered_subnets = filter_subnets(file_content)
add_subnets_to_list(filtered_subnets, LIST_ID, ACCOUNT_ID)