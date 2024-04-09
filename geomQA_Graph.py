# pip install streamlit
# pip install --upgrade --quiet  langchain langchain-community langchain-openai neo4j
# pip install python-dotenv
# new virtual environment, see https://stackoverflow.com/questions/54106071/how-can-i-set-up-a-virtual-environment-for-python-in-visual-studio-code
# after installation, activate the environment
# the code has been adapted from https://github.com/JohannesJolkkonen/funktio-ai-samples/blob/main/knowledge-graph-demo/main.py


import dotenv
import os

import streamlit as st
from timeit import default_timer as timer
from streamlit_chat import message

from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph

# load and initialize environment variables
dotenv.load_dotenv()  # take environment variables from .env.

openai_api_key = os.getenv("OPENAI_KEY")
neo4j_connection_url = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# create access to the neo4j graph
graph = Neo4jGraph(url=neo4j_connection_url, username=neo4j_username, password=neo4j_password)

# function to query the neo4j knowledge graph
def query_graph (user_input):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, return_intermediate_steps=True)
    response = chain.invoke({"query": user_input})
    return response

# frontend layout
st.set_page_config(layout="wide")
title_col, empty_col, img_col = st.columns([3, 1, 2])    

with title_col:
    st.title("Question Answering Assistant (Graph)")
with img_col:
    st.image("https://www.uni-muenster.de/imperia/md/images/geoinformatics/_v/2021-logo-ifgi-text-de.png", width=200)

# Initialize chat history
if "user_msgs" not in st.session_state:
    st.session_state.user_msgs = []

if "system_msgs" not in st.session_state:
    st.session_state.system_msgs = []


message("Hello, I am a chatbot. Please ask your question...") 

# React to user input
user_input = st.chat_input("Ask your question")
if user_input:
    with st.spinner("Processing your input..."):
        # Add user message to chat history
        st.session_state.user_msgs.append(user_input)

        start = timer()
        result = query_graph(user_input)

        intermediate_steps = result['intermediate_steps']
        cypher_query = intermediate_steps[0]['query']
        database_results = intermediate_steps[1]['context']
        answer = result['result']
        answer_modified = answer + (f" \n Time taken: {timer() - start:.2f}s")
        # Add system (final) answer to chat history
        st.session_state.system_msgs.append(answer_modified)
        #st.write(f"Time taken: {timer() - start:.2f}s")

    col1, col2, col3 = st.columns([2, 1, 1])

    # Display the chat history
    with col1:
        if st.session_state["system_msgs"]:
            for i in range(len(st.session_state["system_msgs"])):
                message(st.session_state["user_msgs"][i], is_user=True, key=str(i) + "_user")
                message(st.session_state["system_msgs"][i], key = str(i) + "_assistant")

    with col2:
        if cypher_query:
            st.text_area("Last Cypher Query", cypher_query, key="_cypher", height=240)
        
    with col3:
        if database_results:
            st.text_area("Last Database Results", database_results, key="_database", height=240)


# todo (add a cypher_prompt_template and a qa_prompt_template to the GraphCypherQAChain to impove cypher queries and customize outputs)