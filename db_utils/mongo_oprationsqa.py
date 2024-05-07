#storing data in to mongo db
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from common_utils.Config import Config
from common_utils.embeddings import default_embeddings

embedding = default_embeddings()
client = MongoClient(Config.MONGODB_URI_CLUSTER)

db_name = "vector_db"
collection_name = "vector_collections"
collection = client[db_name][collection_name]


def save_to_db(texts):
    
    # print(texts[0])
    
    MongoDBAtlasVectorSearch.from_documents(documents = texts,embedding=embedding,collection = collection)

def delete_from_mongodb(doc_id):
    collection.delete_many({"documentid": doc_id})
# #     # collection.drop()



if __name__ == '__main__':

    delete_from_mongodb()
    # save_to_db()


