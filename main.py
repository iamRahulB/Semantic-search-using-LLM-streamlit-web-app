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

def main():

  # Session assignment
  if "run_once" not in st.session_state:
      st.session_state.run_once = True
      
      # Initialize session variables
      st.session_state.messages = []

  st.title("Rahul's Semantic Search LLM ")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  

# Get the current time in IST
  

# Print the formatted time


  if user_input := st.chat_input("What is up?"):

    # Display user message in chat message container
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    my_model = MyModel()

    response = my_model.run_gemini(user_input)

    response_json = json.dumps(response)

    data = json.loads(response_json)

    answer = response

    # print(st.session_state.messages)

    if "Not Available" in answer or "not Available" in answer:
    

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
                                                    chunk_overlap=200)

          splitted_text = splitter.split_text(str(all_links_body_text))

          obj_embedding = Embedding()
          st.write("Getting Embeddings...")

          searched_result = obj_embedding.get_embedding(splitted_text,user_input)

          st.write("Getting results...")
          obj_final_gemini=FinalGemini()

          response=obj_final_gemini.pass_to_gemini(user_input,searched_result)
          status.update(label="Done", state="complete", expanded=False)


      response_json = json.dumps(response)

      data = json.loads(response_json)

      answer = data["answer"]

      with st.chat_message("assistant"):
        st.markdown(answer+str(f"\n\n\nSource : Web \n\n {links[0]}\n\n{links[1]}\n\n{links[2]}"))

      st.session_state.messages.append({
          "role": "assistant",
          "content": answer+str(f"\n\n\nSource : Web \n\n {links[0]}\n\n{links[1]}\n\n{links[2]}")
      })
      

    else:
      with st.chat_message("assistant"):
        st.markdown(answer+str("\n\nSurce : Gemini"))

      st.session_state.messages.append({"role": "assistant", "content": answer+str("\n\nSurce : Gemini")})


if __name__ == "__main__":
    main()    

