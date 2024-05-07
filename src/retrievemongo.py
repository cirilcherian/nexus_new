from pymongo import MongoClient
from common_utils.Config import Config
# from bson import Binary
import base64


client = MongoClient(Config.MONGODB_URI_SERVERLESS)
db = client["Nexus360"]
collection = db["Uploaded_Documents"]

def retrieve_file_from_mongodb(document_id, output_file_path):
    # Connect to MongoDB


    # Retrieve the document with the given ID
    document = collection.find_one({"DocumentID": document_id})
    file_data_binary = document.get("FileData")
    # print(file_data_binary)
    


    if document is None:
        print("Document not found.")
        return
    
    try:
    # Decode Base64 data
        # pdf_data = base64.b64decode(file_data_binary)
        # pdf_data = codecs.decode(file_data_binary, 'base64')
        # pdf_data = base64.decodebytes(file_data_binary.encode('ascii'))
        # decoded_data = base64.b64decode(file_data_binary)
        # utf8_string = decoded_data.decode('utf-8')

        # Write decoded data to a PDF file
        # with open("output.pdf", "wb") as pdf_file:
        #     pdf_file.write(pdf_data)

        base64_data = base64.b64encode(file_data_binary).decode('utf-8')
        file_data = base64.b64decode(base64_data)

        with open(output_file_path, "wb") as output_file:
            output_file.write(file_data)

            print("PDF file created successfully.")
            return
    except Exception as e:
        print("An error occurred:", str(e))







    # Retrieve the binary data from the document
    # file_data_binary = document.get("FileData")
    # print(type(file_data_binary))
    # str1 = base64.b64decode(file_data_binary)
    # if not isinstance(file_data_binary, Binary):
    #     print("FileData field is not binary.")
    #     return
    
    

    # Get the binary data as bytes
    # print(file_data_binary)
    # file_data_bytes = file_data_binary
    # base64_data = base64.b64encode(file_data_bytes).decode('utf-8')
    # file_data = base64.b64decode(base64_data)
    # OR if you need to access the binary data as bytes use:
    # file_data_bytes = file_data_binary.to_bytes()

    # Write the binary data to a PDF file
    # with open(output_file_path, "wb") as output_file:
    #     output_file.write(str1)


    # if document is None:
    #     print("Document not found.")
    #     return

    # # Retrieve the base64 encoded data from the document
    # file_data_base64 = document.get("FileData")
    # if file_data_base64 is None:
    #     print("FileData field is empty.")
    #     return

    # # Decode the base64 data
    # file_data = base64.b64decode(file_data_base64)
    # print(file_data)

    # # Write the binary data to a PDF file
    # with open(output_file_path, "wb") as output_file:
    #     output_file.write(file_data)
    
    

    


