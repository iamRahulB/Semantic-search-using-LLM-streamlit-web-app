from langchain_community.vectorstores import FAISS
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import datetime


class PineConeIndex:

    def __init__(self) -> None:
        self.now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        self.formatted_time=self.now.strftime("%Y-%m-%d %H:%M:%S")


        



    def add_to_pinecone(self,user_input,response):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        index_name = "chathistory"
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

        response_formatted=[f"{self.formatted_time}  {user_input} - {response}"]

        vectorstore.add_texts(response_formatted)

        print("added to pinecone--------------------------response_formatted",response_formatted)


    
    def get_from_pinecone(self,user_input):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        index_name = "chathistory"

        docsearch_query = PineconeVectorStore.from_existing_index( index_name=index_name,embedding=embeddings,)

        docs = docsearch_query.max_marginal_relevance_search(user_input,k=2,fetch_k=20,)

        print("semantic docs------------------",docs)

        user_input_semantic_search=[]
        


        try :

            for i in docs:
                user_input_semantic_search.append(f"{self.formatted_time} :{i.page_content}")

            

        except:
            pass
        
            # except :
            #    docsearch_except = PineconeVectorStore.from_texts(texts=["this is first test message of pinecone. Ai dont include this in chat "], embedding=embeddings, index_name=index_name,ids=["rahulb"])
            #    docsearch_except = PineconeVectorStore.from_texts(texts=["this is first test message of pinecone. Ai dont include this in chat "], embedding=embeddings, index_name=index_name,ids=["rahulb"])
            #    docs_except = docsearch_query.similarity_search(user_input,k=1)
            #    user_input_semantic_search=[docs_except[0].page_content]
            # print("user input semantic search----------------------",user_input_semantic_search)

            # user_input_semantic_search=[docs[0].page_content,docs[1].page_content]
        
        print("got from pinecone")


        print("best of best------------------donnnn",user_input_semantic_search)
        return user_input_semantic_search
