from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reports.services import ReportingService


class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReportingService().monthly(request.user, request.query_params.get("month", "")))


class YearlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReportingService().yearly(request.user, request.query_params.get("year", "")))


class InterestReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReportingService().interest(request.user))


class PrincipalReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReportingService().principal(request.user))


class VehicleCostsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReportingService().vehicle_costs(request.user))


class FundingGapsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = ReportingService.parse_date_param(request.query_params.get("start"))
        end = ReportingService.parse_date_param(request.query_params.get("end"))
        return Response(ReportingService().funding_gaps(request.user, start, end))
