from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from security.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(APIView):
    def post(self, request):
        serializer = MyTokenObtainPairSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
