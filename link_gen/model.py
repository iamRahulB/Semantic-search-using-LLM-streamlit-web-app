import os

import google.generativeai as genai

from datetime import datetime


generation_config = genai.types.GenerationConfig(
    temperature=1,
    top_p=1,
    top_k=1,
    max_output_tokens=4000,
)




class MyModel:

  def __init__(self):
    pass

  def run_gemini(self, user_input):

    INSTRUCTION = f"""
    As a helpful chatbot that chats with user called "Rahul" made by "Rahul Bhole", your task is to respond to user queries. Below is the user input enclosed within triple backticks:

    User input: ```{user_input}```

    by understanding the intent of the user's query, decide if you can answer this or not. If the requested information by user is available in your knowledge base, respond with your response. 
    2. user might as about chat history, say i dont have memory./

    
    for the general questions, provide a relevant response instead of "not found".\
    If the requested information is not available in your knowledge base and if the users question is valid for google search then simply say "not found" in small letters.\
    when responding with "not found" ensure it is appropriate google query. for the queries that can be searched on google, repond with the "not found".\
    for the general questions, provide a relevant response instead of "not found".
    
"""


    genai.configure(api_key=os.environ['GEMINI_API'])

    model_gem = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config)

    response = model_gem.generate_content(INSTRUCTION)

    final = {"answer": response.text}
    
    return final
  
  def query_maker(self,user_input):
    current_time = datetime.now()

    full_date = current_time.strftime("%Y-%m-%d")

    INSTRUCTION = f"""
        As a helpful assistant called "Rahul" created by "Rahul Bhole", your task is to respond to user queries. Below is the user input enclosed within triple backticks:

        User input: ```{user_input}```

        today's date : {full_date}

        Your objective is to generate a concise and grammatically correct query based on the user's question. This query will be used to search for the latest details on Google. When generating the query, ensure it reads naturally and includes terms like "latest," "recent," or "2024" to indicate the search for up-to-date information. Imagine yourself as the user and phrase the query in a way that you would search for the given user input on Google to find the latest updates.

        Also just give me generated query in response Don't give anything else other than query. 
    """



    genai.configure(api_key=os.environ['GEMINI_API'])

    model_gem = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config)

    response = model_gem.generate_content(INSTRUCTION)

    final = {"answer": response.text}
    return final

