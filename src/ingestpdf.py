from langchain_community.document_loaders import TextLoader
from common_utils.logging_utils import setup_logger
from db_utils.mongo_oprationsqa import save_to_db
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common_utils.Config import Config
import fitz
import PIL.Image as Image
import io
import os

#SQL = SQL()
logger = setup_logger()


def save_image(block, page_num, base_path):
    """Saves the image from the block and returns the file path."""
    try:
        image_filename = f"image_page{page_num+1}_{block['number']}.{block['ext']}"
        image_folder = os.path.join(base_path, image_filename)
        image = Image.open(io.BytesIO(block["image"]))
        image.save(image_folder)
        logger.info("Extracted images from pdf "+ image_folder)
        return image_folder
    except Exception as e:
        exception_type = type(e).__name__
        exception_description = str(e)
        logger.error("Error extracting images: "+ str(exception_type) + str(exception_description) )


def process_text_block(block, page_num, line_number):
    """Processes a text block and returns formatted text."""
    text_content = []
    for line in block["lines"]:
        line_text = " ".join([span["text"] for span in line["spans"]])
        if line_text.strip():
            text_content.append((line_text.strip(), line_number, page_num + 1, block["bbox"]))
            line_number += 1
    return text_content, line_number



def extract_data_from_pdf(pdf_path, image_save_path):
    """Extracts text and images from a PDF, returning structured data."""
    extracted_data = []
    try:
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks = page.get_text("dict")["blocks"]
            line_number = 1
            for block in blocks:
                if block["type"] == 0:  # Text block
                    # Process text block
                    text_content = block["lines"]
                    extracted_data.extend(text_content)

                elif block["type"] == 1:  # Image block
                    # Save image and add its path to extracted data
                    image_path = f"{image_save_path}/page_{page_num + 1}_image.png"  # Example image path
                    extracted_data.append(("image", image_path))

        doc.close()
        print("Extracted data from PDF successfully.")
        return extracted_data

    except Exception as exe:
        print(f"Error extracting data from PDF: {exe}")
        return None


# def extract_data_from_pdf(pdf_path, image_save_path):
#     """Extracts text and images from a PDF, returning structured data."""
#     try:
#         doc = fitz.open(pdf_path)
#         extracted_data = []

#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             blocks = page.get_text("dict")["blocks"]
#             line_number = 1
#             for block in blocks:
#                 if block["type"] == 0:  # Text block
#                     text_content, line_number = process_text_block(block, page_num, line_number)
#                     extracted_data.extend(text_content)

#                 elif block["type"] == 1:  # Image block
#                     image_path = save_image(block, page_num, image_save_path)
#                     extracted_data.append(("<img>" + image_path + "</img>", None, page_num + 1, block["bbox"]))

#         doc.close()
#         logger.info("Extracted data from pdf")
#         return extracted_data

#     except Exception as exe:
#         exception_type = type(exe).__name__
#         exception_description = str(exe)
#         logger.error("Error extracting images: " )
#         logger.error("Error extracting data from pdf: "+ str(exception_type) + str(exception_description) )


def process_extracted_data(data):
    """Processes extracted data for final output."""
    # Sort by page number and bbox upper left corner
    data.sort(key=lambda x: (x[2], x[3][1], x[3][0]))
    return [item[0] for item in data ], [{ "page": item[2], "line_number": item[1]} for item in data]



import datetime

def pdf_2_txt(document):
     
     try:
        text = "\n".join(document)  # Concatenate lines of the document with newline characters
        with open("1.txt", 'w', encoding="utf-8") as text_file:
            text_file.write(text)
        print("Converted pdf to text")
     except Exception as exe:

        print("Error converting pdf to text: " + str(exe))

def process_text_file(metadata,text_file_name="1.txt"):
    # using text loader to load text file
    try:
        loader = TextLoader(text_file_name, encoding='utf8')
        documents = loader.load()
        # print(documents)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(metadata)
        metadata["spacename"].append("Super Admin")
        print(metadata)
        for text in texts:
            text.metadata =metadata
        # delete_from_chromadb()
        # save_to_db(texts)
        # delete_from_mongodb()

        # print(texts)
        save_to_db(texts)
        
        
        logger.info("Extracted text from pdf")
    except Exception as exe:
        logger.error("Error using textloader to read text file: "+ str(exe))



def main(pdf_path,metadata):
    print(pdf_path,metadata)
    extracted_data = extract_data_from_pdf(pdf_path, Config.chat_pdf_image_path)
    document, metadata1 = process_extracted_data(extracted_data)
    # print(document)
    
    metadata = metadata
    file_name = os.path.basename(pdf_path)
    pdf_2_txt(document)
    process_text_file(metadata)
    os.remove("1.txt")
    # os.remove(pdf_path)



def ingest_main1(file_path,metadata):
    try:
        loader = PDFPlumberLoader(file_path)
        documents = loader.load()
        

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        metadata["spacename"].append("Super Admin")
        # print(metadata)
        for text in texts:
            text.metadata =metadata

        save_to_db(texts)
        #removing pdf files
        # os.remove(file_path)
    except Exception as exe:
        print("an error occured "+ str(exe))
    # os.remove(file_path)


if __name__ == "__main__":
    pdf_path = "/home/chaitanya/Downloads/SQL-Server-2019-Installation-Guide.pdf"
    user = "superadmin"
    main(pdf_path, user)

