from flask import Flask, render_template, jsonify, Response
import sqlite3
import csv
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    conn = sqlite3.connect('aquaalert.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tank_id, water_level, motor_status FROM water_logs ORDER BY log_id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    return jsonify({"water_level": row[1] if row else 0, "motor_status": row[2] if row else "OFF"})

@app.route('/api/download_report')
def download_report():
    conn = sqlite3.connect('aquaalert.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, tank_id, water_level, motor_status FROM water_logs ORDER BY log_id DESC')
    logs = cursor.fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Timestamp', 'Tank ID', 'Water Level (%)', 'Motor Status'])
    writer.writerows(logs)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=AquaAlert_Weekly_Report.csv"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
