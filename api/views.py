from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from auth_with_otp.models import UserModel, OtpModel
from .serializers import OtpSerializer, UserModelSerializer, VerifyPhoneNumberSerializer
from .helpers import send_otp

class AuthTotpViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    
    @action(detail=False, methods=['POST'], url_path='req-otp', url_name='request_otp', 
            serializer_class=VerifyPhoneNumberSerializer)
    def request_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.queryset.filter(phone_number=serializer.validated_data['phone_number']).first()

        if user:
            otp_record, created = OtpModel.objects.get_or_create(user=user)
            otp = otp_record.generate_otp()
            message = send_otp(serializer.validated_data['phone_number'], otp)
            if message:
                return Response({"message": "OTP generated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Something wrong happened while sending msg", "erros": message}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({"errors":"Please check your phone number and try again"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='verify-otp', url_name='verify-otp', 
            serializer_class=OtpSerializer)
    def verify_otp(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            otp_record = OtpModel.objects.filter(otp=serializer.data.get('otp_value')).first()

            if otp_record is None:
                return Response({"errors": "Please provide correct OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if otp_record.verify_otp(otp_record.otp):
                return Response({"message":"OTP verified"}, status=status.HTTP_200_OK)
            return Response({"errors": "Please provide correct OTP"})
        except Exception as e:
            return Response({"errors":"Something went wrong ", "message": str(e)},
                             status=status.HTTP_400_BAD_REQUEST)