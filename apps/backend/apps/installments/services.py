from dateutil.relativedelta import relativedelta

from apps.core.utils import split_amount
from apps.installments.models import InstallmentPurchase, InstallmentPurchaseItem


class InstallmentScheduleService:
    def regenerate(self, purchase: InstallmentPurchase) -> list[InstallmentPurchaseItem]:
        locked = list(purchase.items.filter(is_locked=True).order_by("installment_number"))
        locked_count = len(locked)
        remaining_count = max(purchase.installment_count - locked_count, 0)
        principal_total = purchase.principal_total or purchase.total_amount
        interest_total = purchase.interest_total or 0
        fee_total = purchase.fee_total or 0
        remaining_principal = principal_total - sum(item.principal_amount for item in locked)
        remaining_interest = interest_total - sum(item.interest_amount for item in locked)
        remaining_fee = fee_total - sum(item.fee_amount for item in locked)

        purchase.items.filter(is_locked=False).delete()

        principal_parts = split_amount(remaining_principal, remaining_count)
        interest_parts = split_amount(remaining_interest, remaining_count)
        fee_parts = split_amount(remaining_fee, remaining_count)
        items: list[InstallmentPurchaseItem] = []
        start_number = locked_count + 1
        base_date = purchase.first_installment_date + relativedelta(months=locked_count)

        for index in range(remaining_count):
            item = InstallmentPurchaseItem.objects.create(
                user=purchase.user,
                installment_purchase=purchase,
                installment_number=start_number + index,
                due_on=base_date + relativedelta(months=index),
                amount_total=principal_parts[index] + interest_parts[index] + fee_parts[index],
                principal_amount=principal_parts[index],
                interest_amount=interest_parts[index],
                fee_amount=fee_parts[index],
            )
            items.append(item)
        return locked + items
