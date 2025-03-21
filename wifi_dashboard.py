import tkinter as tk
from tkinter import ttk
import pandas as pd
import time
from risk_analyzer import analyze_risk

def update_table():
    try:
        df = pd.read_csv("wifi_scan_results.csv")

        # 🚨 Clear existing rows before inserting new ones
        for row in tree.get_children():
            tree.delete(row)

        # 🚀 Insert new data
        for row in df.itertuples():
            risk = analyze_risk(row.SSID, row.BSSID, row.Encryption)
            print(f"DEBUG: Inserting {row.SSID} → Risk: {risk}%")  # Debugging log
            tree.insert("", "end", values=(row.SSID, row.BSSID, row.Encryption, f"{risk}%"))

    except Exception as e:
        print("No data available yet. ERROR:", e)

    root.after(30000, update_table)  # Refresh every 30 sec

# 🖥️ GUI Setup
root = tk.Tk()
root.title("Wi-Fi Risk Report")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Real-Time Wi-Fi Risk Report", font=("Arial", 14, "bold")).grid(row=0, column=0)

columns = ("SSID", "BSSID", "Encryption", "Risk Score")
tree = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=1, column=0)

update_table()
root.mainloop()
