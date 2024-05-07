import docx2txt
# from PIL import Image
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from db_utils.mongo_oprationsqa import save_to_db
# from langchain.docstore.document import Document
# from langchain_core.documents import Document
# from langchain_core.documents import Document

def extract_data_from_docx(docx_path, image_save_path):
    """Extracts text and images from a DOCX file, returning structured data."""
    try:
        extracted_data = []

        # Extract text
        text = docx2txt.process(docx_path)
        if text.strip():
            extracted_data.append(("text", text.strip()))

        # Extract images
        try:
            images = docx2txt.process(docx_path, image_dir=image_save_path)
            for i, image_path in enumerate(images.values()):
                extracted_data.append(("image", image_path))
        except:

            pass

        print("Extracted data from DOCX successfully.")
        return extracted_data

    except Exception as e:
        print(f"Error extracting data from DOCX: {e}")
        return 
def process_text_file(metadata,text_file_name="1.txt"):
# using text loader to load text file
    try:
        loader = TextLoader(text_file_name, encoding='utf8')
        documents = loader.load()
        # print(documents)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        # print(texts)
        # print(metadata)
        metadata["spacename"].append("Super Admin")
        print(metadata)
        for text in texts:
            text.metadata =metadata
        # delete_from_chromadb()
        # save_to_db(texts)
        # delete_from_mongodb()

        print(texts)
        save_to_db(texts)
    except Exception as exe:
        print("an error occured "+str(exe))


def main_docx(docx_path, metadata):
    image_save_path = "images"  # Path to save extracted images
    os.makedirs(image_save_path, exist_ok=True)

    extracted_data = extract_data_from_docx(docx_path, image_save_path)
    return extracted_data

def main(document_path,metadata):
    extracted_data = main_docx(document_path, metadata)
    # print(extracted_data)
    text_content = "".join([item[1] for item in extracted_data])
    print(type(text_content))
    with open("1.txt", "w", encoding="utf-8") as file:
        file.write(text_content)
    process_text_file(metadata)
    os.remove("1.txt")
    
    



    
    # Process extracted data here as needed

# Example usage:
if __name__ == "__main__":
    docx_path = "hello2.docx"
    filename = "hello2.docx"
    metadata = {
        "DocumentID": "14ad9de431de4715b6aeb0b6c565d464",
        "FileName": "gitahhhh.pdf",
        "spacename": ["jahjhsah"],
        "SpaceID": "ahsgsgahasiui",
        "UploadedBy": "jsahjhaaash",
        "UpdatedDate": "hsahhaaa"
        }
    extracted_data = main(docx_path, metadata)
    # print(extracted_data)
    # text_content = "".join([item[1] for item in extracted_data])

    # with open("1.txt", "w", encoding="utf-8") as file:
    #     file.write(text_content)
    # process_text_file(metadata,text_file_name="1.txt")


        

    # doc = Document(page_content=text_content, metadata=metadata)
    # # doc =  Document(page_content=text_content, metadata=metadata)
    # # print(type(text_content))
    # # print(extracted_data)
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # texts = text_splitter.split_documents(doc)
    # # print(texts)

    # document, metadata1 = process_extracted_data(extracted_data)
    # print(document)
    # print(doc)

    
