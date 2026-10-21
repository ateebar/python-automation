import datetime

def run_automation():
    now = datetime.datetime.now()
    print(f"[@ateebar] Otomasyon çalıştı! Tarih ve Saat: {now.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_automation()
