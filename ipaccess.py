import os
import requests
from cloudflare import Cloudflare

client = Cloudflare(api_email=os.environ["CF_API_EMAIL"], api_key=os.environ["CF_API_KEY"])

def filter_subnets(content):
    return [line.strip() for line in content.splitlines() if line and not line.startswith('#') and int(line.split('/')[1]) <= 31]

url = 'https://github.com/essinghigh/blocklist-abuseipdb-compressed/raw/refs/heads/main/abuseipdb-s100-120d_compressed.ipv4'
response = requests.get(url)
response.raise_for_status()

subnets = filter_subnets(response.text)
item = client.rules.lists.items.update(
    list_id=os.environ["CF_LIST_ID"],
    account_id=os.environ["CF_ACCOUNT_ID"],
    body=[{"ip": subnet, "comment": "AbuseIPDB"} for subnet in subnets]
)
print(f"Update operation ID: {item.operation_id}")
