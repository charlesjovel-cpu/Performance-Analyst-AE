import os
import io
import json
import time
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from werkzeug.utils import secure_filename
from pdf_generator import generate_pdf_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['HISTORY_FOLDER'] = 'history'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['HISTORY_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_logic(file_path):
    sheet_name = "Reporte IA"
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        return {"error": str(e)}

    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # Logic from analyze_report.py
    raw_students = []
    company_name = "Unknown"
    group_code = "Unknown"
    report_date = "Unknown"

    for index, row in df.iterrows():
        if index == 0:
            company_name = str(row.get('company_name', 'Unknown'))
            group_code = str(row.get('group_code', 'Unknown'))
            val_date = row.get('report_date', 'Unknown')
            report_date = str(val_date) if val_date else 'Unknown'

        s_name = row.get('student_name', 'Unknown')
        if pd.isna(s_name): continue
        
        att_pct = pd.to_numeric(row.get('attendance_percentage', 0), errors='coerce') or 0
        grade = pd.to_numeric(row.get('average_grade_0_to_10', 0), errors='coerce') or 0
        rosetta = pd.to_numeric(row.get('rosetta_weekly_hours', 0), errors='coerce') or 0
        comments = str(row.get('teacher_comments', ''))
        if comments == 'nan' or comments.lower() == 'nan': comments = ""
        
        raw_students.append({
            "name": s_name,
            "att": att_pct,
            "grade": grade,
            "rosetta": rosetta,
            "comments": comments
        })

    # Normalize Attendance
    if raw_students:
        max_att = max(s['att'] for s in raw_students)
        if max_att <= 1.0 and max_att > 0:
            for s in raw_students:
                s['att'] *= 100

    students = []
    
    count_low_att = 0
    count_low_grade = 0
    count_low_rosetta = 0
    
    for s in raw_students:
        issues = []
        rec_actions = []
        
        att_pct = s['att']
        grade = s['grade']
        rosetta = s['rosetta']
        comments = s['comments']
        
        flag_att = att_pct < 75
        flag_grade = grade < 7
        flag_rosetta = rosetta < 2
        
        if flag_att: 
            issues.append("Low Attendance")
            count_low_att += 1
        if flag_grade: 
            issues.append("Low Grade")
            count_low_grade += 1
        if flag_rosetta: 
            issues.append("Low Platform Usage")
            count_low_rosetta += 1
        
        keywords = ["demotivation", "low engagement", "desmotiv", "baja partici", "poco partici"]
        flag_comments = any(k in comments.lower() for k in keywords)
        
        if flag_comments:
            issues.append("Teacher Comment Concern")

        issue_count = sum([flag_att, flag_grade, flag_rosetta])
        risk_level = "LOW RISK"
        risk_class = "low"
        
        if issue_count >= 2 or flag_comments:
            risk_level = "HIGH RISK"
            risk_class = "high"
        elif issue_count == 1:
            risk_level = "MEDIUM RISK"
            risk_class = "medium"
        
        if flag_att or flag_grade:
            if flag_att and flag_grade:
                rec_actions.append("Mandatory Saturday reinforcement (2 weeks) + follow-up review")
            else:
                rec_actions.append("Saturday reinforcement session 9:00–10:00 AM")
        
        if flag_rosetta:
            rec_actions.append("Encourage consistent practice")
            
        if risk_level in ["HIGH RISK", "MEDIUM RISK"]:
             rec_actions.append("Contact student and schedule follow-up")

        students.append({
            "name": s['name'],
            "issues": issues,
            "risk": risk_level,
            "risk_class": risk_class,
            "actions": rec_actions,
            "att": round(att_pct, 0),
            "grade": round(grade, 2),
            "rosetta": rosetta,
            "comments": comments
        })

    total = len(students)
    high = sum(1 for s in students if s['risk'] == "HIGH RISK")
    med = sum(1 for s in students if s['risk'] == "MEDIUM RISK")
    low = sum(1 for s in students if s['risk'] == "LOW RISK")

    return {
        "success": True,
        "meta": {
            "company": company_name,
            "group": group_code,
            "date": report_date,
            "total": total
        },
        "stats": {
            "high": high,
            "medium": med,
            "low": low,
            "pct_att": round((count_low_att / total * 100), 1) if total else 0,
            "pct_grade": round((count_low_grade / total * 100), 1) if total else 0,
            "pct_rosetta": round((count_low_rosetta / total * 100), 1) if total else 0
        },
        "students": students
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        try:
            result = analyze_logic(path)
            
            # Save to History
            if result.get('success'):
                timestamp = int(time.time())
                company_safe = secure_filename(result['meta'].get('company', 'Unknown'))
                hist_filename = f"{timestamp}_{company_safe}.json"
                hist_path = os.path.join(app.config['HISTORY_FOLDER'], hist_filename)
                
                # Add stored filename to result so frontend knows it (optional, but good)
                result['history_filename'] = hist_filename
                
                with open(hist_path, 'w') as f:
                    json.dump(result, f)
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
        
    return jsonify({"error": "Invalid file type"})

@app.route('/history', methods=['GET'])
def get_history():
    try:
        files = []
        hist_dir = app.config['HISTORY_FOLDER']
        # List all json files in history reversed (newest first)
        for f_name in sorted(os.listdir(hist_dir), reverse=True):
            if f_name.endswith('.json'):
                path = os.path.join(hist_dir, f_name)
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        files.append({
                            'filename': f_name,
                            'date': data['meta'].get('date', 'Unknown'),
                            'company': data['meta'].get('company', 'Unknown'),
                            'group': data['meta'].get('group', 'Unknown'),
                            'high_risk': data['stats'].get('high', 0),
                            'timestamp': f_name.split('_')[0]
                        })
                except:
                    continue # Skip broken files
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/history/<filename>', methods=['GET'])
def get_history_item(filename):
    try:
        safe_name = secure_filename(filename)
        path = os.path.join(app.config['HISTORY_FOLDER'], safe_name)
        if not os.path.exists(path):
            return jsonify({"error": "File not found"}), 404
            
        with open(path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        pdf = generate_pdf_report(data)
        
        # Output to buffer (fpdf2 output() returns bytearray)
        pdf_bytes = pdf.output() 
        buffer = io.BytesIO(bytes(pdf_bytes))
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Report_{data['meta'].get('company', 'Analysis')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"PDF Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
