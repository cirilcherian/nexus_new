# from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain import hub
from common_utils.embeddings import default_embeddings
from common_utils.Config import Config
from src.csv_answer import csv_answer
from common_utils.HTMLFormatterAI import HTMLFormatter

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers import MergerRetriever
# from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain.memory import ChatMessageHistory
# import getpass
# import os

from typing import Dict, Any
# from langchain_community.chat_models import ChatOpenAI
DB_NAME = "vector_db"
COLLECTION_NAME = "vector_collections"


model = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k", #"gpt-3.5-turbo",
    # model_name="gpt-4",
    temperature="0.3"
    # verbose=True
)


embeddings = default_embeddings()
def qa(query,spacename,search_kwargs: Dict [Any, Any] = {}):

    mongo_uri = Config.MONGODB_URI_CLUSTER
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(mongo_uri,DB_NAME + "." + COLLECTION_NAME,embeddings,index_name="vector_index1")
    # filters = {"file_name":"wildfire.pdf","space":space}
    # docsearch = vector_search.similarity_search(query,search_kwargs = {
    #     "k": 1,
    #     "score_threshold": 0.85,
    #     "pre_filter" : {"spacename":spacename}
    #     })
    # print(docsearch)
    # vector_search.similarity_search_with_score
    retrievers_answer = []
    retrievers_for_filecheck = []
    for space in spacename:
        retriever_answer = vector_search.as_retriever(
            search_type = "similarity",
            search_kwargs = {
                "k": 25,
                "score_threshold": 0.75,
                "pre_filter" : {"spacename":space}
                })
        
        retrievers_answer.append(retriever_answer)
        
        # print(retriever_answer)



        retriever_for_filecheck = vector_search.as_retriever(
            search_type = "similarity",
            search_kwargs = {
                "k": 5,
                "score_threshold": 1,
                "pre_filter" : {"spacename":space},
                "post_filter":{"$sort":{"score":+1}}
                })
        retrievers_for_filecheck.append(retriever_for_filecheck)
    combined_retrievers_answer = MergerRetriever(retrievers=retrievers_answer)
    combined_retrievers_for_filecheck = MergerRetriever(retrievers=retrievers_for_filecheck)

    # retriever_for_filecheck = vector_search.as_retriever(
    #     search_type = "similarity",
    #     search_kwargs = {
    #         "k": 1,
    #         "score_threshold": 1,
    #         "pre_filter" : {"spacename":spacename}
    #         })
    # print(retriever)
    

    # vector_search.as_retriever()
    # docs = vector_search.similarity_search(query, K=3)
    # print(docs)
    
    # def custom_retrieval_chain(query, retriever, combine_docs_chain):
    # # Retrieve documents and sort by similarity score
    #     results = retriever.similarity_search(query, k=3)
    #     sorted_results = sorted(results, key=lambda x: retriever.score(query, x), reverse=True)

    #     # Pass the sorted documents to the combine_docs_chain
    #     output = combine_docs_chain.run(input_documents=sorted_results, question=query)
    #     return output
    # # vector_search.similarity_search_with_score
    # retrieve

    # def custom_retrieval_chain(query, retriever, combine_docs_chain):
    # # Retrieve documents and sort by similarity score
    #     results = retriever.aaa
    #     results = retriever.similarity_search_with_score(query)
    #     sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    #     # Extract only the documents (without scores)
    #     sorted_docs = [doc for doc, score in sorted_results]

    #     # Pass the sorted documents to the combine_docs_chain
    #     output = combine_docs_chain.run(input_documents=sorted_docs, question=query)
    #     return output





    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(model,retrieval_qa_chat_prompt)
    # retrieval_chain1 = create_retrieval_chain(retriever_answer,combine_docs_chain)
    retrieval_chain1 = create_retrieval_chain(combined_retrievers_answer,combine_docs_chain)
    # print(retrieval_chain1)
    # retrieval_chain2 = create_retrieval_chain(retriever_for_filecheck,combine_docs_chain)
    retrieval_chain2 = create_retrieval_chain(combined_retrievers_for_filecheck,combine_docs_chain)

    # prompt = """analyse the question.if it is a greeting type question make answers for the greeting.if it is not a greeting type question and context is not there give answer as "you are not allowed to access the database or the data is not in the database".Else give the answers only from the context with out fabricating anything other than from context"""


    # prompt = """You're an expert in crafting responses solely from the question and context. 
    #             For greeting type questions make answers accordingly.
    #             For question "who are you" respond as "I am an expert in making answers for the questions from companies documents."
    #             For question "Can you help me" respond as "Yes,I can help you,please ask the question".
    #             For question is non greeting type and context is empty respond as "You are not allowed to access this data or the data is not available in the database".
    #             Give answers only from the context don't fabricate anything other than the context.understand above guidelines and follow it strictly for the following question, """

    prompt= """You excel in providing responses based solely on questions and context. Here are the guidelines to follow:
                    - For greeting-type questions, craft appropriate responses.
                    - When asked "who are you," reply with "I am an expert in crafting responses based on company documents."
                    - If asked "Can you help me," answer with "Yes, I can assist you. Please ask your question."
                    - For non-greeting questions with an empty context, respond with "You are not permitted to access this data, or the data is unavailable in the database."
                Give answers only from the context; don't fabricate anything other than what's provided. Understand the above guidelines and follow them strictly for the following question.
            """
    


    #     a) Greeting type examples: 'hi,' 'hai,' 'Hello,' 'Can you help me,' etc.
    #     b) Non-greeting type example: 'What is SQL.'

    #     If the question is a greeting type, respond accordingly to the greeting.
    #     Example: 'Hello, how can I help you?'

    #     If the question is non-greeting type check if context available :
    #         1:if context available:
    #         make answers only from the given context,avoid speculation and fabricating things.
    #         2:if context available:
    #         give answer as "You are not allowed to access the data or the data is not in the database".
    
    # give only the answer after having all the above steps.
        
    #     """
    # prompt = """You are an expert in making answers .Follow the guidelines properly before making answers.

    #     Categorize the question as either greeting type or non-greeting type:
    #     a) Greeting type examples: 'hi,' 'hai,' 'Hello,' 'Can you help me,' etc.
    #     b) Non-greeting type example: 'What is SQL.'
    #     If the question is a greeting type, respond accordingly to the greeting.
    #     Example: 'Hello, how can I help you?'
    #     If the question is non-greeting type:
    #     a) Check if context is an empty list:
    #     i) If no context is available, respond with answer "You don't have access, or the context is not available in the database."
    #     ii) If context is present, provide answers solely from the given context. Avoid fabricating information.
        
    #     """
    # prompt = """You are an expert in making answers from the context.if there is no context available,and question is not a greeting type,make answer as "you don't have the access to the data or it is not available in the database"."""
    # prompt = """You're skilled at generating answers based only on context. If no context is available and the question isn't a greeting type, answer is 'You don't have access to the data, or it's not available in the database.'"""
    output = retrieval_chain2.invoke({"input":query})

    # print(output['context'])
    file_name = ""
    try:

        ##############################################
        l = len(output['context'])
        list1 = []
        for i in range(l):
            print(output['context'][i].metadata['filename'])
            list1.append((output['context'][i].metadata['filename']).lower())
        # print(list1)
        for i in range(len(list1)):
            if list1[i] in query.lower():
                file_name = list1[i]
                document_id = output['context'][i].metadata['documentid']
                break
            else:
                file_name = output['context'][0].metadata['filename']
                document_id = output['context'][0].metadata['documentid']

        #################################################
        
        # print(file_name)
        # print(document_id)
    except:
        pass
    if file_name.endswith('.csv') and output['context'] != []:
        # elif '.' in filename and filename.rsplit('.', 1)[1].lower() in "csv":
        # print(file_name.rsplit('.', 1)[1])
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        #     retrieve_csv_file_from_mongodb(doc_id,file_path)
        response = csv_answer(query,document_id)
        return response
            
    else:
        output1 = retrieval_chain1.invoke({"input": prompt + query })
        print(len(output1['context']))
        answer = HTMLFormatter(output1["answer"])
        return answer


    # Assuming output is your dictionary

# Check if 'filename' key exists in the dictionary
    # print(type(output['context']))

        
    # if 'filename' in output['context']:
    #     # Check if the value of 'filename' ends with '.csv'
    #     if output['filename'].endswith('.csv'):
    #         print("The filename ends with '.csv'.")
    #     else:
    #         print("The filename does not end with '.csv'.")
    # else:
    #     print("The 'filename' key does not exist in the dictionary.")

    # print(output)
    # # print(retriever)
    # # if output["context"] == []:
    # #     return "you are not allowed to access this data or the context not in database"
    
    # # else:
    
    




if __name__ == '__main__':

    # Create the upload folder if it doesn't exist
    answer = qa(" issues for congress","datascience")
    print(answer)
    
