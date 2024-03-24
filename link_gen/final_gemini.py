import os

import google.generativeai as genai

from link_gen.pinecone_index import PineConeIndex
from link_gen.elastic_search import Elastic
from link_gen.recent_chat_history import RecentChat





generation_config = genai.types.GenerationConfig(
    temperature=1,
    top_p=1,
    top_k=1,
    max_output_tokens=40960,
)

class FinalGemini:
    def __init__(self) -> None:
        pass

    def pass_to_gemini(self,user_input,semantic_search,links):
        
        obj_recent_chat=RecentChat
        recent_chat=obj_recent_chat.recent_chat_history(self,num_messages_to_get=1)

        
        print("here are links of the content :::::::::::::::::::::\n",links,"\n")

        INSTRUCTION=f"""
*User asked the following question inside tripple backticks:*
```
{user_input}
```
last chat between you and user: ---{recent_chat}---

summary of the user query: *{semantic_search}*

here is links from where summary is extracted : ---{links}---


i have provided the last chat between you and user, your task is to get context and topic from last chat\
based on context and topic you should answer the user query by using provided summary\

if the last chat is not relevant to user query then ignore it. 


**Answer the question and provide a detailed explanation based on the summary provided.
Remember to use Markdown formatting.
Remember User does not know that summary is sent to you So pretend you are providing info from your knowledge base.**
remember : don't reveal tha you are provided with information about user question, make user believe that u had all the info.
strict: always provide the links in response so user can go and check on the websites.

"""


        genai.configure(api_key=os.environ['GEMINI_API'])

        model_gem = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config, safety_settings=[
  {
    "category": "HARM_CATEGORY_DANGEROUS",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]
)

        response = model_gem.generate_content(INSTRUCTION).text


        # obj_pinecone=PineConeIndex()
        # obj_pinecone.add_to_pinecone(user_input,response)

        obj_elastic_search=Elastic()
        obj_elastic_search.add_to_elasticsearch(user_input,response,)

        final = {"answer": response}

        return final
