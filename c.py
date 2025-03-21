import csv
from collections import defaultdict

def get_vendor_prefix(mac):
    """Extract the first three bytes (prefix) of a MAC address to identify the vendor."""
    return ":".join(mac.split(":")[:3])

# File containing Wi-Fi scan results
csv_filename = "wifi_networkss.csv"

# Dictionaries to store SSID → BSSID list & BSSID → SSID list
bssid_map = defaultdict(set)
ssid_map = defaultdict(set)
ssid_vendor_map = defaultdict(set)
ssid_signal_map = defaultdict(list)
honeypots = []

try:
    with open(csv_filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            ssid = row["SSID"].strip()
            bssid = row["BSSID"].strip()
            encryption = row["Encryption"].strip()
            signal = row["Signal Strength (%)"].strip()

            # Convert signal to integer or None
            signal = int(signal) if signal.isdigit() else None

            if bssid:
                vendor_prefix = get_vendor_prefix(bssid)
                bssid_map[bssid].add(ssid)
                ssid_map[ssid].add(bssid)
                ssid_vendor_map[ssid].add(vendor_prefix)

                if signal is not None:
                    ssid_signal_map[ssid].append(signal)

            # Flag open (unencrypted) networks
            if encryption.lower() == "none":
                honeypots.append(f"⚠️ Open Network: {ssid} ({bssid})")

    # ✅ **Check for SSID spoofing (same SSID but different vendor prefixes)**
    for ssid, vendors in ssid_vendor_map.items():
        if len(vendors) > 1:
            signal_values = [s for s in ssid_signal_map[ssid] if s is not None]  # Ignore None values

            if signal_values:
                avg_signal = sum(signal_values) / len(signal_values)
                # If signals are very close, it's suspicious (e.g., same location)
                if max(signal_values) - min(signal_values) < 10:
                    honeypots.append(f"🚨 Suspicious SSID '{ssid}' has multiple vendors & similar signals: {', '.join(vendors)}")

    # ✅ **Fix: Only flag BSSID spoofing if some BSSIDs have a different vendor prefix**
    for ssid, bssids in ssid_map.items():
        vendor_prefixes = {get_vendor_prefix(bssid) for bssid in bssids}

        if len(vendor_prefixes) > 1:
            # Find BSSIDs that do not match the most common vendor prefix
            vendor_count = defaultdict(int)
            for bssid in bssids:
                vendor_count[get_vendor_prefix(bssid)] += 1
            
            most_common_vendor = max(vendor_count, key=vendor_count.get)  # Vendor with highest count
            
            # Identify BSSIDs with a different vendor prefix
            suspicious_bssids = [bssid for bssid in bssids if get_vendor_prefix(bssid) != most_common_vendor]

            if suspicious_bssids:
                honeypots.append(f"🚨 Possible Honeypot! SSID '{ssid}' has BSSIDs from different vendors: {', '.join(suspicious_bssids)}")

    # Print results
    if honeypots:
        print("\n🔍 Possible Honeypots Detected:")
        for alert in honeypots:
            print(alert)
    else:
        print("\n✅ No honeypots detected.")

except FileNotFoundError:
    print("🚨 CSV file not found. Run the Wi-Fi scan first.")
