from flask_jwt_extended import JWTManager
# from common_utils.Config import Config
from common_utils.logging_utils import setup_logger
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from src.ingestpdf import main as ingest_main,ingest_main1
from src.ingestdocx import main as ingest_document
from src.retrievemongo import retrieve_file_from_mongodb
from db_utils.mongo_oprationsqa import delete_from_mongodb
from src.retrieve_csv import retrieve_csv_file_from_mongodb
from src.ingest_csv import ingest_csv
from src.qa1 import qa
import os


logger = setup_logger()
app = Flask(__name__)



CORS(app, methods=["GET", "POST"], resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = '*'

# Set the upload folder
UPLOAD_FOLDER = 'docs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Testing Purpose
@app.route('/test')
@cross_origin()
def greet():
    result = jsonify({"status":"working successfully!"})
    return result

@app.route('/ingest', methods=['POST'])
@cross_origin()
#@jwt_required()
def upload_file():
    data = request.get_json()
    doc_id = data.get('DocumentID')
    # base64_doc = data.get('FileData')
    filename = data.get('FileName')
    space_name = data.get('SpaceName')
    space_id = data.get('SpaceID')
    uploader_name = data.get('UploadedBy')
    updated_time = data.get('UpdatedDate')
    # print(data)

    try:
        metadata = {
            'documentid': doc_id,
            'filename': filename,
            'spacename': [space_name],
            'spaceid':space_id,
            'uploadername': uploader_name,
            "updateddate" : updated_time
            }
        print(metadata)
                # Check if the filename ends with '.pdf'.for pdf
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in "pdf":
            print(filename.rsplit('.', 1)[1])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            retrieve_file_from_mongodb(doc_id,file_path)
        # Check if the filename ends with '.docx'.for docx file
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() in "docx":
            print(filename.rsplit('.', 1)[1])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            retrieve_file_from_mongodb(doc_id,file_path)
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() in "csv":
            print(filename.rsplit('.', 1)[1])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            retrieve_csv_file_from_mongodb(doc_id,file_path)
        else:
            pass

    except Exception as exe:
        print("error occured "+ str(exe))
            # Process the document
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in "pdf":
        try:
            try:
                ingest_main1(file_path, metadata)
            except:
                ingest_main(file_path, metadata)
        except Exception as exe:
            print("an error occured "+str(exe))

    elif '.' in filename and filename.rsplit('.', 1)[1].lower() in "docx":

        try:
            ingest_document(file_path,metadata)
        except Exception as exe:
            print("error occured "+ str(exe))
    elif '.' in filename and filename.rsplit('.', 1)[1].lower() in "csv":
        try:
            ingest_csv(file_path,metadata)
        except Exception as exe:
            print("error occured "+ str(exe))
        
    else:
        print("wrong file format given")



        


    # Respond with success status
    # os.remove(file_path)
    response = jsonify({"status": "success"}), 201
    return response


@app.route('/qa', methods=['POST'])
@cross_origin()
#@jwt_required()
def questionAnswering():
    try:
        # Get JSON data from the request
        json_data = request.get_json()
        question = json_data.get('question')
        spacename = json_data.get('spacename')
        print(question)
        print(spacename)
        answer = qa(question,spacename)
        logger.info(f"answer is: {answer}")

    #     #mongo_db.insert_doc(user_id, question, answer, source)
        return jsonify({"question":question, "answer":answer}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/delete', methods=['POST'])
@cross_origin()
#@jwt_required()
def DeleteDocuments():
    try:
        json_data = request.get_json()
        print(json_data)
        doc_id = json_data.get('DocumentID')
        delete_from_mongodb(doc_id)
        response = f"deleted document with document id {doc_id}"
        response = jsonify({"status":response})
        return response, 204
    except Exception as e:
        return jsonify({"error":str(e)}), 404




if __name__ == '__main__':

    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=False, host="0.0.0.0", port = 5066)


