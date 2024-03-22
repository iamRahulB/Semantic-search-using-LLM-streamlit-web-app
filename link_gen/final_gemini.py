import os

import google.generativeai as genai

from link_gen.pinecone_index import PineConeIndex
from link_gen.elastic_search import Elastic





generation_config = genai.types.GenerationConfig(
    temperature=1,
    top_p=1,
    top_k=1,
    max_output_tokens=40960,
)

class FinalGemini:
    def __init__(self) -> None:
        pass

    def pass_to_gemini(self,user_input,semantic_search):

        INSTRUCTION=f"""
*User asked the following question inside tripple backticks:*
```
{user_input}
```
I have summarized the answer below:
summary: *{semantic_search}*

**Answer the question and provide a detailed explanation based on the summary provided.
Remember to use IPython Markdown formatting and include any relevant Python code.
Remember User does not know that summary is sent to you So pretend as you know all already.**
"""


        genai.configure(api_key=os.environ['GEMINI_API'])

        model_gem = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config, )

        response = model_gem.generate_content(INSTRUCTION).text



        # obj_pinecone=PineConeIndex()
        # obj_pinecone.add_to_pinecone(user_input,response)

        obj_elastic_search=Elastic()
        obj_elastic_search.add_to_elasticsearch(user_input,response)

        final = {"answer": response}

        return final
