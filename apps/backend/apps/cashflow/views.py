from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cashflow.services import CashflowService
from apps.reports.services import ReportingService, RiskAnalysisService


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ReportingService().dashboard_summary(
            user=request.user,
            range_name=request.query_params.get("range", "monthly"),
            date_value=request.query_params.get("date"),
        )
        return Response(data)


class DashboardCashflowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = ReportingService.parse_date_param(request.query_params.get("start"))
        end = ReportingService.parse_date_param(request.query_params.get("end"))
        return Response(CashflowService().build(request.user, start, end))


class DashboardRiskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = ReportingService.parse_date_param(request.query_params.get("start"))
        end = ReportingService.parse_date_param(request.query_params.get("end"))
        return Response(RiskAnalysisService().build(request.user, start, end))
