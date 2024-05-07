import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
# from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import matplotlib.image as mpimg
# from langchain_openai import OpenAI
from langchain_community.llms import OpenAI
import base64



def ask_question(question):
    try:
        data = pd.read_csv("biostats.csv")
        #print(data.columns.tolist())
        agent = create_pandas_dataframe_agent(openai, data, verbose=True)
        
        prompt = "If you plot anything then save the plot to plot.png. "
        response = agent(question + prompt)
        print(response)
        if os.path.exists('plot.png'):
            img = mpimg.imread('plot.png')
            encim = base64.b64encode(img).decode('utf-8')
            os.remove('plot.png')
            return encim
        else:
            return response

    except Exception as e:
        return str(e)
    

question = "hello how are you"
ask_question(question)


