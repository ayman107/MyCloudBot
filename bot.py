import os, requests, re, random, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

TARGET_URL = "https://ayman1077.blogspot.com/2025/12/fffrf.html"

def fetch_proxies():
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=1000",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt"
    ]
    raw = []
    for s in sources:
        try:
            r = requests.get(s, timeout=10)
            raw.extend(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text))
        except: continue
    return list(set(raw))

def simulate_device_task(proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Device-RAM': '4GB'
    }
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    
    success_in_this_device = 0
    for _ in range(100):
        try:
            r = requests.get(TARGET_URL, headers=headers, proxies=proxies, timeout=5)
            if r.status_code == 200:
                success_in_this_device += 1
        except: break
    return success_in_this_device

def main():
    proxies = fetch_proxies()
    total_success = 0
    # تنفيذ المهام لـ 30 جهاز وهمي (لضمان عدم تجاوز وقت جيت هاب المجاني)
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(simulate_device_task, proxies[:30]))
        total_success = sum(results)

    # كتابة التقرير
    report = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Total Successful Hits: {total_success}\n"
    with open("stats.txt", "a") as f:
        f.write(report)
    print(f"[*] Cycle Finished. Recorded {total_success} hits.")

if __name__ == "__main__":
    main()
