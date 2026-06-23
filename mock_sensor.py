import sqlite3, time, random
from datetime import datetime

# Setup DB
conn = sqlite3.connect('aquaalert.db')
conn.execute('CREATE TABLE IF NOT EXISTS water_logs (log_id INTEGER PRIMARY KEY, timestamp TEXT, tank_id TEXT, water_level INTEGER, motor_status TEXT)')
conn.close()

level, status = 50, "OFF"
print("Simulator Running... Press Ctrl+C to stop.")

while True:
    level = level - random.randint(1, 3) if status == "OFF" else level + random.randint(5, 8)
    if level <= 20: status = "ON"
    if level >= 95: status = "OFF"
    
    conn = sqlite3.connect('aquaalert.db')
    conn.execute('INSERT INTO water_logs (timestamp, tank_id, water_level, motor_status) VALUES (?, ?, ?, ?)', 
                 (datetime.now().strftime("%H:%M:%S"), "TANK-01", level, status))
    conn.commit()
    conn.close()
    print(f"Logged: {level}% | Motor: {status}")
    time.sleep(2)
