from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt

# ------------------------------
# 1. Data (example)
# ------------------------------
applicant = {
    "name": "John Doe",
    "age": 30,
    "income": 60000,
    "credit_score": 750,
    "loan_amount": 250000,
    "loan_decision": "Approved",
    "reasons": ["Credit score is sufficient", "Income is enough"]
}

# ------------------------------
# 2. Create charts using matplotlib
# ------------------------------

# Bar chart: Financial overview
labels = ['Credit Score', 'Income ($)', 'Loan Amount ($)']
values = [applicant['credit_score'], applicant['income'], applicant['loan_amount']]
colors_bar = ['#4CAF50', '#2196F3', '#FF9800']  # nicer colors

plt.figure(figsize=(6,4))
plt.bar(labels, values, color=colors_bar, edgecolor='black')
plt.title('Applicant Financial Overview', fontsize=14)
plt.savefig('financial_bar.png', bbox_inches='tight', transparent=True)
plt.close()

# Pie chart: Loan Decision
labels = ['Approved', 'Rejected']
sizes = [1, 0] if applicant['loan_decision'] == "Approved" else [0, 1]
colors_pie = ['#4CAF50', '#F44336']

plt.figure(figsize=(4,4))
plt.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
plt.title('Loan Decision', fontsize=14)
plt.savefig('decision_pie.png', bbox_inches='tight', transparent=True)
plt.close()

# ------------------------------
# 3. Generate PDF with enhanced visuals
# ------------------------------
pdf_file = "enhanced_loan_report.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter

# Background color for the whole page
c.setFillColor(colors.whitesmoke)
c.rect(0, 0, width, height, fill=1)

# Title with underline
c.setFont("Helvetica-Bold", 24)
c.setFillColor(colors.darkblue)
c.drawCentredString(width/2, height-50, "Loan Application Report")
c.setLineWidth(2)
c.line(50, height-60, width-50, height-60)

# Applicant Info Box
c.setFillColor(colors.lightblue)
c.roundRect(40, height-220, width-80, 120, 10, fill=1)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 14)
c.drawString(50, height-190, f"Applicant Name: {applicant['name']}")
c.setFont("Helvetica", 12)
c.drawString(50, height-210, f"Age: {applicant['age']}")
c.drawString(250, height-210, f"Income: ${applicant['income']:,}")
c.drawString(50, height-230, f"Loan Amount Requested: ${applicant['loan_amount']:,}")

# Loan Decision Box
decision_color = colors.green if applicant['loan_decision'] == "Approved" else colors.red
c.setFillColor(decision_color)
c.roundRect(40, height-290, width-80, 40, 5, fill=1)
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(width/2, height-270, f"Decision: {applicant['loan_decision']}")

# Reasons Box
c.setFillColor(colors.whitesmoke)
c.roundRect(40, height-380, width-80, 80, 5, fill=1)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 12)
c.drawString(50, height-360, "Reasons:")
c.setFont("Helvetica", 12)
y = height-380 + 60
for reason in applicant['reasons']:
    c.drawString(70, y, f"- {reason}")
    y -= 20

# Add charts
c.drawImage('financial_bar.png', 50, height-600, width=500, height=200, mask='auto')
c.drawImage('decision_pie.png', 50, height-820, width=250, height=200, mask='auto')

# Finish PDF
c.save()
print(f"Enhanced loan report saved as {pdf_file}")
