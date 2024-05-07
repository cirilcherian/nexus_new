from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain_openai import ChatOpenAI
# import chardet
from langchain_community.document_loaders import TextLoader
from db_utils.mongo_oprationsqa import save_to_db
import os


def ingest_csv(file_path,metadata):
    try:

        

        # def detect_encoding(file_path):
            # Read a small chunk of the file to detect its encoding
        #     with open(file_path, 'rb') as f:
        #         detector = chardet.UniversalDetector()
        #         for line in f:
        #             detector.feed(line)
        #             if detector.done:
        #                 break
        #         detector.close()
        #     return detector.result['encoding']
        # encoding = detect_encoding(file_path)
    
        # df = pd.read_csv(file_path)
        df = pd.read_csv(file_path, encoding='latin-1')
        agent = create_pandas_dataframe_agent(ChatOpenAI(temperature=0.5,model="gpt-4-turbo"), df, verbose=True)
        question = "Analyse the data frame and explain it.mention all the column names"
        # print(agent.get_prompts)
        try:
            response = agent(question)
        except:
            try:
                # question = "mention all the column names."
                response = agent(question)
                # agent.get_prompts
            except:
                try:
                    question = "mention all the column names."
                    response = agent(question)
                except:
                    print("metadata generation failed")



        print(response["output"])
        # print(response['output'])
        filename1 = metadata['filename']
        documentid1 = metadata['documentid']
        response = f"This is file named {filename1}.The document id for the file is {documentid1}.The data in the csv file is converted to a data frame. "+response['output']
        # print(response)
        # print(metadata)
        with open("1.txt", 'w', encoding="utf-8") as text_file:
            text_file.write(response)
            print("Converted text to txt file")
        loader = TextLoader("1.txt", encoding='utf8')
        documents = loader.load()
        metadata["spacename"].append("Super Admin")
        print(metadata)
        # documents[0].metadata = metadata
        for document in documents:
            document.metadata = metadata
        os.remove("1.txt")
        save_to_db(documents)
        
    except Exception as exe:
        print("error occured "+str(exe))