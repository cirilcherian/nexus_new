import os
import base64
from common_utils.HTMLFormatterAI import HTMLFormatter

def get_image_paths():
    try:
        # Get the current working directory
        cwd = os.getcwd()
        
        # List all files in the current directory
        files = os.listdir(cwd)
        
        # Filter out the image files
        image_files = [file for file in files if file.endswith('.png')]
        
        if not image_files:
            print("No PNG image file found in the current directory.")
            return None
        
        # Return the list of image paths
        return [os.path.join(cwd, image) for image in image_files]
    except Exception as exe:
        print("an error occured "+str(exe))

def generate_html_output(text_output=None, image_paths=None):
    
    try:
    
        html_output = ""

        # If text output is provided, wrap it in <p> tags
        

        # If image paths are provided, encode image data and embed them in the HTML
        if image_paths:
            for image_path in image_paths:
                with open(image_path, "rb") as img_file:
                    # print(image_path)
                    filename = os.path.basename(image_path)
                    image_data = base64.b64encode(img_file.read()).decode("utf-8")
                # os.remove(image_path)
                html_output += f"<img src='data:image/png;base64,{image_data}' alt={filename}>"


                # Delete the image file
                os.remove(image_path)
                print(f"Image file '{image_path}' deleted successfully.")
        if text_output and image_paths==None:
            html_output += f"{text_output}"
            html_output = HTMLFormatter(html_output)

        return html_output
    except Exception as exe:
        print("an error occured "+str(exe))
if __name__ == '__main__':
# Example usage:
    text_output = "This is some text output."
    image_paths = get_image_paths()
    # print(image_paths)
    html_output = generate_html_output(text_output, image_paths)
    print(html_output)