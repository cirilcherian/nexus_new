# import pymongo
# import base64
from pymongo import MongoClient
from common_utils.Config import Config
# from bson import Binary
import base64


client = MongoClient(Config.MONGODB_URI_SERVERLESS)
db = client["Nexus360"]
collection = db["Uploaded_Documents"]

def retrieve_csv_file_from_mongodb(document_id, output_file_path):
    try:
        # Retrieve the document with the given ID
        document = collection.find_one({"DocumentID": document_id})

        if document is None:
            print("Document not found.")
            return

        # Extract file data
        file_data_binary = document.get("FileData")

        # Decode Base64 data
        # file_data_decoded = base64.b64decode(file_data_binary)

        # Write decoded data to a file
        with open(output_file_path, "wb") as output_file:
            output_file.write(file_data_binary)

        print("csv file created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == '__main__':       
    document_id = "your_document_id"
    output_file_path = "output.csv"
    # collection = your_mongodb_collection  # Replace with your MongoDB collection object
    retrieve_csv_file_from_mongodb(document_id,output_file_path)