import datetime
import streamlit as st

class RecentChat:

    def __init__(self) -> None:
        pass

    def recent_chat_history(self):
        conversation_data=[]

        for messages in st.session_state.messages:
            conversation_data.append(messages)

        user_content_list = []
        assistant_content_list = []

        for entry in conversation_data:
            if entry['role'] == 'user':
                user_content_list.append(entry['content'])
            elif entry['role'] == 'assistant':
                assistant_content_list.append(entry['content'])

        # Combine user and assistant content into a single list
        combined_content_list = [
            f"user_content: {user_content}, assistant_content: {assistant_content}"
            for user_content, assistant_content in zip(user_content_list, assistant_content_list) 
            ]

        
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        formatted_time=now.strftime("%Y-%m-%d %H:%M:%S")


        final_chat=[]
        for content in combined_content_list:
            final_chat.append(f"{formatted_time} :{content}")

        print("recent chat history ::::::::::::::::::::::: \n :::", final_chat,"\n")

        return final_chat
