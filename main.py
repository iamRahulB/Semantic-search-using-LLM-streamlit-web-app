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

st.title("Rahul's Semantic Search LLM")

if "messages" not in st.session_state:
  st.session_state.messages = []

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

  answer = data["answer"]

  if answer == "not found":
    with st.chat_message("assistant"):
      with st.status("Getting content from web...") as status_bar:
        st.write("Getting webpages...")

        
    
    obj_link_gen = LinkGen(user_input)
    links = obj_link_gen.generate_links()

    obj_web_content = WebContent()

    all_links_body_text = obj_web_content.fetch_content(links)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=200)

    splitted_text = splitter.split_text(str(all_links_body_text))

    obj_embedding = Embedding()
    embeddings,model = obj_embedding.get_embedding(splitted_text)

    obj_faiss_search=FaissSearch()
    distances,indexes=obj_faiss_search.index_search(user_input,embeddings,model)
    semantic_search=[]
    for index in indexes[0]:
        semantic_search.append(splitted_text[index])
    
    obj_final_gemini=FinalGemini()

    response=obj_final_gemini.pass_to_gemini(user_input,semantic_search)

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


