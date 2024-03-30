# pip install steamlit

import streamlit as st
import numpy as np
from timeit import default_timer as timer
from langchain.graphs


def query_graph (user_input):
    pass




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
