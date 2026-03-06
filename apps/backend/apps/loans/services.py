from decimal import Decimal

from dateutil.relativedelta import relativedelta

from apps.core.utils import split_amount
from apps.loans.models import Loan, LoanInstallment


class LoanScheduleService:
    def regenerate(self, loan: Loan) -> list[LoanInstallment]:
        locked = list(loan.installments.filter(is_locked=True).order_by("installment_number"))
        locked_count = len(locked)
        remaining_count = max(loan.installment_count - locked_count, 0)
        remaining_principal = loan.principal_total - sum(item.principal_amount for item in locked)
        remaining_interest = loan.interest_total - sum(item.interest_amount for item in locked)
        remaining_fee = loan.fee_total - sum(item.fee_amount for item in locked)

        loan.installments.filter(is_locked=False).delete()

        principal_parts = split_amount(remaining_principal, remaining_count)
        interest_parts = split_amount(remaining_interest, remaining_count)
        fee_parts = split_amount(remaining_fee, remaining_count)
        installments: list[LoanInstallment] = []
        start_number = locked_count + 1
        base_date = loan.first_installment_date + relativedelta(months=locked_count)

        for index in range(remaining_count):
            due_on = base_date + relativedelta(months=index)
            principal_amount = principal_parts[index]
            interest_amount = interest_parts[index]
            fee_amount = fee_parts[index]
            amount_total = principal_amount + interest_amount + fee_amount
            installment = LoanInstallment.objects.create(
                user=loan.user,
                loan=loan,
                installment_number=start_number + index,
                due_on=due_on,
                amount_total=amount_total,
                principal_amount=principal_amount,
                interest_amount=interest_amount,
                fee_amount=fee_amount,
            )
            installments.append(installment)

        if installments:
            loan.end_date = installments[-1].due_on
            loan.save(update_fields=["end_date", "updated_at"])
        return locked + installments
