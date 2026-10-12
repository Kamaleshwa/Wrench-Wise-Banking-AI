
import json
import os
import re

from dotenv import load_dotenv
from google import genai

from agents.banking_agent import handle_banking_request
from agents.risk_agent import handle_risk_request
from agents.credit_agent import handle_credit_request

# Load Gemini configuration from the .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# --------------------------------------------------
# 1. Understand the user's request
# --------------------------------------------------

def fallback_understanding(message):
    """Identify common banking requests without Gemini."""

    text = message.lower()

    customer_match = re.search(r"\bC\d+\b", message, re.I)
    transaction_match = re.search(r"\bTX\d+\b", message, re.I)

    amount = None

    # Detect amounts such as ₹50000 or Rs. 50,000
    amount_match = re.search(
        r"(?:₹\s*|rs\.?\s*)(\d+(?:,\d{3})*(?:\.\d+)?)",
        message,
        re.I,
    )

    if amount_match:
        amount = float(amount_match.group(1).replace(",", ""))

    # Detect amounts such as 3 lakh or 2.5 lakhs
    lakh_match = re.search(
        r"(\d+(?:\.\d+)?)\s*lakhs?\b",
        text,
        re.I,
    )

    if lakh_match:
        amount = float(lakh_match.group(1)) * 100000

    # Determine intent
    if transaction_match or any(
        word in text for word in ("fraud", "suspicious", "risk")
    ):
        intent = "risk"

    elif any(
        word in text
        for word in (
            "eligible",
            "eligibility",
            "qualify",
            "loan amount",
            "apply for a loan",
            "loan of",
        )
    ):
        intent = "credit"

    elif "balance" in text:
        intent = "balance"

    elif any(
        word in text for word in ("transaction", "history", "payments")
    ):
        intent = "transactions"

    elif "loan" in text:
        intent = "loans"

    elif any(
        word in text
        for word in (
            "customer details",
            "customer information",
            "profile",
            "who am i",
        )
    ):
        intent = "customer"

    else:
        intent = "unknown"

    return {
        "intent": intent,
        "customer_id": (
            customer_match.group(0).upper()
            if customer_match else None
        ),
        "transaction_id": (
            transaction_match.group(0).upper()
            if transaction_match else None
        ),
        "amount": amount,
    }


def understand_request(message):
    """Use Gemini to classify the request, with a fallback."""

    fallback = fallback_understanding(message)

    if client is None:
        return fallback

    prompt = f"""
You classify requests for a simulated banking application.

Choose exactly one intent:
balance, customer, transactions, loans, risk, credit, unknown.

Rules:
- balance: account balance
- customer: customer profile
- transactions: transaction history
- loans: existing loans
- risk: fraud or suspicious transaction analysis
- credit: eligibility for a new loan or a requested loan amount
- unknown: unrelated or unsupported requests

Extract:
- customer_id: ID such as C1001, or null
- transaction_id: ID such as TX104, or null
- amount: requested loan amount in rupees as a number, or null

Convert lakh amounts to rupees. For example, 3 lakh = 300000.
Return JSON only with keys:
intent, customer_id, transaction_id, amount.

User message:
{message}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        data = json.loads(response.text)

        allowed_intents = {
            "balance",
            "customer",
            "transactions",
            "loans",
            "risk",
            "credit",
            "unknown",
        }

        if data.get("intent") not in allowed_intents:
            return fallback

        # Validate extracted IDs before using them
        customer_id = data.get("customer_id")
        transaction_id = data.get("transaction_id")
        amount = data.get("amount")

        if not isinstance(customer_id, str) or not re.fullmatch(
            r"C\d+", customer_id, re.I
        ):
            customer_id = fallback["customer_id"]

        if not isinstance(transaction_id, str) or not re.fullmatch(
            r"TX\d+", transaction_id, re.I
        ):
            transaction_id = fallback["transaction_id"]

        try:
            amount = float(amount) if amount is not None else fallback["amount"]
        except (ValueError, TypeError):
            amount = fallback["amount"]

        if amount is not None and (amount <= 0 or amount > 1000000000):
            amount = None

        return {
            "intent": data["intent"],
            "customer_id": customer_id,
            "transaction_id": transaction_id,
            "amount": amount,
        }

    except Exception as error:
        print("Gemini intent detection failed:", error)
        return fallback


# --------------------------------------------------
# 2. Supervisor / Orchestrator
# --------------------------------------------------

def route_request(message, default_customer_id="C1001"):
    """Route the request to the appropriate specialized agent."""

    details = understand_request(message)

    customer_id = (
        details.get("customer_id") or default_customer_id
    )
    intent = details.get("intent", "unknown")

    # Banking Agent
    if intent in {
        "balance",
        "customer",
        "transactions",
        "loans",
    }:
        result = handle_banking_request(customer_id, intent)

    # Risk / Fraud Agent
    elif intent == "risk":
        result = handle_risk_request(
            customer_id,
            details.get("transaction_id"),
        )

    # Credit / Loan Agent
    elif intent == "credit":
        amount = details.get("amount")

        if amount is None:
            return {
                "agent": "Supervisor",
                "intent": intent,
                "customer_id": customer_id,
                "error": (
                    "Please specify a loan amount, "
                    "for example: Am I eligible for ₹3 lakh?"
                ),
            }

        result = handle_credit_request(customer_id, amount)

    # Unsupported request
    else:
        return {
            "agent": "Supervisor",
            "intent": "unknown",
            "customer_id": customer_id,
            "error": (
                "I couldn't identify that banking request. "
                "Ask about your balance, transactions, loans, "
                "fraud indicators, or loan eligibility."
            ),
        }

    return {
        "agent": result.get("agent", "Supervisor"),
        "intent": intent,
        "customer_id": customer_id,
        "result": result,
    }


# --------------------------------------------------
# 3. Generate a natural-language response
# --------------------------------------------------

def generate_natural_response(user_message, routed_result):
    """Explain tool results in simple English."""

    if routed_result.get("error"):
        return routed_result["error"]

    agent_result = routed_result.get("result", {})

    if agent_result.get("error"):
        return agent_result["error"]

    # Gemini explains the results returned by the agents.
    # It does not make banking decisions.
    if client is not None:
        prompt = f"""
You are the response assistant for a simulated banking application.

Explain the supplied result in simple, clear English.
Use only the facts contained in the tool result.
Never invent balances, transactions, or loan decisions.
Do not claim that a transaction is fraudulent merely because
it has risk indicators.
Explain that credit eligibility is illustrative, not a real
lending decision.
Keep the response concise.

User's question:
{user_message}

Agent result (JSON):
{json.dumps(routed_result, default=str)}

Write only the customer-facing answer.
"""

        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            if response.text:
                return response.text.strip()

        except Exception as error:
            print("Gemini response generation failed:", error)

    # Fallback responses when Gemini is unavailable
    intent = routed_result.get("intent")

    # Banking Agent wraps the actual data in result["result"]
    data = agent_result.get("result", {})

    if intent == "balance" and "balance" in data:
        return (
            "Your simulated account balance is "
            f"₹{data['balance']:,.2f}."
        )

    if intent == "customer" and data:
        return (
            f"Customer name: {data.get('name', 'Unknown')}\n\n"
            f"Customer ID: {data.get('customer_id', 'Unknown')}\n\n"
            f"Monthly income: "
            f"₹{data.get('monthly_income', 0):,.2f}\n\n"
            f"Credit score: {data.get('credit_score', 'Unknown')}"
        )

    if intent == "transactions":
        transactions = data if isinstance(data, list) else []

        if not transactions:
            return "No transactions were found for this customer."

        lines = ["Here are the recent simulated transactions:"]

        for tx in transactions:
            lines.append(
                f"- {tx['transaction_id']}: "
                f"₹{tx['amount']:,.2f} "
                f"({tx['transaction_type']}) — "
                f"{tx['description']} [{tx['status']}]"
            )

        return "\n".join(lines)

    if intent == "loans":
        loans = data if isinstance(data, list) else []

        if not loans:
            return "No existing loans were found for this customer."

        lines = ["Here are the existing simulated loans:"]

        for loan in loans:
            lines.append(
                f"- {loan['loan_id']}: "
                f"₹{loan['amount']:,.2f} — {loan['status']}"
            )

        return "\n".join(lines)

    if intent == "risk":
        results = agent_result.get("results", [])

        if not results:
            return "No matching transactions were found for risk analysis."

        lines = ["Simulated transaction risk analysis:"]

        for item in results:
            reasons = ", ".join(item.get("reasons", []))

            if not reasons:
                reasons = "No configured risk indicators detected"

            lines.append(
                f"- {item['transaction_id']}: "
                f"{item['risk_level']} risk. {reasons}."
            )

        lines.append(
            "These are rule-based demo results, not proof of fraud."
        )
        return "\n".join(lines)

    if intent == "credit":
        eligible = agent_result.get("eligible_under_demo_rules")

        if eligible is not None:
            amount = agent_result.get("requested_amount", 0)

            status = (
                "meets the demo eligibility rules"
                if eligible
                else "does not meet the demo eligibility rules"
            )

            return (
                f"Requested loan amount: ₹{amount:,.2f}.\n\n"
                f"The customer {status}.\n\n"
                "This is an illustrative result, not a real "
                "lending decision."
            )

    return (
        "The request was processed, but I couldn't create a summary. "
        "Please try another supported banking request."
    )
