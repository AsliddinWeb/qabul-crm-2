import uuid
import os
import base64

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetPassportInfoFromGov(APIView):
    permission_classes = [IsAuthenticated]

    """
    Tashqi API orqali pasport seriyasi, raqami va tug‘ilgan sanasi asosida shaxsiy ma’lumotlarni olish
    """

    @swagger_auto_schema(
        operation_summary="Pasport bo‘yicha shaxsiy ma’lumot olish",
        manual_parameters=[
            openapi.Parameter('series', openapi.IN_QUERY, description="Pasport seriyasi (masalan: AB)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('number', openapi.IN_QUERY, description="Pasport raqami (masalan: 6777651)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('birth_date', openapi.IN_QUERY, description="Tug‘ilgan sana (format: YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response(description="Tashqi API'dan muvaffaqiyatli javob"),
            400: "Parametrlar noto‘liq",
            500: "Server yoki API xatosi"
        }
    )
    def get(self, request):
        document_series = request.GET.get('series')
        document_number = request.GET.get('number')
        birth_date = request.GET.get('birth_date')  # format: YYYY-MM-DD

        if not all([document_series, document_number, birth_date]):
            return Response({"error": "series, number, and birth_date are required"}, status=400)

        url = settings.PASSPORT_API
        params = {
            "documentSeries": document_series,
            "documentNumber": document_number,
            "pinfl": "",
            "dateOfBirth": datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d.%m.%Y"),
            "INN": "",
            "identityDocumentId": 2
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                returned_data = {}
                
                # Parse data
                returned_data["full_name"] = data.get("fullname")

                returned_data["first_name"] = data.get("firstname")
                returned_data["last_name"] = data.get("familyname")
                returned_data["second_name"] = data.get("lastname")

                returned_data["birth_date"] = data.get("dateofbirth")
                returned_data["passport_series"] = f"{data.get('CheckResult').get('documentseries')}{data.get('CheckResult').get('documentnumber')}"
                returned_data["passport_number"] = data.get("pinfl")
                returned_data["given_by"] = data.get("DocumentTables")[0].get("dateofissue")
                returned_data["address"] = data.get("LivePlaceTables")[0].get("address")

                # Rasmni saqlash (agar mavjud bo‘lsa)
                base64_photo = data.get("base64photo")
                if base64_photo:
                    file_name = f"{uuid.uuid4()}.jpg"
                    folder_path = os.path.join(settings.MEDIA_ROOT, "applications/passport")
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, file_name)

                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(base64_photo))

                    photo_url = f"https://qabul-api.xiuedu.uz{settings.MEDIA_URL}applications/passport/{file_name}"
                    returned_data["photo_url"] = photo_url

                return Response(returned_data, status=200)
            else:
                return Response({
                    "error": "Tashqi API xatosi",
                    "status": response.status_code,
                    "message": response.text
                }, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
