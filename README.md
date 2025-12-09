# 📊 Performance Analyst

A web-based student performance analysis tool that helps educational institutions identify at-risk students and provide targeted interventions.

## ✨ Features

- **📈 Automated Risk Assessment**: Analyzes student data to identify HIGH, MEDIUM, and LOW risk students
- **📊 Visual Dashboard**: Clean, intuitive interface with color-coded risk indicators
- **📄 PDF Reports**: Generate professional PDF reports for stakeholders
- **📚 Analysis History**: Save and review past analyses
- **🎯 Actionable Recommendations**: Provides specific intervention strategies for each student

## 🎯 Risk Criteria

Students are evaluated based on three key metrics:
- **Attendance**: Below 75% triggers concern
- **Academic Performance**: Grades below 7/10 require attention
- **Platform Usage**: Less than 2 hours/week on Rosetta Stone indicates low engagement

### Risk Levels:
- **HIGH RISK**: 2+ issues or concerning teacher comments
- **MEDIUM RISK**: 1 issue identified
- **LOW RISK**: All metrics within acceptable range

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd Performance-Analyst
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 app.py
```

4. Open your browser and navigate to:
```
http://localhost:5001
```

## 📁 Project Structure

```
Performance Analyst/
├── app.py                 # Main Flask application
├── pdf_generator.py       # PDF report generation
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/              # Stylesheets
│   └── images/           # Logo and images
├── uploads/              # Temporary file storage
├── history/              # Saved analysis reports
└── requirements.txt      # Python dependencies
```

## 📊 Excel File Format

The application expects an Excel file with a sheet named **"Reporte IA"** containing the following columns:

- `company_name` - Organization name
- `group_code` - Group/class identifier
- `report_date` - Date of the report
- `student_name` - Student's full name
- `attendance_percentage` - Attendance rate (0-100 or 0-1)
- `average_grade_0_to_10` - Academic grade (0-10 scale)
- `rosetta_weekly_hours` - Weekly hours on Rosetta Stone
- `teacher_comments` - Optional teacher observations

## 🎨 Features Highlights

### Analysis Dashboard
- Real-time student risk assessment
- Color-coded performance indicators
- Detailed student-by-student breakdown
- Statistical overview of class performance

### PDF Export
- Professional report formatting
- Company branding
- Comprehensive student data
- Recommended actions for each student

### History Management
- Save all analyses automatically
- Quick access to previous reports
- Compare performance over time

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Data Processing**: Pandas
- **PDF Generation**: FPDF2
- **Frontend**: HTML, CSS, JavaScript
- **File Handling**: Werkzeug

## 📝 Usage

1. **Upload Excel File**: Click the upload area and select your student data file
2. **Review Analysis**: View the automated risk assessment and recommendations
3. **Download PDF**: Generate a professional report for distribution
4. **Access History**: Review previous analyses from the history section

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**AECorp Platform**

## 📧 Contact

For questions or support, please contact: [Your contact information]

---

**Note**: This tool is designed for educational purposes to help identify students who may need additional support. All data should be handled in accordance with privacy regulations and institutional policies.
