from fpdf import FPDF

# Create a PDF object
pdf = FPDF()
pdf.add_page()

# Header
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="MOCK BANK STATEMENT - Adarsh", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Period: January 2026", ln=True, align='C')
pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
pdf.ln(5) # Add a blank line

# Fake Transactions with "Noise" to test the AI
transactions = [
    "01/01/2026 | INFLOW  | Tech Solutions Ltd (Salary)   | + Rs. 95,000",
    "02/01/2026 | UPI     | Zomato                        | - Rs. 450",
    "03/01/2026 | UPI     | Amazon India                  | - Rs. 1,299",
    "05/01/2026 | OUTFLOW | HDFC Home Loan EMI            | - Rs. 32,000",
    "08/01/2026 | OUTFLOW | Jio Mobile Recharge           | - Rs. 749",
    "10/01/2026 | UPI     | Swiggy Instamart              | - Rs. 320",
    "12/01/2026 | OUTFLOW | Auto Loan EMI                 | - Rs. 12,000",
    "14/01/2026 | OUTFLOW | Uber Rides                    | - Rs. 250",
    "15/01/2026 | OUTFLOW | Netflix Subscription          | - Rs. 649",
    "16/01/2026 | UPI     | BookMyShow                    | - Rs. 850",
    "18/01/2026 | PENALTY | Cheque Bounce Charge          | - Rs. 500",
    "19/01/2026 | INFLOW  | UPI Cashback Received         | + Rs. 50",
    "21/01/2026 | PENALTY | Insufficient Funds Fee (ACH)  | - Rs. 500",
    "22/01/2026 | UPI     | Blinkit Groceries             | - Rs. 410",
    "25/01/2026 | OUTFLOW | Electricity Bill              | - Rs. 1,450",
    "27/01/2026 | UPI     | Transfer to Friend            | - Rs. 2,500",
    "28/01/2026 | OUTFLOW | Supermarket                   | - Rs. 8,500",
    "30/01/2026 | INFLOW  | Interest Credit               | + Rs. 125",
    "31/01/2026 | INFO    | Average Closing Balance       | Rs. 55,000"
]

# Write transactions to PDF using a Monospace font for realism
pdf.set_font("Courier", size=10) 
for t in transactions:
    pdf.cell(200, 8, txt=t, ln=True)

# Save the PDF
pdf.output("dummy_statement.pdf")
print("✅ dummy_statement.pdf created successfully!")