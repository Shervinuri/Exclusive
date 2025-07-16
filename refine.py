import requests, base64, socket, re, os

SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/V4ray/main/configs/CollecSHEN.txt"
OUTPUT_FILE = "configs/Шервин.txt"
REMARK = "☬SHΞN™"
MSG = (
    "درود بر یاران جان\n"
    "شروین ۱۰ دقیقه دیگه\n"
    "مجدد این لیست رو آپدیت میکنه\n"
    "پس اگر کانفیگ خوبی پیدا کردی منتقل کن یجا دیگه\n"
    "چون ممکنه که این بره یکی بهتر بیاد جاش\n😁\n"
)

def extract_vless(text):
    vless_list = []
    for line in text.strip().splitlines():
        if line.startswith("vless://"):
            vless_list.append(line.strip())
    return list(set(vless_list))

def test_connect(host, port, timeout=3):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except:
        return False

def get_ip_from_vless(vless_url):
    match = re.search(r"vless://([^@]+)@([a-zA-Z0-9\-\.]+):(\d+)", vless_url)
    if match:
        return match.group(2), match.group(3)  # host, port
    return None, None

def get_country_flag(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        country_code = res.get("countryCode", "US")
        return chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))
    except:
        return "🏳️"

def get_connection_type(vless_url):
    if "type=ws" in vless_url:
        return "ws"
    elif "type=grpc" in vless_url:
        return "grpc"
    else:
        return "?"

def remark_vless(url, flag, ctype):
    clean = url.split('#')[0]
    return f"{clean}#{REMARK} {flag} {ctype}"

def main():
    os.makedirs("configs", exist_ok=True)
    try:
        text = requests.get(SOURCE_URL, timeout=10).text
    except:
        print("❌ Failed to fetch source")
        return

    print("🔎 Extracting VLESS configs...")
    raw_vless = extract_vless(text)

    print(f"⚙️ Testing {len(raw_vless)} configs for connectivity...")
    good = []
    for vless in raw_vless:
        host, port = get_ip_from_vless(vless)
        if host and port and test_connect(host, port):
            flag = get_country_flag(host)
            ctype = get_connection_type(vless)
            good.append(remark_vless(vless, flag, ctype))
            print(f"✅ {host}:{port} - {flag} {ctype}")
        else:
            print(f"❌ {host}:{port} unreachable")

    with open(OUTPUT_FILE, "w") as f:
        f.write(MSG + "\n")
        for line in good:
            f.write(line + "\n")

    print(f"\n💾 Saved {len(good)} good configs to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
