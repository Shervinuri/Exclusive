import requests
import yaml
from urllib.parse import unquote

# لینک منبع کانفیگ‌ها
SOURCE_URL = "https://raw.githubusercontent.com/Shervinuri/V4ray/main/configs/CollecSHEN.txt"
# نام فایل خروجی. پسوند .yaml برای نرم‌افزارهای کلاینت ضروری است
OUTPUT_FILE = "CollecSHEN.yaml"

def parse_vless_url(url):
    """این تابع یک لینک VLESS را به فرمت دیکشنری پایتون برای Clash تبدیل می‌کند."""
    try:
        if not url.startswith("vless://"):
            return None

        # بخش اصلی لینک از ریمارک (#) جدا می‌شود
        parts = url.split("#")
        main_part = parts[0][8:]  # حذف vless://
        # ریمارک با unquote دیکود می‌شود تا کاراکترهای خاص درست نمایش داده شوند
        remark = unquote(parts[1]) if len(parts) > 1 else "Unnamed"

        # جدا کردن اطلاعات کاربر از آدرس سرور
        user_info, address_part = main_part.split("@")
        
        # ✅ اصلاح شد: UUID همان بخش قبل از @ است
        uuid = user_info

        # جدا کردن پارامترها از آدرس
        server_port, params_str = address_part.split("?", 1) if "?" in address_part else (address_part, "")
        server, port = server_port.split(":")

        # مقادیر پیش‌فرض
        network = "tcp"
        path = ""
        host = ""
        sni = ""
        service_name = ""

        # پردازش پارامترهای لینک
        params = params_str.split("&")
        
        for part in params:
            if part.startswith("type="):
                network = part.split("=", 1)[1]
            elif part.startswith("path="):
                path = unquote(part.split("=", 1)[1])
            elif part.startswith("host="):
                host = part.split("=", 1)[1]
            elif part.startswith("sni="):
                # ✨ جدید: پارامتر sni برای TLS اضافه شد
                sni = part.split("=", 1)[1]
            elif part.startswith("serviceName="):
                # ✨ جدید: پارامتر serviceName برای gRPC اضافه شد
                service_name = unquote(part.split("=", 1)[1])

        proxy = {
            "name": remark.strip(),
            "type": "vless",
            "server": server,
            "port": int(port),
            "uuid": uuid,
            "tls": True,  # فرض بر این است که همه کانفیگ‌ها TLS دارند
            "udp": True,  # برای عملکرد بهتر و پشتیبانی از UDP اضافه شد
            "network": network,
            # ✅ اصلاح شد: مقدار servername برای SNI به درستی تنظیم می‌شود
            "servername": sni or host or server,
        }

        if network == "ws":
            proxy["ws-opts"] = {
                "path": path,
                "headers": {"Host": host or server}
            }
        elif network == "grpc":
            proxy["grpc-opts"] = {
                # ✅ اصلاح شد: از serviceName خوانده شده از لینک استفاده می‌شود
                "grpc-service-name": service_name
            }

        return proxy
    except Exception:
        return None

def generate_yaml():
    """کانفیگ‌ها را از لینک منبع دریافت و فایل YAML را تولید می‌کند."""
    try:
        res = requests.get(SOURCE_URL)
        res.raise_for_status()  # در صورت خطا در درخواست، متوقف می‌شود
        lines = res.text.strip().splitlines()
        proxies = []

        for line in lines:
            if proxy := parse_vless_url(line.strip()):
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

        # فایل با انکودینگ utf-8 برای پشتیبانی کامل از کاراکترهای فارسی و خاص ذخیره می‌شود
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"✅ فایل Clash YAML با نام {OUTPUT_FILE} و با {len(proxies)} کانفیگ ساخته شد.")

    except requests.exceptions.RequestException as e:
        print(f"⛔ خطا در دریافت اطلاعات از لینک: {e}")
    except Exception as e:
        print(f"⛔ یک خطای پیش‌بینی نشده رخ داد: {e}")

if __name__ == "__main__":
    generate_yaml()
