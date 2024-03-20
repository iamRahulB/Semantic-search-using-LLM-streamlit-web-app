from langchain_google_genai import ChatGoogleGenerativeAI
import os
import langchain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.chains import LLMChain
import pandas as pd
from langchain_community.vectorstores import FAISS
import streamlit as st
from langchain_pinecone import PineconeVectorStore
import datetime
from link_gen.pinecone_index import PineConeIndex
from link_gen.templates import Templates


history=[]

class MyModel:

  def __init__(self):
    pass

  

  def run_gemini(self, user_input):
    conversation_data=[]
    for messages in st.session_state.messages:
      conversation_data.append(messages)

    user_content_list = []
    assistant_content_list = []

    for entry in conversation_data:
        if entry['role'] == 'user':
            user_content_list.append(entry['content'])
        elif entry['role'] == 'assistant':
            assistant_content_list.append(entry['content'])

    # Combine user and assistant content into a single list
    combined_content_list = [
        f"user_content: {user_content}, assistant_content: {assistant_content}"
        for user_content, assistant_content in zip(user_content_list, assistant_content_list) 
        ]

    
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    formatted_time=now.strftime("%Y-%m-%d %H:%M:%S")


    final_chat=[]
    for content in combined_content_list:
        final_chat.append(f"{formatted_time} :{content}")

    last_conversastion=final_chat[-2:]
    last_conversastion=list(reversed(last_conversastion))

    print("last message to ai -----------", last_conversastion)

    # mes=mes.reverse()
    # mes_last=mes[0:4]
    # new_mes=mes[:3]
    # print("laste 1 message---------------------------------------------------------------",new_mes)

    obj_pinecone=PineConeIndex()  
    user_input_semantic_search=obj_pinecone.get_from_pinecone(user_input)

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=0.9,max_output_tokens=4096)  
 
    prompt=PromptTemplate(
    input_variables=["user_input","user_input_semantic_search","last_conversastion"],
    template=Templates.template )

    chain=LLMChain(llm=llm,prompt=prompt)

   
    
    response=chain.predict(user_input=user_input,user_input_semantic_search=user_input_semantic_search,last_conversastion=last_conversastion)

    if "Not Available" in response:
      pass
    
    else:
      obj_pinecone.add_to_pinecone(user_input,response)

    

    return response
  


  def query_maker(self,user_input):

    current_time = datetime.datetime.now()

    full_date = current_time.strftime("%Y-%m-%d")

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=0.9,max_output_tokens=4096)  
  
    prompt=PromptTemplate(
    input_variables=["user_input","full_date",],
    template=Templates.template2  )

    chain=LLMChain(llm=llm,prompt=prompt)
    
    response=chain.predict(user_input=user_input,full_date=full_date)

    final = {"answer": response}
    
    return final

  

