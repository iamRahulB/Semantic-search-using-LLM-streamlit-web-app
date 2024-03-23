from langchain.vectorstores import ElasticVectorSearch,ElasticsearchStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from link_gen.remove_stopwords import StopWordsRemoval
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
 


class Elastic:

    def __init__(self) -> None:
        pass
    def add_to_elasticsearch(self,user_input,response):
        embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        obj_remove_stopwords=StopWordsRemoval()

        cleaned_text=obj_remove_stopwords.stopwords_removal(response)

        

        splitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                                    chunk_overlap=20,
                                                    )

        splitted_text = splitter.split_text(str(cleaned_text))


        print("this is response splitted text ",splitted_text)
        

        user_id=st.session_state.user_id.lower()

    
            
        
        index_name=user_id

        db=ElasticsearchStore(
            es_cloud_id=os.environ.get("ES_CLOUD_ID"),
            es_api_key=os.environ.get("ES_API_KEY"),
            embedding=embeddings,
            index_name=index_name )
        
        splitted_text.insert(0, f"User Question: {user_input}")

        db.add_texts(texts=splitted_text)

        print("added to elastic search database::::::::::::::::::::::::::::\n",splitted_text,"\n")

        print("current user session ID ::::::::::::::::::::::::: ",user_id,"\n")


    def get_from_elasticsearch(self,user_input):

        embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        user_id=st.session_state.user_id.lower()

        index_name=user_id

        db=ElasticsearchStore(
            es_cloud_id=os.environ.get("ES_CLOUD_ID"),
            es_api_key=os.environ.get("ES_API_KEY"),
            embedding=embeddings,
            index_name=index_name
        )
        # filter semantic result by user id or session ids

    
        user_input_semantic_search=[]
        scores=[]

        try :
            docs=db.similarity_search_with_score(query=user_input,k=20)

            for i in docs:
                if i[1]>0.90:
                    user_input_semantic_search.append(i[0].page_content)
                scores.append(i[1])

            if len(user_input_semantic_search)==0:
                user_input_semantic_search=["Semantic history does not contain relevant information, so depend on chat history and knowledge base."]


        except:
            user_input_semantic_search=["Semantic history does not contain relevant information, so depend on chat history and knowledge base."]

        print("Generated scores of semantic search : ",scores)
        print("elastic semantic search result :::::::::::::::::::::::;: \n",user_input_semantic_search,"\n")

        print("current user session ID ::::::::::::::::::::::::: ",user_id,"\n")

        return user_input_semantic_search
