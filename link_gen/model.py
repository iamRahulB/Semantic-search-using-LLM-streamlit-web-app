from langchain_google_genai import ChatGoogleGenerativeAI
import os
import langchain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain.chains import LLMChain
 
from datetime import datetime


generation_config = genai.types.GenerationConfig(
    temperature=0.9,
    top_p=1,
    top_k=1,
    max_output_tokens=4000,
)




class MyModel:

  def __init__(self):
    
    pass



  def user_inputs(self,user_input):
      # Create embeddings for the user question using a Google Generative AI model
      embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

      # Load a FAISS vector database from a local file
      new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)

      print(new_db)

      # Perform similarity search in the vector database based on the user question
      docs = new_db.similarity_search(user_input,k=1, fetch_k=4)

      return docs
  
  
  def chat_history(self,df,user_input):     
    # Create embeddings using a Google Generative AI model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create a vector store using FAISS from the provided text chunks and embeddings
    vector_store = FAISS.from_texts(df.history, embedding=embeddings)

    # Save the vector store locally with the name "faiss_index"
    vector_store.save_local("faiss_index")

    serached_result=self.user_inputs(user_input)[0].page_content

    print(serached_result)

    print(df)

    return serached_result

  
  

  def run_gemini(self, user_input):

    INSTRUCTION = f"""
    As a helpful chatbot called "Rahul" made by "Rahul Bhole", your task is to respond to user queries. Below is the user input enclosed within triple backticks:

    User's Query: ```{user_input}```

    1. user might ask about chat history, say i dont have memory./
    2. if the user dont mention perticular topic in query then he refers to previous conversation, but you dont have memory.
    3. if the user's question is invalid or incomplete then handle this in response
    by understanding the intent of the user's query, decide if you can answer this or not. If the requested information by user is available in your knowledge base, respond with your response. 
    
    
    for the general questions that u can answer, provide a relevant response instead of "not found".\
    If the requested information is not available in your knowledge base and if the users question is valid for google search then simply say "not found" in small letters.\
    when responding with "not found" ensure it is appropriate google query. for the queries that can be searched on google, repond with the "not found".\
    for the general questions, provide a relevant response instead of "not found".

    note: the reason behind "not found" is to send you the information related to user's query in next api request from google.
"""


    genai.configure(api_key=os.environ['GEMINI_API'])

    model_gem = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config)

    response = model_gem.generate_content(INSTRUCTION)

    final = {"answer": response.text}
    
    return response
  



  def query_maker(self,user_input):

    if "HISTORY" not in st.session_state:
      st.session_state.HISTORY = []


    if "HISTORY" not in st.session_state.HISTORY:
      user_input_semantic_search="This is first time running this tool"


    current_time = datetime.now()

    full_date = current_time.strftime("%Y-%m-%d")

    
    llm=ChatGoogleGenerativeAI(model="gemini-1.0-pro",temperature=0.9,max_output_tokens=4096)  
  
    prompt=PromptTemplate(
    input_variables=["user_input","full_date","user_input_semantic_search"],
    template=template2  )

    chain=LLMChain(llm=llm,prompt=prompt)
    
    response=chain.predict(user_input=user_input,full_date=full_date,user_input_semantic_search=user_input_semantic_search)



    st.session_state.HISTORY.append({"history":f"user input : {user_input} \n AI Response {response}"})

    

    df=pd.DataFrame(st.session_state.HISTORY)

    user_input_semantic_search=self.chat_history(df,user_input)

    # print(user_input_semantic_search)

    

    final = {"answer": response}
    
    return final

  

