from tools.banking_api import (
    get_customer,
    get_balance,
    get_transactions,
    get_loans,
)

print("Customer:", get_customer("C1001"))
print("Balance:", get_balance("C1001"))
print("Transactions:", get_transactions("C1001"))
print("Loans:", get_loans("C1001"))