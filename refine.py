import requests
import yaml

SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/V4ray/main/configs/CollecSHEN.txt"
OUTPUT_FILE = "CollecSHEN.yaml"

def parse_vless_url(url):
    try:
        if not url.startswith("vless://"):
            return None

        content = url[8:]
        main, remark = content.split("#") if "#" in content else (content, "Unnamed")
        userinfo, address = main.split("@")
        uuid = userinfo.split("?")[0]
        server_port, params = address.split("?", 1) if "?" in address else (address, "")
        server, port = server_port.split(":")
        network = "tcp"
        path = ""
        host = ""

        if "type=grpc" in params:
            network = "grpc"
        elif "type=ws" in params or "ws=" in params:
            network = "ws"

        for part in params.split("&"):
            if part.startswith("path="):
                path = part.split("=", 1)[1]
            if part.startswith("host="):
                host = part.split("=", 1)[1]

        proxy = {
            "name": remark.strip(),
            "type": "vless",
            "server": server,
            "port": int(port),
            "uuid": uuid,
            "tls": True,
            "network": network,
        }

        if network == "ws":
            proxy["ws-opts"] = {
                "path": path,
                "headers": {"Host": host or server}
            }
        elif network == "grpc":
            proxy["grpc-opts"] = {
                "grpc-service-name": "default"
            }

        return proxy
    except:
        return None

def generate_yaml():
    res = requests.get(SOURCE_URL)
    lines = res.text.strip().splitlines()
    proxies = []

    for line in lines:
        line = line.strip()
        if line.startswith("vless://"):
            proxy = parse_vless_url(line)
            if proxy:
                proxies.append(proxy)

    if not proxies:
        print("⛔ هیچ کانفیگ معتبری یافت نشد.")
        return

    proxy_names = [p['name'] for p in proxies]

    yaml_content = {
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "SHΞN AUTO",
                "type": "select",
                "proxies": proxy_names
            }
        ],
        "rules": [
            "MATCH,SHΞN AUTO"
        ]
    }

    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(yaml_content, f, allow_unicode=True)

    print(f"✅ Clash YAML ساخته شد ({len(proxies)} کانفیگ) → {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_yaml()
