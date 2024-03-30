# pip install steamlit
# pip install --upgrade --quiet  langchain langchain-community langchain-openai neo4j

import streamlit as st
import os
from timeit import default_timer as timer
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph

# initialize environment variables
openai_api_key = os.getenv("OPENAI_KEY")
neo4j_connection_url = os.getenv("NEO4J_CONNECTION_URL")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# create access to the neo4j graph
graph = Neo4jGraph(url=neo4j_connection_url, username=neo4j_username, password=neo4j_password)

# function to query the neo4j knowledge graph
def query_graph (user_input):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
    response = chain.invoke({"query": user_input})
    return response

# frontend application using streamlit
st.set_page_config(layout="wide")
title_col, empty_col, img_col = st.columns([2, 1, 2])    

with title_col:
    st.title("Question Answering Assistant")
with img_col:
    st.image("https://www.uni-muenster.de/imperia/md/images/geoinformatics/_v/2021-logo-ifgi-text-de.png", width=200)

with st.chat_message("user"):
     st.write("Hello 👋")
     
user_input = st.chat_input("Ask your question")
if user_input:
    st.write(f"User has sent the following question: {user_input}")
    start = timer()
    result = query_graph(user_input)
