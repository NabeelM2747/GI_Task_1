import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserValidSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
def csv_upload(request):
    if request.method == 'POST':
        valid_records = []
        rejected_records = []
        validation_errors = []
        csv_file = request.FILES.get('file')

        # Validate that the existence of requested file in variable
        if not csv_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File is not a CSV type"}, status=status.HTTP_400_BAD_REQUEST)

        # CSV file parsing row wise and content validation based on the rules (LNo:27 - LNo: 38)
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        csv_data = [row for row in reader]
        for row in csv_data:
            serializer = UserValidSerializer(data=row)
            if serializer.is_valid():
                valid_records.append(serializer.validated_data)
            else:
                rejected_records.append(row)
                validation_errors.append({
                    "Rejected_Data": row,
                    "errors": serializer.errors})

        # Save valid records to the database
        if valid_records:
            User.objects.bulk_create([User(**record) for record in valid_records])
        saved_users = User.objects.all()
        serialized_data = UserValidSerializer(saved_users, many=True).data
        total_users = len(saved_users)
        User_Data = {
            "Total_Count": total_users,
            "All_Users": serialized_data
        }
        response_data = {
            "total_saved": len(valid_records),
            "total_rejected": len(rejected_records),
            "validation_errors": validation_errors,
        }
        return Response({"Main Response": response_data, "csv_data": csv_data, "Total_Users": User_Data},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid Method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
