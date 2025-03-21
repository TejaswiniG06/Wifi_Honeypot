from plyer import notification

def send_alert(msg):
    notification.notify(title="Wi-Fi Sentinel", message=msg, timeout=5)

if __name__ == "__main__":
    send_alert("⚠️ High-Risk Wi-Fi Detected!")
