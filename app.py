
from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  


DATA_FOLDER = "data"

@app.route('/api/computers', methods=['GET'])
def get_computers():
    """מחזיר רשימה של כל המחשבים בתיקיית data"""
    try:
        computers = [name for name in os.listdir(DATA_FOLDER) 
                    if os.path.isdir(os.path.join(DATA_FOLDER, name))]
        return jsonify(computers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/computers/<computer>', methods=['GET'])
def get_computer_dates(computer):
    """מחזיר רשימה של כל התאריכים עבור מחשב ספציפי"""
    computer_path = os.path.join(DATA_FOLDER, computer)
    
    if not os.path.exists(computer_path):
        return jsonify({"error": "Computer not found"}), 404
        
    try:
        dates = [name for name in os.listdir(computer_path) 
                if os.path.isdir(os.path.join(computer_path, name))]
        dates.sort()  # מסדר את התאריכים בסדר עולה
        return jsonify(dates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/computers/<computer>/<day>', methods=['GET'])
def get_day_content(computer, day):
    """מחזיר את תוכן קובץ ה-JSON של יום ספציפי"""
    day_path = os.path.join(DATA_FOLDER, computer, day)
    
    if not os.path.exists(day_path):
        return jsonify({"error": "Path not found"}), 404
        
    try:
        # מחפש את קובץ ה-JSON בתיקייה
        json_files = [f for f in os.listdir(day_path) if f.endswith('.json')]
        
        if not json_files:
            return jsonify({"error": "No JSON file found in directory"}), 404
            
        # לוקח את קובץ ה-JSON הראשון
        json_path = os.path.join(day_path, json_files[0])
        
        # קורא את תוכן קובץ ה-JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return jsonify(data)
            
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)