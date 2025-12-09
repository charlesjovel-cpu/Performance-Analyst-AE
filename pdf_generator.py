from fpdf import FPDF
import datetime

class VIPReportPDF(FPDF):
    def __init__(self, meta):
        super().__init__(orientation='L', unit='mm', format='Letter')
        self.meta = meta
        self.set_auto_page_break(auto=True, margin=15)
        
        # Colors
        self.c_bg = (255, 255, 255) # White BG for print
        self.c_text = (0, 0, 0)     # Pure Black
        self.c_primary = (212, 175, 55) # Gold
        self.c_accent = (20, 20, 20)    # Dark Grey
        self.c_danger = (217, 4, 41)    # Red
        self.c_warning = (251, 133, 0)  # Orange
        self.c_success = (16, 185, 129) # Green

    def header(self):
        # Top Bar
        self.set_fill_color(*self.c_accent)
        self.rect(0, 0, 280, 20, 'F')
        
        # Logo Text
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*self.c_primary)
        self.set_xy(10, 5)
        self.cell(100, 10, 'AECorp AI | Performance Analysis', 0, 0, 'L')
        
        # Date
        self.set_font('Helvetica', '', 10)
        self.set_text_color(200, 200, 200)
        self.set_xy(200, 5)
        self.cell(70, 10, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 0, 'R')
        
        # Bottom Gold Line
        self.set_draw_color(*self.c_primary)
        self.set_line_width(0.5)
        self.line(0, 20, 280, 20)
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def kpi_card(self, x, y, title, value, color_rgb):
        # Card Border
        self.set_draw_color(200, 200, 200)
        self.set_fill_color(250, 250, 250)
        self.rect(x, y, 60, 30, 'DF')
        
        # Top Accent Line
        self.set_fill_color(*color_rgb)
        self.rect(x, y, 60, 2, 'F')
        
        # Content
        self.set_xy(x+2, y+5)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(100, 100, 100)
        self.cell(56, 5, title, 0, 2, 'C')
        
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(*color_rgb)
        self.cell(56, 12, str(value), 0, 2, 'C')

    def student_row(self, student):
        # Risk Color
        r_color = self.c_accent
        if student['risk_class'] == 'high': r_color = self.c_danger
        elif student['risk_class'] == 'medium': r_color = self.c_warning
        elif student['risk_class'] == 'low': r_color = self.c_success

        # Container
        x = self.get_x()
        y = self.get_y()
        
        # Check page break
        if y > 180:
            self.add_page()
            y = self.get_y()

        self.set_draw_color(230, 230, 230)
        self.set_fill_color(255, 255, 255)
        self.rect(x, y, 260, 25, 'DF')
        
        # Left Border Strip
        self.set_fill_color(*r_color)
        self.rect(x, y, 2, 25, 'F')
        
        # Name
        self.set_xy(x+5, y+3)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(100, 8, student['name'], 0, 2)
        
        # Stats
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        stats_text = f"Attendance: {student['att']}%  |  Grade: {student['grade']}  |  Platform: {student['rosetta']}h"
        self.cell(100, 6, stats_text, 0, 0)
        
        # Issues
        self.set_xy(x+110, y+8)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(*self.c_danger)
        issues = ", ".join(student['issues'])
        self.multi_cell(140, 5, issues, align='R')
        
        self.set_y(y + 30)

def generate_pdf_report(data):
    pdf = VIPReportPDF(data['meta'])
    pdf.add_page()
    
    # -- REPORT HEADER --
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Report: {data['meta'].get('company', 'Unknown Company')}", 0, 1, 'L')
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Group: {data['meta']['group']}   |   Students: {data['meta']['total']}", 0, 1, 'L')
    pdf.ln(5)
    
    # -- KPI CARDS --
    y_kpi = pdf.get_y()
    pdf.kpi_card(10, y_kpi, "HIGH RISK", data['stats']['high'], pdf.c_danger)
    pdf.kpi_card(75, y_kpi, "MEDIUM RISK", data['stats']['medium'], pdf.c_warning)
    pdf.kpi_card(140, y_kpi, "LOW USAGE", f"{data['stats']['pct_rosetta']}%", pdf.c_primary)
    pdf.kpi_card(205, y_kpi, "LOW ATT", f"{data['stats']['pct_att']}%", pdf.c_accent)
    pdf.ln(35)
    
    # -- RECOMMENDATIONS --
    pdf.set_fill_color(250, 250, 250)
    pdf.set_draw_color(212, 175, 55) # Gold border
    pdf.rect(10, pdf.get_y(), 260, 30, 'DF')
    
    pdf.set_xy(15, pdf.get_y()+3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*pdf.c_primary)
    pdf.cell(0, 6, "AI RECOMMENDATIONS", 0, 1)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.set_x(15)
    
    # Logic for recs (simple default)
    recs = ["Monitor platform usage weekly.", "Reinforce attendance importance."]
    if data['stats']['pct_grade'] > 30: recs.append("Consider general review session due to low grades.")
    
    for r in recs:
        pdf.set_x(20)
        pdf.cell(0, 5, f"- {r}", 0, 1)
        
    pdf.ln(15)
    
    # -- STUDENTS LIST --
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "At-Risk Student Analysis", 0, 1)
    pdf.ln(2)
    
    for student in data['students']:
        if student['risk'] == "LOW RISK": continue
        pdf.student_row(student)
        
    return pdf
