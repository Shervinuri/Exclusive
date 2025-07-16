import requests, re

INPUT = "configs/CollecSHEN.txt"
OUTPUT = "configs/Шервин.txt"
REMARK = "☬SHΞN™"

def get_country_flag(ip):
    try:
        r = requests.get(f"https://ipapi.co/{ip}/country/", timeout=3)
        if r.ok:
            code = r.text.strip().upper()
            if len(code) == 2:
                return chr(127397 + ord(code[0])) + chr(127397 + ord(code[1]))
    except:
        pass
    return "ناکجا آباد 🚏"

def extract_ip(config):
    try:
        m = re.search(r'@([\d.]+)', config)
        return m.group(1) if m else ""
    except:
        return ""

def extract_type(config):
    if "grpc" in config.lower():
        return "grpc"
    if "ws" in config.lower():
        return "ws"
    return "?"

def refine_vless_configs():
    with open(INPUT, 'r') as f:
        raw = f.read().splitlines()

    clean_configs = []
    seen = set()

    for c in raw:
        c = c.strip()
        if not c.startswith("vless://") or c in seen:
            continue

        ip = extract_ip(c)
        if not ip:
            continue

        # اتصال به سرور برای تست
        try:
            requests.get(f"http://{ip}", timeout=3)
        except:
            continue  # اگر وصل نشد حذفش کن

        country_flag = get_country_flag(ip)
        net_type = extract_type(c)
        c = c.split('#')[0] + f"#{REMARK} {country_flag} {net_type}"
        clean_configs.append(c)
        seen.add(c)

    if not clean_configs:
        print("⛔ هیچ کانفیگ سالمی پیدا نشد.")
        return

    with open(OUTPUT, 'w') as f:
        f.write("درود بر یاران جان\nشروین ۱۰ دقیقه دیگه\nمجدد این لیست رو آپدیت میکنه پس اگر کانفیگ خوبی پیدا کردی منتقل کن یجا دیگه چون ممکنه\nکه این بره یکی بهتر بیاد جاش 😁\n\n")
        for c in clean_configs:
            f.write(c + '\n')

    print(f"✅ ذخیره شد: {len(clean_configs)} کانفیگ سالم در {OUTPUT}")

if __name__ == "__main__":
    refine_vless_configs()
