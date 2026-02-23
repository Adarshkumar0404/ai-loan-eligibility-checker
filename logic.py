# logic.py

# A. Bank Rules Database
# You can add more banks here easily later without touching the main code.
LOAN_RULES = [
    {"bank": "HDFC Bank", "loan_type": "Premium Personal Loan", "min_salary": 80000, "min_score": 750, "interest": "10.5%"},
    {"bank": "ICICI Bank", "loan_type": "Dream Home Loan", "min_salary": 50000, "min_score": 700, "interest": "8.75%"},
    {"bank": "SBI", "loan_type": "Student/Starter Loan", "min_salary": 25000, "min_score": 650, "interest": "11.0%"},
    {"bank": "Kotak Mahindra", "loan_type": "Quick Cash", "min_salary": 15000, "min_score": 600, "interest": "14.0%"},
    {"bank": "Axis Bank", "loan_type": "Micro Loan", "min_salary": 10000, "min_score": 300, "interest": "16.0%"}
]

# B. Scoring Function
def calculate_custom_score(data):
    """
    Generates a score between 300 and 900 based on the extracted data.
    """
    salary = data.get("monthly_salary", 0)
    balance = data.get("closing_balance_avg", 0)
    emis = data.get("total_emis", 0)
    bounces = data.get("bounced_checks", 0)

    # Base score
    score = 300 
    
    # Logic: Higher Salary & Balance adds points
    score += (salary / 1000) * 2  
    score += (balance / 1000) * 1 
    
    # Logic: High EMIs reduce score slightly (debt burden)
    if salary > 0:
        dti_ratio = emis / salary
        if dti_ratio > 0.5: # If debt is more than 50% of income
            score -= 50
            
    # Logic: Bounced checks hurt the score badly
    score -= (bounces * 50)
    
    # Cap the score between 300 and 900
    return max(300, min(900, int(score)))

def check_loan_eligibility(salary, score):
    """
    Filters the LOAN_RULES list to find matches.
    """
    eligible_loans = []
    for loan in LOAN_RULES:
        if (salary >= loan['min_salary']) and (score >= loan['min_score']):
            eligible_loans.append(loan)
    return eligible_loans