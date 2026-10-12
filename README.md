# Wrench-Wise-Banking-AI
## Simulated Real-Time Banking Architecture Using Multi-Agent Automation

### 1. Project Overview

Wrench Wise Banking AI is a prototype banking assistant that uses a supervisor-orchestrator architecture to route customer requests to specialized AI agents. It combines Python, Gemini, SQLite, and Streamlit to simulate common banking operations.

The application supports natural-language questions about account balances, transaction history, suspicious transactions, existing loans, and loan eligibility.

**Note:** This is a simulated banking application using fictional data. It is not connected to a real bank or live banking APIs.

### 2. Objectives

- Build a supervisor that identifies customer requests and routes them to the appropriate agent.
- Implement three specialized agents for banking operations, risk analysis, and credit eligibility.
- Simulate banking APIs using Python functions and an SQLite database.
- Integrate Gemini for natural-language understanding and responses.
- Provide a user-friendly dashboard using Streamlit.
- Demonstrate multiple banking use cases through an interactive interface.

### 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and agent implementation |
| Google Gemini API | Intent classification and natural-language responses |
| Streamlit | Interactive user interface |
| SQLite | Simulated banking database |
| python-dotenv | Loading API credentials from `.env` |
| Regular expressions | Fallback request classification |

### 4. System Architecture

```text
                 Customer
                    |
                    v
            Streamlit Interface
                    |
                    v
          Supervisor / Orchestrator
                    |
           Intent Classification
                    |
       +------------+------------+
       |            |            |
       v            v            v
  Banking Agent  Risk/Fraud   Credit/Loan
       Agent        Agent        Agent
       |            |            |
       +------------+------------+
                    |
                    v
         Simulated Banking Tools
                    |
                    v
              SQLite Database
                    |
                    v
          Agent Results Returned
                    |
                    v
         Gemini Natural-Language
                Response
                    |
                    v
               Customer
```

### 5. Specialized Agents

**Banking Agent**
- Retrieves customer profiles.
- Retrieves simulated account balances.
- Displays transaction history.
- Retrieves existing loan information.

**Risk/Fraud Agent**
- Checks configured risk indicators, including high transaction amounts, pending status, and suspicious descriptions.
- Assigns a rule-based risk level.
- Provides reasons for review.

**Credit/Loan Agent**
- Evaluates a requested loan amount using demo rules.
- Considers credit score, monthly income, and existing loan exposure.
- Returns an illustrative eligibility result.

**Supervisor/Orchestrator**

The supervisor classifies incoming requests and routes them to the relevant specialized agent. If Gemini is unavailable, basic fallback classification is used for supported requests.

### 6. Main Use Cases

1. **Account balance:** A customer asks, “Show my balance.”
2. **Transaction history:** A customer asks to view recent transactions.
3. **Risk analysis:** A customer asks, “Check transaction TX104 for suspicious activity.”
4. **Existing loans:** A customer asks to view their current loans.
5. **Loan eligibility:** A customer asks, “Am I eligible for a loan of ₹3 lakh?”

### 7. Project Structure

```text
wrenchwise-banking-ai/
│
├── app.py
├── orchestrator.py
├── requirements.txt
├── .env
├── .gitignore
│
├── agents/
│   ├── __init__.py
│   ├── banking_agent.py
│   ├── risk_agent.py
│   └── credit_agent.py
│
├── tools/
│   ├── __init__.py
│   └── banking_api.py
│
└── database/
    ├── __init__.py
    ├── db.py
    └── seed_data.py
```

### 8. Installation and Setup

**Prerequisites**
- Python installed.
- Visual Studio Code or another Python editor.
- A Google Gemini API key for AI-powered functionality.

**Step 1: Open the project directory**

```powershell
cd "C:\Users\kamalesh\Documents\Multi-Agent Banking AI MVP"
```

**Step 2: Install dependencies**

```powershell
python -m pip install -r requirements.txt
```

**Step 3: Configure environment variables**

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder with your own API key. Confirm that the selected model is available to your API account.

**Step 4: Initialize the simulated database**

```powershell
python -m database.seed_data
```

**Step 5: Launch the application**

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

### 9. Testing

Use the following manual test scenarios:

| Test | Input | Expected behavior |
|---|---|---|
| TC01 | Show my balance | Banking Agent returns the selected customer's balance |
| TC02 | Show my recent transactions | Banking Agent displays available transactions |
| TC03 | Show my customer profile | Banking Agent retrieves customer information |
| TC04 | Show my existing loans | Banking Agent retrieves loan records |
| TC05 | Check transaction TX104 for suspicious activity | Risk/Fraud Agent reports configured indicators |
| TC06 | Am I eligible for a loan of ₹3 lakh? | Credit/Loan Agent returns a demo eligibility result |
| TC07 | Ask an unrelated question | Supervisor reports an unsupported request |
| TC08 | Use an unknown customer ID | Application reports that the customer was not found |

### 10. Security and Limitations

- All customer information is fictional.
- The application does not connect to real banking systems.
- Risk analysis uses demonstration rules and is not a production fraud-detection model.
- Loan eligibility rules are illustrative and must not be used for real lending decisions.
- Gemini API credentials are stored in `.env`, which is excluded through `.gitignore`.
- Production deployment would require authentication, authorization, audit logging, secure API integration, stronger validation, and additional testing.

### 11. Future Enhancements

- Add authentication and role-based access control.
- Integrate secure, authorized banking APIs.
- Introduce a trained fraud-detection model.
- Add a transaction approval workflow with human review.
- Improve agent observability and automated testing.
- Add monitoring, audit trails, and deployment support.

### 12. Conclusion

Wrench Wise Banking AI demonstrates how a supervisor-orchestrator can coordinate multiple specialized agents in a simulated banking environment. By combining Python-based banking tools, SQLite, Gemini, and Streamlit, the project illustrates multi-agent automation and natural-language interaction in a practical financial-services use case.





### 13. Output

#### userinterface


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cc5c202f-90e8-4cfa-9b75-37bc0ad9682b" />


#### person change


<img width="370" height="915" alt="image" src="https://github.com/user-attachments/assets/15330e2c-617f-4226-95a7-88f81d834c74" />


#### AI-responce


<img width="1528" height="913" alt="image" src="https://github.com/user-attachments/assets/03a087ba-5965-4b57-8f34-8a3d2e3512d9" />
<img width="1347" height="413" alt="image" src="https://github.com/user-attachments/assets/104c0b92-9e02-48c0-b13d-cac6bc676ba1" />
<img width="1346" height="647" alt="image" src="https://github.com/user-attachments/assets/4d54a88a-6295-4310-843b-4f1a92103ebd" />



