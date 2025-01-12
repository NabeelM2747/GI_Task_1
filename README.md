# CSV Upload API with Django REST Framework

**Project Overview:**
This project implements an API endpoint for uploading user data from a CSV file using Django REST Framework. The API
validates the uploaded data and saves valid records to the database.

**Prerequisites**

* Python 3.x
* Django 3.x or higher
* Django REST Framework
* A database (SQLite is used by default)

**Setup Instructions**

1. Clone the Repository:
   `git clone <repository-url>`
   `cd <repository-directory>`
2. Create a Virtual Environment
   `python -m venv venv`
   `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`
3. Install Requirements:
   Use the existing requirements.txt file to install the necessary packages:
4. Apply Migrations:
   Run the following command to set up your database:
5. Run the Development Server:
   Start the Django development server:
6. Access the API:
   Open your web browser or Postman and navigate to:
   [http://127.0.0.1:8000/csv_upload](http://127.0.0.1:8000/csv_upload)

**Testing the API**
To test the CSV upload functionality:

1. Use the Sample CSV File:
   A sample CSV file named `CSV_Sample_File.csv` is included in the repository. This file contains example user data
   formatted correctly for testing.
2. Upload a CSV File:

* In Postman, create a new POST request to [http://127.0.0.1:8000/csv_upload](http://127.0.0.1:8000/csv_upload).
* In the Body tab, select form-data.
* Set the key as file and choose your CSV_Sample_File.csv file from the repository.

3. Send the Request:
   Click on "Send" to upload the CSV file. You should receive a JSON response indicating how many records were saved and
   how many were rejected.