
from orchestrator import route_request

questions = [
    "Check my balance for customer C1001",
    "Show transaction history for C1001",
    "Is transaction TX104 suspicious for C1001?",
    "Can customer C1001 qualify for a 3 lakh loan?",
    "Tell me a joke",
]

for question in questions:
    print("\nQuestion:", question)
    print("Response:", route_request(question))
