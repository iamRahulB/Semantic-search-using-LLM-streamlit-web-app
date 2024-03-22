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
from link_gen.elastic_search import Elastic
from link_gen.recent_chat_history import RecentChat





history=[]

class MyModel:

  def __init__(self):
    pass

  

  def run_gemini(self, user_input):

    obj_recent_chat_history=RecentChat()
    final_chat=obj_recent_chat_history.recent_chat_history()

    last_conversastion=final_chat[-2:]
    last_conversastion=list(reversed(last_conversastion))


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

    if "Perform Google Search" in response or "perform google search" in response or "Perform google search" in response:
      pass
    
    else:
      # obj_pinecone.add_to_pinecone(user_input,response)
       
       obj_elastic_search.add_to_elasticsearch(user_input,response)

    return response
  


  def query_maker(self,user_input):

    current_time = datetime.datetime.now()

    full_date = current_time.strftime("%Y-%m-%d")

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=0.9,max_output_tokens=40960)  
  
    prompt=PromptTemplate(
    input_variables=["user_input","full_date",],
    template=Templates.template2  )

    chain=LLMChain(llm=llm,prompt=prompt)
    
    response=chain.predict(user_input=user_input,full_date=full_date)

    final = {"answer": response}
    
    return final

  
