from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from security.serializers import MyTokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema


class MyTokenObtainPairView(APIView):
    @swagger_auto_schema(
        request_body=MyTokenObtainPairSerializer,
        responses={200: "Token generated successfully"},
    )
    def post(self, request):
        serializer = MyTokenObtainPairSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
