import pywifi
from pywifi import const
import time
import pandas as pd

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first wireless interface
    iface.scan()  # Start scanning
    time.sleep(3)  # Wait for the scan to complete
    results = iface.scan_results()  # Get the results

    networks = []
    for result in results:
        ssid = result.ssid
        bssid = result.bssid
        encryption = "Open" if result.akm[0] == const.AKM_TYPE_NONE else "Encrypted"
        networks.append((ssid, bssid, encryption))

    df = pd.DataFrame(networks, columns=["SSID", "BSSID", "Encryption"])
    df.to_csv("wifi_scan_results.csv", index=False)
    return df

if __name__ == "__main__":
    print("🔍 Scanning Wi-Fi Networks...")
    df = scan_wifi()
    print(df)
