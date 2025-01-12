from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import io
from .models import User


class CSVUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('csv_upload')  # Update this with your actual view name

    def create_csv_file(self, content):
        file = io.StringIO()
        file.write(content)
        file.seek(0)
        return file

    def test_upload_valid_csv(self):
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Smith,jane@example.com,25\n"
        file = self.create_csv_file(csv_content)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_upload_invalid_csv(self):
        csv_content = "name,email,age\nInvalid User,invalid-email,-5\n"
        file = self.create_csv_file(csv_content)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(len(response.data["Main Response"]["validation_errors"]), 1)

    def test_no_file_provided(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No file provided", response.data["error"])

    def test_upload_non_csv_file(self):
        file = io.BytesIO(b"Not a CSV file")
        file.name = "test.txt"
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("File is not a CSV type", response.data["error"])
