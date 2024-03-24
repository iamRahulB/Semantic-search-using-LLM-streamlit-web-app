import streamlit as st
from link_gen.fetch_links import LinkGen
import json
from link_gen.model import MyModel
from link_gen.get_web_content import WebContent
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from link_gen.embedding import Embedding
from link_gen.faiss_search import FaissSearch
from link_gen.final_gemini import FinalGemini
import datetime
from link_gen.generate_user_id import UserId
import time

def main():

  # Session assignment
  if "run_once" not in st.session_state:
      st.session_state.run_once = True
      
  # Initialize session variable
  obj_user_id=UserId()   

  st.title("Rahul's Semantic Search Querio AI ")

  if "messages" not in st.session_state and "user_id" not in st.session_state:
    st.session_state.messages = []
    st.session_state["user_id"]=obj_user_id.generate_user_id()
  st.write(f"current Session ID : {st.session_state.user_id}" )

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if user_input := st.chat_input("What is up?"):

    # Display user message in chat message container
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    my_model = MyModel()

    response = my_model.run_gemini(user_input)

    response_json = json.dumps(response)

    data = json.loads(response_json)

    knowledge_answer = response

    # print(st.session_state.messages)

    if "Not Available" in response or "Not available" in response or "not Available" in response or "not available" in response:
    
      new_query=my_model.query_maker(user_input) 
      new_query =new_query["answer"] 
      with st.chat_message("assistant"):
          st.write(f"Searching for: {new_query}")

      obj_link_gen = LinkGen(new_query)
      links = obj_link_gen.generate_links()

      obj_web_content = WebContent()
      
      with st.chat_message("assistant"):
        with st.status("Getting content from web...",expanded=True) as status:
          st.write("Getting webpages...")

          all_links_body_text = obj_web_content.fetch_content(links)
          splitter = RecursiveCharacterTextSplitter(chunk_size=300,
                                                    chunk_overlap=60)

          splitted_text = splitter.split_text(str(all_links_body_text))

          obj_embedding = Embedding()
          st.write("Getting Embeddings...")

          

          searched_result = obj_embedding.get_embedding(splitted_text,user_input)

          st.write("Getting results...")
          obj_final_gemini=FinalGemini()

          response=obj_final_gemini.pass_to_gemini(user_input,searched_result,links)
          status.update(label="Done", state="complete", expanded=False)


      response_json = json.dumps(response)

      data = json.loads(response_json)

      web_answer = data["answer"]

      
      final_answer_web=web_answer+str(f"\n\n\nSource : Web ")   #\n\n {links[0]}\n\n{links[1]}\n\n{links[2]}
      with st.chat_message("assistant"):
        
        def stream():
           for char in final_answer_web.split(" "):
              yield char + " "
              time.sleep(0.02)
        st.write_stream(stream)

      st.session_state.messages.append({
          "role": "assistant",
          "content": web_answer+str(f"\n\n\nSource : Web ")  #\n\n {links[0]}\n\n{links[1]}\n\n{links[2]}
      })
      

    else:
      final_answer_knowledge=knowledge_answer+str("\n\nSource : Querio AI")
      with st.chat_message("assistant"):
        def stream():
           for char in final_answer_knowledge.split(" "):
              yield char + " "
              time.sleep(0.02)
        st.write_stream(stream)

      st.session_state.messages.append({"role": "assistant", "content": knowledge_answer+str("\n\nSource : Querio AI")})


if __name__ == "__main__":
    main()    

