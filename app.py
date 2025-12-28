from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from transformers import pipeline
import os
import re
from faq_data import loan_faq_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import shap
import pandas as pd
from flask import send_file
llm_pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

def get_llm_reply(message):
    prompt = f"""
    You are a helpful loan assistant chatbot.
    Answer clearly in 2-3 sentences.

    Question: {message}
    Answer:
    """
    output = llm_pipe(prompt, max_new_tokens=120,do_sample=False)
    return output[0]["generated_text"].strip()



app = Flask(__name__, template_folder="templets")


# LOAD ML MODEL

model = joblib.load("loan_pipeline.pkl")




ALL_FEATURES = [
    "person_age","person_gender","person_education","person_income","person_emp_exp",
    "person_home_ownership","loan_amnt","loan_intent","loan_int_rate","loan_percent_income",
    "cb_person_cred_hist_length","credit_score","previous_loan_defaults_on_file"
]

PREDICT_KEYWORDS = [
    "predict", "prediction", "loan approval",
    "check my loan", "check loan",
    "eligibility", "am i eligible"
]




def validate_inputs(df):
    rules = {
        "person_age": (18, 65),
        "person_income": (10000, 10000000),
        "credit_score": (300, 900),
        "loan_amnt": (1000, 5000000),
        "person_emp_exp": (0, 50)
    }

    for col, (min_v, max_v) in rules.items():
        if col not in df.columns:
            return False, f"{col} is missing"
        if not df[col].between(min_v, max_v).all():
            return False, f"{col} must be between {min_v} and {max_v}"

    return True, "Valid"




def is_gibberish(text):
    if len(re.findall(r"[a-zA-Z]", text)) < len(text) * 0.4:
        return True
    if len(set(text)) <= 2:
        return True
    return False

def is_help_question(text):
    help_phrases = [
        "can you help me", "help me", "i need help",
        "what can you do", "how can you help"
    ]
    return any(p in text for p in help_phrases)




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/index1")
def index1():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/app")
def loan_form():
    return render_template("app.html")



@app.route("/loan-form", methods=["POST"])
@app.route("/loan-form", methods=["POST"])
def submit_loan_form():
    try:
        data = request.form.to_dict()  # get all form inputs

        # Convert numeric fields
        numeric_cols = ["person_age","person_income","person_emp_exp",
                        "loan_amnt","cb_person_cred_hist_length","credit_score"]
        for col in numeric_cols:
            data[col] = float(data.get(col, 0))

        # Compute loan percent income
        data["loan_percent_income"] = (data["loan_amnt"] / max(1, data["person_income"])) * 100

        # Validate inputs
        is_valid, msg = validate_inputs(pd.DataFrame([data]))
        if not is_valid:
            result = "Rejected ❌"
            reasons = [msg]
        else:
            # Predict
            pred = model.predict(pd.DataFrame([data]))[0]
            result = "Approved ✅" if pred == 1 else "Rejected ❌"

            # SHAP / reasons (dummy or real)
            reasons = [
                "Credit score is sufficient" if pred==1 else "Credit score is low",
                "Income is enough" if pred==1 else "Income too low"
            ]

        # Generate PDF directly (no username needed)
        os.makedirs("reports", exist_ok=True)
        pdf_file = "reports/loan_report.pdf"  # same file for now
        generate_pdf(pdf_file, data, result, reasons)

        # Render result page with download link
        return render_template(
            "result.html",
            status=result,
            confidence="N/A",
            reason=", ".join(reasons),
            download_link="/download-report"  # single PDF
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({
            "reply": "Please type a question 😊",
            "source": "validation"
        })

    user_text = user_msg.lower()

   
    if user_text in ["hi", "hello", "hey", "hai"]:
        return jsonify({
            "reply": "👋 Hi! I’m your Loan Assistant. Ask me about EMI, credit score, eligibility, or approval.",
            "source": "greeting"
        })

  
    if is_help_question(user_text):
        return jsonify({
            "reply": (
                "I can help with:\n"
                "• EMI\n• Loan eligibility\n• Credit score\n• Loan approval\n\n"
                "Ask your question 😊"
            ),
            "source": "help"
        })

  
    if any(word in user_text for word in PREDICT_KEYWORDS):
        return jsonify({
            "reply": "Sure 👍 Redirecting you to the loan application form.",
            "action": "redirect",
            "redirect_url": "/app",
            "source": "redirect"
        })

    
    faq_reply = loan_faq_response(user_text)
    if faq_reply:
        return jsonify({
            "reply": faq_reply,
            "source": "faq"
        })

   
    if is_gibberish(user_text) and len(user_text.split()) <= 2:
        return jsonify({
            "reply": "Sorry 😕 I couldn’t understand that. Please ask a loan-related question.",
            "source": "gibberish"
        })

    
    return jsonify({
        "reply": get_llm_reply(user_msg),
        "source": "huggingface-llm"
    })
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

def generate_pdf(filename, user_data, result, reasons):
    os.makedirs("reports", exist_ok=True)

    # -------------------------------
    # 1️⃣ Generate Charts
    # -------------------------------
    # Bar chart for Financial Overview
    labels = ["Credit Score", "Income", "Loan Amount"]
    values = [
        user_data.get("credit_score", 0),
        user_data.get("person_income", 0),
        user_data.get("loan_amnt", 0)
    ]
    colors_bar = ["#4CAF50", "#2196F3", "#FF9800"]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors_bar, edgecolor="black")
    plt.title("Financial Overview", fontsize=14)
    plt.tight_layout()
    bar_chart_path = "reports/financial_bar.png"
    plt.savefig(bar_chart_path, transparent=True)
    plt.close()

    # Pie chart for Loan Decision
    sizes = [1, 0] if "Approved" in result else [0, 1]
    colors_pie = ["#4CAF50", "#F44336"]
    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=["Approved", "Rejected"], colors=colors_pie, autopct="%1.1f%%", startangle=90)
    plt.title("Loan Decision", fontsize=14)
    pie_chart_path = "reports/decision_pie.png"
    plt.savefig(pie_chart_path, transparent=True)
    plt.close()

    # -------------------------------
    # 2️⃣ Create PDF
    # -------------------------------
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Background
    c.setFillColor(colors.whitesmoke)
    c.rect(0, 0, width, height, fill=1)

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width/2, height-50, "Loan Application Report")
    c.setLineWidth(2)
    c.line(50, height-60, width-50, height-60)

    # -------------------------------
    # Applicant Info Box
    # -------------------------------
    c.setFillColor(colors.lightblue)
    c.roundRect(40, height-200, width-80, 100, 10, fill=1)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    applicant_name = user_data.get("name") or user_data.get("person_name", "N/A")
    c.drawString(50, height-170, f"Applicant: {applicant_name}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height-190, f"Age: {user_data.get('person_age', 'N/A')}")
    c.drawString(250, height-190, f"Income: ${user_data.get('person_income', 0):,}")
    c.drawString(50, height-210, f"Loan Amount Requested: ${user_data.get('loan_amnt', 0):,}")

    # -------------------------------
    # Loan Decision Badge
    # -------------------------------
    decision_color = colors.green if "Approved" in result else colors.red
    c.setFillColor(decision_color)
    c.roundRect(50, height-260, 180, 35, 5, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(50 + 90, height-245, f"{result}")

    # -------------------------------
    # Reasons Box
    # -------------------------------
    c.setFillColor(colors.whitesmoke)
    c.roundRect(40, height-350, width-80, 70, 5, fill=1)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height-330, "Reasons:")

    c.setFont("Helvetica", 12)
    y = height-350 + 50
    for reason in reasons:
        c.drawString(70, y, f"- {reason}")
        y -= 20

    # -------------------------------
    # Charts
    # -------------------------------
    c.drawImage(bar_chart_path, 50, height-600, width=500, height=200, mask='auto')
    c.drawImage(pie_chart_path, 50, height-820, width=250, height=200, mask='auto')

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawString(100, 30, "Generated by Loan Advisory AI System")

    c.save()
# ------------------- LOAD USER DATA -------------------

# ------------------- REPORTS PAGE -------------------

# ------------------- REPORTS PAGE -------------------
@app.route("/reports")
def reports_page():
    os.makedirs("reports", exist_ok=True)
    filename = "reports/loan_report.pdf"
    report_exists = os.path.exists(filename)

    if not report_exists:
        return "No report available. Please submit a loan application first."

    return render_template(
        "reports.html",
        report_exists=report_exists,
        download_link="/download-report"  # fixed download link
    )

# ------------------- DOWNLOAD ROUTE -------------------
@app.route("/download-report")
def download_report():
    filename = "reports/loan_report.pdf"
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "Report not found. Please submit a loan application first."

if __name__ == "__main__":
    app.run(port=5500, debug=False)
