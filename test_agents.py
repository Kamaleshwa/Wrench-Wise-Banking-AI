
from agents.banking_agent import handle_banking_request
from agents.risk_agent import handle_risk_request
from agents.credit_agent import handle_credit_request

print("\n--- BANKING AGENT ---")
print(handle_banking_request("C1001", "balance"))

print("\n--- RISK AGENT ---")
print(handle_risk_request("C1001", "TX104"))

print("\n--- CREDIT AGENT ---")
print(handle_credit_request("C1001", 300000))
