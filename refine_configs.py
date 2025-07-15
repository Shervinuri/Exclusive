import requests import os

SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/V4ray/main/configs/CollecSHEN.txt" OUTPUT_FILE = "configs/Шервин.txt" REMARK = "☬SHΞN™" TEST_URL = "https://www.google.com/generate_204"

def is_config_alive(config): try: if config.startswith("vmess://") or config.startswith("vless://") or config.startswith("ss://"): r = requests.get(TEST_URL, timeout=3) return r.status_code == 204 except: return False

def fetch_configs(): try: res = requests.get(SOURCE_URL, timeout=15) if res.status_code == 200: return res.text.strip().splitlines() except: pass return []

def main(): os.makedirs("configs", exist_ok=True) lines = fetch_configs() all_configs = []

for line in lines:
    line = line.strip()
    if not line.startswith(('vmess://', 'vless://', 'ss://')):
        continue
    if '#' in line:
        line = line.split('#')[0]
    line = line + '#' + REMARK
    if is_config_alive(line):
        print("✅ Alive")
        all_configs.append(line)
    else:
        print("❌ Dead")

all_configs = list(dict.fromkeys(all_configs))

with open(OUTPUT_FILE, 'w') as f:
    for c in all_configs:
        f.write(c + '\n')

print(f"💾 Saved {len(all_configs)} alive configs to {OUTPUT_FILE}")

if name == "main": main()

