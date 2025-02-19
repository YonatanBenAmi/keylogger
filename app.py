from flask import Flask, jsonify, abort, render_template
import os
import json

app = Flask(__name__)

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<computer>', methods=['GET'])
def get_computer_days(computer):
    computer_path = os.path.join(BASE_PATH, computer)
    if not os.path.exists(computer_path) or not os.path.isdir(computer_path):
        abort(404, description="Computer not found")
    try:
        # מקבל את רשימת כל התיקיות (הימים) בתיקיית המחשב
        days = [d for d in os.listdir(computer_path) if os.path.isdir(os.path.join(computer_path, d))]
    except Exception as e:
        abort(500, description=f"Error reading computer directory: {e}")
    return jsonify({"days": days})

@app.route('/<computer>/<day>', methods=['GET'])
def get_day_data(computer, day):
    file_path = os.path.join(BASE_PATH, computer, day, 'data.json')
    if not os.path.exists(file_path):
        abort(404, description="Data not found")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        abort(500, description=f"Error reading file: {e}")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
