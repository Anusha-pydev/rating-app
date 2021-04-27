from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis import serializers


class CalculatePremiumView(APIView):
    @swagger_auto_schema(
        operation_description="Calculate Final Quoted Premium",
        request_body=serializers.QuoteSerializer,
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, title="success"
                    ),
                    "final_premium": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, title="Final Quoted Premium Amount"
                    ),
                },
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, title="failure"
                    ),
                    "error": openapi.Schema(
                        type=openapi.TYPE_OBJECT, title="Error Reason"
                    ),
                },
            ),
        },
    )
    def post(self, request):
        """
        # Create transaction with single api hit.
        """
        requested_data = request.data
        serializer = serializers.QuoteSerializer(data=requested_data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            premium = serializer.calculate_premium(validated_data)
            return Response(
                {
                    "success": True,
                    "final_premium": round(premium),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
