
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI,ChatOpenAI
from common_utils.Config import Config
from pymongo import MongoClient
import os
import pandas as pd
from common_utils.html_utils import get_image_paths,generate_html_output


client = MongoClient(Config.MONGODB_URI_SERVERLESS)
db = client["Nexus360"]
collection = db["Uploaded_Documents"]





def csv_answer(query,documentid):

    try:

        document = collection.find_one({"DocumentID": documentid})
        if document is None:
            print("Document not found.")
            return
        file_data_binary = document.get("FileData")
        output_file_name = "1.csv"
        output_file_path = os.path.join(os.getcwd(), output_file_name)
        with open(output_file_path, "wb") as output_file:
                output_file.write(file_data_binary)
        df = pd.read_csv(output_file_path, encoding='latin-1')
        agent = create_pandas_dataframe_agent(ChatOpenAI(temperature=0,model="gpt-4-turbo"), df, verbose=True)
        # question = query
        prompt = """If the result of the operation is an image,make sure avoiding plt.show() but save it as a PNG file in the current working directory.if one task encountered error please mention that cause of error in text format"""
        # prompt = """if the operation yields multiple images,or a single image convert those images in to a single PNG file,make sure avoiding plt.show() but save it as a PNG file in current working directory."""
        response = agent(query+prompt)
        image_paths = get_image_paths()
        # print(image_paths)
        html_output = generate_html_output(response['output'], image_paths)
        # print(response)
        # print(type(response))
        os.remove(output_file_path)

        return html_output
    except Exception as exe:
        return generate_html_output("an error occured "+str(exe))