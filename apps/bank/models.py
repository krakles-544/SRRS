from django.db import models
from apps.records.models import FinancialDocument
from datetime import date, timedelta

class Account(models.Model):
    ACCOUNT_TYPES = [('savings', 'Savings'),
                     ('current', 'Current'),]
    account_number = models.CharField(max_length=20, unique=True)
    account_holder = models.CharField(max_length=255)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_holder} - {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES =[
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(FinancialDocument, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.account.account_number})"

    
class Loan(models.Model):
    LOAN_STATUS =[
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('defaulted', 'Defaulted'), 
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    expected_repayment = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default='active')
    document = models.ForeignKey(FinancialDocument, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
       self.expected_repayment = self.amount + (self.amount * (self.interest_rate / 100))
       super().save(*args, **kwargs)

            

    def __str__(self):
        return f"Loan of {self.amount} - {self.get_status_display()} ({self.account.account_number})"


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    expected_repayment = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    penalty_interest = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(FinancialDocument, on_delete=models.SET_NULL, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.expected_repayment:
            self.expected_repayment = self.loan.expected_repayment

        self.balance = self.expected_repayment - self.amount_paid

        if self.loan.end_date < date.today() and self.balance > 0:
            weeks_late = (date.today() - self.loan.end_date).days // 7
            penalty_rate = 2.0
            self.penalty_interest = (self.balance * (penalty_rate / 100)) * weeks_late

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Repayment of {self.amount_paid} for loan{self.loan.id} on {self.payment_date}"



