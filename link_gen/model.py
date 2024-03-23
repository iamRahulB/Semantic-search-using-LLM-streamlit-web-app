from langchain_google_genai import ChatGoogleGenerativeAI
import os
import langchain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.chains import LLMChain
import pandas as pd
from langchain_community.vectorstores import FAISS
import streamlit as st
from langchain_pinecone import PineconeVectorStore
import datetime
from link_gen.pinecone_index import PineConeIndex
from link_gen.templates import Templates
from link_gen.elastic_search import Elastic
from link_gen.recent_chat_history import RecentChat




history=[]

class MyModel:

  def __init__(self):
    pass

  

  def run_gemini(self, user_input):

    obj_recent_chat_history=RecentChat()
    num_messages_to_get=2    #2 means 3 
    last_conversastion=obj_recent_chat_history.recent_chat_history(num_messages_to_get)

    


    # mes=mes.reverse()
    # mes_last=mes[0:4]
    # new_mes=mes[:3]
    # print("laste 1 message---------------------------------------------------------------",new_mes)
    
    obj_elastic_search=Elastic()
    user_input_semantic_search=obj_elastic_search.get_from_elasticsearch(user_input)


    # obj_pinecone=PineConeIndex()  
    # user_input_semantic_search=obj_pinecone.get_from_pinecone(user_input)

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=1,max_output_tokens=40960,)  
 
    prompt=PromptTemplate(
    input_variables=["user_input","user_input_semantic_search","last_conversastion"],
    template=Templates.template )

    chain=LLMChain(llm=llm,prompt=prompt
                   )

   
    
    response=chain.predict(user_input=user_input,user_input_semantic_search=user_input_semantic_search,last_conversastion=last_conversastion)

    if "Not Available" in response or "Not available" in response or "not Available" in response or "not available" in response:
      pass
    
    else:
      # obj_pinecone.add_to_pinecone(user_input,response)
       
       obj_elastic_search.add_to_elasticsearch(user_input,response)

    return response
  


  def query_maker(self,user_input):

    current_time = datetime.datetime.now()

    obj_recent_chat=RecentChat
    
    last_conversation=obj_recent_chat.recent_chat_history(self,num_messages_to_get=1)

    print("query maker last chat \n\n ",last_conversation, '\n\n')

    full_date = current_time.strftime("%Y-%m-%d")

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=1,max_output_tokens=40960)  
  
    prompt=PromptTemplate(
    input_variables=["user_input","full_date","last_conversation"],
    template=Templates.template2  )

    chain=LLMChain(llm=llm,prompt=prompt)
    
    response=chain.predict(user_input=user_input,full_date=full_date,last_conversation=last_conversation)

    final = {"answer": response}
    
    return final

  
