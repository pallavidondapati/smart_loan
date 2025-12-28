import random



FAQ_RESPONSES = {

    "greeting": [
        "Hey! 👋 I’m your personal loan assistant.",
        "Hello 😊 How can I assist you with loans today?",
        "Hi! Need help with EMI or eligibility?",
        "Welcome 👋 Let’s talk about your loan needs.",
        "Hey! I can guide you through loan approval.",
        "Hi! Ask me anything related to loans 💬",
        "Hello! Planning to take a loan?",
        "Welcome! 😊 I’m here to help you make better loan decisions.",
        "Hey there! Tell me what loan you’re looking for.",
        "Hi 👋 Let’s get started with your loan query."
    ],

    "loan_types": [
        "We offer Personal, Home, Education, Vehicle, Business, and Gold loans.",
        "Personal loans are unsecured and do not require collateral.",
        "Home loans are long-term loans with lower interest rates.",
        "Education loans support higher studies in India or abroad.",
        "Vehicle loans are available for cars and two-wheelers.",
        "Business loans help with expansion and working capital.",
        "Gold loans are secured loans against gold jewelry.",
        "Each loan type has different eligibility criteria.",
        "Loan choice depends on income and purpose.",
        "Tell me which loan you’re interested in."
    ],

    "eligibility": [
        "Loan eligibility depends on age, income, employment type, and credit score.",
        "Most banks require applicants to be between 21 and 60 years old.",
        "Stable income improves loan eligibility.",
        "Self-employed applicants need business income proof.",
        "Higher income increases eligibility.",
        "Lower existing EMIs improve approval chances.",
        "Eligibility varies from bank to bank.",
        "Co-applicant income can improve eligibility.",
        "Credit score plays a major role.",
        "Share your details and I’ll help estimate eligibility."
    ],

    "emi": [
        "EMI stands for Equated Monthly Installment.",
        "EMI depends on loan amount, interest rate, and tenure.",
        "Lower tenure results in higher EMI but less interest paid.",
        "Longer tenure lowers EMI but increases total interest.",
        "Prepayment can reduce interest burden.",
        "EMI usually starts one month after disbursement.",
        "Auto-debit helps avoid missed EMIs.",
        "Missing EMIs affects credit score.",
        "Tell me loan amount and tenure to calculate EMI.",
        "Choosing the right EMI is important for budgeting."
    ],

    "interest_rate": [
        "Interest rates vary depending on loan type.",
        "Personal loans usually have higher interest rates.",
        "Home loans offer lower interest rates.",
        "Good credit score helps get lower rates.",
        "Interest rates can be fixed or floating.",
        "Floating rates may change over time.",
        "Fixed rates remain constant throughout tenure.",
        "Women applicants may get lower rates.",
        "Government employees may get benefits.",
        "Compare lenders before choosing a loan."
    ],

    "credit_score": [
        "Credit score ranges from 300 to 900.",
        "A score above 750 is considered excellent.",
        "Late EMI payments reduce credit score.",
        "Paying EMIs on time improves score.",
        "High credit utilization reduces score.",
        "Too many loan inquiries reduce score.",
        "Checking credit score does not hurt it.",
        "Low score may cause rejection.",
        "Co-applicant with good score can help.",
        "Good credit saves money on interest."
    ],

    "documents": [
        "ID proof includes Aadhaar, PAN, or Passport.",
        "Address proof can be Aadhaar or utility bills.",
        "Income proof includes salary slips or ITR.",
        "Last 6 months bank statements are required.",
        "Home loans require property documents.",
        "Education loans need admission proof.",
        "Business loans need business registration proof.",
        "Self-employed applicants need extra documents.",
        "PAN card is mandatory for most loans.",
        "Submitting complete documents speeds approval."
    ],

    "rejection": [
        "Loan rejection happens due to low income or credit score.",
        "High existing EMIs can cause rejection.",
        "Incomplete documents may lead to rejection.",
        "Job instability affects approval chances.",
        "Applying for high amount increases rejection risk.",
        "Rejection is not permanent.",
        "Improve credit score before reapplying.",
        "Wait before applying again after rejection.",
        "A co-applicant can reduce rejection chances.",
        "Choose the right loan amount."
    ],

    "fallback": [
        "I can help with loan eligibility, EMI, interest rates, and documents 😊",
        "Please ask something related to loans.",
        "Tell me what kind of loan you are looking for.",
        "I specialize in loan guidance.",
        "I didn’t understand that, but I can help with loans.",
        "Try asking about EMI or eligibility.",
        "Let me know your loan requirement.",
        "I’m here to guide you through loans.",
        "Please rephrase your question.",
        "Ask me anything about loans 💬"
    ]
}


KEYWORD_TO_INTENT = {
    "hi": "greeting",
    "hello": "greeting",
    "hey": "greeting",

    "loan types": "loan_types",
    "types of loan": "loan_types",
    "personal loan": "loan_types",
    "home loan": "loan_types",
    "education loan": "loan_types",
    "business loan": "loan_types",

    "eligibility": "eligibility",
    "eligible": "eligibility",
    "qualification": "eligibility",

    "emi": "emi",
    "installment": "emi",
    "monthly payment": "emi",

    "interest rate": "interest_rate",
    "interest": "interest_rate",

    "credit score": "credit_score",
    "cibil": "credit_score",

    "document": "documents",
    "documents": "documents",
    "papers": "documents",

    "reject": "rejection",
    "rejected": "rejection",
    "denied": "rejection"
}


def loan_faq_response(message: str) -> str:
    message = message.lower()

    for keyword, intent in KEYWORD_TO_INTENT.items():
        if keyword in message:
            return random.choice(FAQ_RESPONSES[intent])

    return random.choice(FAQ_RESPONSES["fallback"])
