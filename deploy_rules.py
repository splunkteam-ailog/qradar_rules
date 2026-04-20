import requests
import json
import urllib3
import os

urllib3.disable_warnings()

QRADAR_HOST = os.environ.get("QRADAR_HOST", "https://16.16.213.68")
SEC_TOKEN = os.environ.get("QRADAR_TOKEN", "c2cde311-a18c-4b30-9ba1-c024c7a6c51a")

headers = {
    "SEC": SEC_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Version": "16.0"
}

windows_rules = [
    100069, 100071, 100057, 100059,
    100061, 100067, 100116, 100081,
    100082, 100256
]

success = 0
errors = 0

for rule_id in windows_rules:
    get_resp = requests.get(
        f"{QRADAR_HOST}/api/analytics/rules/{rule_id}",
        headers=headers,
        verify=False
    )

    if get_resp.status_code != 200:
        print(f"ERR GET [{rule_id}] -> {get_resp.status_code}")
        errors += 1
        continue

    rule = get_resp.json()
    rule_name = rule.get("name", "")
    rule["enabled"] = True

    post_resp = requests.post(
        f"{QRADAR_HOST}/api/analytics/rules/{rule_id}",
        headers=headers,
        json=rule,
        verify=False
    )

    if post_resp.status_code == 200:
        print(f"OK [{rule_id}] {rule_name}")
        success += 1
    else:
        print(f"ERR [{rule_id}] {rule_name} -> {post_resp.status_code}")
        errors += 1

print(f"=== Готово: {success} OK, {errors} ошибок ===")
