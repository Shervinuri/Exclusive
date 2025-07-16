import re, os, socket, requests, concurrent.futures

SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/V4ray/main/configs/CollecSHEN.txt"
OUTPUT_FILE = "configs/Шервин.txt"
REMARK = "☬SHΞN™"

# پرچم کشور بر اساس کد
FLAG_MAP = {
    "ir": "🇮🇷", "de": "🇩🇪", "us": "🇺🇸", "nl": "🇳🇱",
    "fr": "🇫🇷", "gb": "🇬🇧", "tr": "🇹🇷", "sg": "🇸🇬",
    "in": "🇮🇳", "ru": "🇷🇺", "jp": "🇯🇵", "cn": "🇨🇳",
    "ca": "🇨🇦", "ae": "🇦🇪", "kz": "🇰🇿", "ua": "🇺🇦"
}

def extract_vless_configs(text):
    return [line.strip() for line in text.strip().splitlines() if line.startswith("vless://")]

def test_config(host, port, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except:
        return False

def extract_info(config):
    try:
        main = config.split("vless://")[1]
        server_part = main.split("@")[1].split("?")[0]
        host, port = server_part.split(":")
        params = main.split("?")[1] if "?" in main else ""
        flow = "grpc" if "type=grpc" in params else "ws" if "ws" in params else "tcp"
        return host, port, flow
    except:
        return None, None, "♻️"

def get_country_flag(host):
    try:
        r = requests.get(f"https://ipapi.co/{hos🔄t}/country/", timeout=3)
        code = r.text.strip().lower()
        return FLAG_MAP.get(code, "🏳️")
    except:
        return "ناکجا آباد 🏳️"

def remodify(config):
    host, port, flow = extract_info(config)
    flag = get_country_flag(host) if host else "🏳️"
    return config.split('#')[0] + f"#{REMARK} {flag} {flow}"

def is_config_alive(config):
    host, port, _ = extract_info(config)
    return test_config(host, port) if host and port else False

def main():
    os.makedirs("configs", exist_ok=True)

    # پیام تبلیغاتی اول
    banner = (
        "درود بر یاران جان\n"
        "شروین ۱۰ دقیقه دیگه\n"
        "مجدد این لیست رو آپدیت میکنه پس اگر کانفیگ خوبی پیدا کردی منتقل کن یجا دیگه چون ممکنه\n"
        "که این بره یکی بهتر بیاد جاش 😁"
    )

    print("🔗 Downloading source configs...")
    try:
        res = requests.get(SOURCE_URL, timeout=10)
        raw_text = res.text
    except:
        print("❌ Failed to download source list.")
        return

    configs = extract_vless_configs(raw_text)
    print(f"🔍 Found {len(configs)} vless configs")

    print("🧪 Testing health of each config...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(is_config_alive, configs))

    alive_configs = [c for c, ok in zip(configs, results) if ok]
    print(f"✅ {len(alive_configs)} configs passed health check")

    final_configs = [remodify(c) for c in alive_configs]

    with open(OUTPUT_FILE, 'w') as f:
        f.write(banner + "\n")
        for c in final_configs:
            f.write(c + "\n")

    print(f"🚀 Done. Saved {len(final_configs)} configs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
