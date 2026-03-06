from django.db import models


class CategoryKind(models.TextChoices):
    EXPENSE = "expense", "Expense"
    INCOME = "income", "Income"


class TemplateType(models.TextChoices):
    NORMAL = "normal", "Normal"
    FIXED_EXPENSE = "fixed_expense", "Fixed expense"
    FIXED_INCOME = "fixed_income", "Fixed income"
    LOAN = "loan", "Loan"
    INSTALLMENT_PURCHASE = "installment_purchase", "Installment purchase"
    CREDIT_CARD_PAYMENT = "credit_card_payment", "Credit card payment"
    VEHICLE_EXPENSE = "vehicle_expense", "Vehicle expense"


class ExpenseStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    SKIPPED = "skipped", "Skipped"
    CANCELLED = "cancelled", "Cancelled"


class ExpenseEntryType(models.TextChoices):
    ONE_TIME = "one_time", "One time"
    RECURRING = "recurring", "Recurring"
    FIXED = "fixed", "Fixed"
    INSTALLMENT = "installment", "Installment"
    LOAN_PAYMENT = "loan_payment", "Loan payment"
    CREDIT_CARD_PAYMENT = "credit_card_payment", "Credit card payment"
    VEHICLE = "vehicle", "Vehicle"


class IncomeStatus(models.TextChoices):
    EXPECTED = "expected", "Expected"
    RECEIVED = "received", "Received"
    MISSED = "missed", "Missed"
    DELAYED = "delayed", "Delayed"
    CANCELLED = "cancelled", "Cancelled"


class RecurrenceAppliesTo(models.TextChoices):
    EXPENSE = "expense", "Expense"
    INCOME = "income", "Income"


class RecurrenceFrequency(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"


class LoanStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    PAID_OFF = "paid_off", "Paid off"
    RESTRUCTURED = "restructured", "Restructured"
    DEFAULTED = "defaulted", "Defaulted"


class InstallmentStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    DELAYED = "delayed", "Delayed"
    CANCELLED = "cancelled", "Cancelled"


class CreditCardPaymentStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    PARTIAL = "partial", "Partial"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"


class VehicleExpenseType(models.TextChoices):
    FUEL = "fuel", "Fuel"
    MAINTENANCE = "maintenance", "Maintenance"
    REPAIR = "repair", "Repair"
    INSURANCE = "insurance", "Insurance"
    PARKING = "parking", "Parking"
    TOLL = "toll", "Toll"
    TAX = "tax", "Tax"
    FINE = "fine", "Fine"
    TIRE = "tire", "Tire"
    WASH = "wash", "Wash"
    OTHER = "other", "Other"


class IncomeProjectionMode(models.TextChoices):
    EXPECTED = "expected", "Expected"
    RECEIVED_ONLY = "received_only", "Received only"


class OnboardingState(models.TextChoices):
    NEW = "new", "New"
    PROFILE_COMPLETED = "profile_completed", "Profile completed"
    ACTIVE = "active", "Active"
