from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.bank.models import Account, Transaction, Loan, LoanRepayment
from apps.records.models import FinancialDocument
roles_permissions = {
    'Manager': ['add_account', 'change_account', 'view_account', 'add_loan', 'change_loan', 'view_loan', 'view_financial_documents'],
    'Teller': ['add_transaction', 'view_transaction', 'view_financial_documents'],
    'Loan Officer': ['add_loan', 'view_loan', 'add_loanrepayment', 'view_loanrepayment', 'view_financial_documents'],
    'Auditor': ['view_account', 'view_transaction', 'view_loan', 'view_loanrepayment', 'view_financial_documents'],
    'Customer': [],
}

for role, perms in roles_permissions.items():
    group, created = Group.objects.get_or_create(name=role)
    for perm_codename in perms:
        try:
            perm = Permission.objects.get(codename=perm_codename)
            group.permissions.add(perm)
        except Permission.DoesNotExist:
            print(f"Permission not found: {perm_codename}")