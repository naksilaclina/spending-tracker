from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authn.views import AuthMeView
from apps.cashflow.views import DashboardCashflowView, DashboardRiskView, DashboardSummaryView
from apps.credit_cards.views import CreditCardAccountViewSet, CreditCardPaymentViewSet
from apps.expenses.views import ExpenseEntryViewSet
from apps.finance.views import CategoryViewSet, TemplateViewSet
from apps.fixed_rules.views import FixedExpenseRuleViewSet, FixedIncomeRuleViewSet
from apps.income.views import IncomeEntryViewSet
from apps.installments.views import InstallmentPurchaseViewSet
from apps.loans.views import LoanViewSet
from apps.reports.views import FundingGapsReportView, InterestReportView, MonthlyReportView, PrincipalReportView, VehicleCostsReportView, YearlyReportView
from apps.settings_app.views import SettingsView
from apps.vehicles.views import VehicleExpenseViewSet, VehicleViewSet

router = DefaultRouter(trailing_slash=False)
router.register("categories", CategoryViewSet, basename="category")
router.register("expenses", ExpenseEntryViewSet, basename="expense")
router.register("incomes", IncomeEntryViewSet, basename="income")
router.register("templates", TemplateViewSet, basename="template")
router.register("fixed-expense-rules", FixedExpenseRuleViewSet, basename="fixed-expense-rule")
router.register("fixed-income-rules", FixedIncomeRuleViewSet, basename="fixed-income-rule")
router.register("loans", LoanViewSet, basename="loan")
router.register("installment-purchases", InstallmentPurchaseViewSet, basename="installment-purchase")
router.register("credit-cards", CreditCardAccountViewSet, basename="credit-card")
router.register("credit-card-payments", CreditCardPaymentViewSet, basename="credit-card-payment")
router.register("vehicles", VehicleViewSet, basename="vehicle")
router.register("vehicle-expenses", VehicleExpenseViewSet, basename="vehicle-expense")

from django.http import JsonResponse


def health_view(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health", health_view, name="health"),
    path("auth/me", AuthMeView.as_view(), name="auth-me"),
    path("dashboard/summary", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("dashboard/cashflow", DashboardCashflowView.as_view(), name="dashboard-cashflow"),
    path("dashboard/risk", DashboardRiskView.as_view(), name="dashboard-risk"),
    path("reports/monthly", MonthlyReportView.as_view(), name="report-monthly"),
    path("reports/yearly", YearlyReportView.as_view(), name="report-yearly"),
    path("reports/interest", InterestReportView.as_view(), name="report-interest"),
    path("reports/principal", PrincipalReportView.as_view(), name="report-principal"),
    path("reports/vehicle-costs", VehicleCostsReportView.as_view(), name="report-vehicle-costs"),
    path("reports/funding-gaps", FundingGapsReportView.as_view(), name="report-funding-gaps"),
    path("settings", SettingsView.as_view(), name="settings"),
    path("", include(router.urls)),
]
