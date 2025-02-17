import os

from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from hana_ml import ConnectionContext
from hana_ml.dataframe import create_dataframe_from_pandas
from langchain.prompts import PromptTemplate
import pandas as pd

# please enter the Credentials from your AI core landscape.
env_vars = {
        "AICORE_AUTH_URL": "",
        "AICORE_CLIENT_ID": "",
        "AICORE_CLIENT_SECRET": "",
        "AICORE_RESOURCE_GROUP": "",
        "AICORE_BASE_URL": ""
}

# Set the environment variables using `os.environ`.
for key, value in env_vars.items():
    os.environ[key] = value


import csv

data = []
with open('GRAPH_DOCU_2503.csv', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        try:
            data.append(row)
        except:
            print(row)

import hdbcli
from hdbcli import dbapi

cc = dbapi.connect(
    address='',
    port='',  # 443 is usual
    user='',
    password='',
    encrypt=True
    )


# # Create a table
# cursor = cc.cursor()
# sql_command = '''CREATE TABLE GRAPH_DOCU_2503(ID1 BIGINT, ID2 BIGINT, L1 NVARCHAR(3), L2 NVARCHAR(3), L3 NVARCHAR(3), FILENAME NVARCHAR(100), HEADER1 NVARCHAR(5000), HEADER2 NVARCHAR(5000), TEXT NCLOB, VECTOR_STR REAL_VECTOR);'''
# cursor.execute(sql_command)
# cursor.close()

# cursor = cc.cursor()
# sql_insert = 'INSERT INTO GRAPH_DOCU_2503(ID1, ID2, L1, L2, L3, FILENAME, HEADER1, HEADER2, TEXT, VECTOR_STR) VALUES (?,?,?,?,?,?,?,?,?,TO_REAL_VECTOR(?))'
# cursor.executemany(sql_insert,data[1:])

# Get embeddings
from gen_ai_hub.proxy.native.openai import embeddings

def get_embedding(input, model="text-embedding-ada-002") -> str:
    response = embeddings.create(
      model_name=model,
      input=input
    )
    return response.data[0].embedding

print("got Embedding")    


cursor = cc.cursor()
def run_vector_search(query: str, metric="COSINE_SIMILARITY", k=4):
    if metric == 'L2DISTANCE':
        sort = 'ASC'
    else:
        sort = 'DESC'
    query_vector = get_embedding(query)
    sql = '''SELECT TOP {k} "ID2", "TEXT"
        FROM "GRAPH_DOCU_2503"
        ORDER BY "{metric}"("VECTOR_STR", TO_REAL_VECTOR('{qv}')) {sort}'''.format(k=k, metric=metric, qv=query_vector, sort=sort)
    cursor.execute(sql)
    hdf = cursor.fetchall()
    return hdf[:k]    

promptTemplate_fstring = """
You are an SAP HANA Cloud expert.
You are provided multiple context items that are related to the prompt you have to answer.
Use the following pieces of context to answer the question at the end. 
Context:
{context}
Question:
{query}
"""
from langchain.prompts import PromptTemplate
promptTemplate = PromptTemplate.from_template(promptTemplate_fstring)

!pip install tiktoken
import tiktoken
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

def ask_llm(query: str, metric='COSINE_SIMILARITY', k = 4) -> str:
    context = ''
    context = run_vector_search(query, metric, k)
    prompt = promptTemplate.format(query=query, context=' '.join(str(context)))
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(str(prompt)))
    print('no of tokens'+ str(num_tokens))
    llm = ChatOpenAI(proxy_model_name='gpt-4-32k',max_tokens = 8000)
    response = llm.invoke(prompt).content
    print('Query: '+ query)
    print('\nResponse:')
    print(response)

# query = "I want to calculate a shortest path. How do I do that?"
# from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
# llm = ChatOpenAI(proxy_model_name='gpt-4-32k')
# response = llm.invoke(query).content
# response    

# query = "I want to calculate a shortest path. How do I do that?"
# response = ask_llm(query=query, k=4)
# response

# query = "Write an article on the new features in graphs."
# response = ask_llm(query=query, k=4)
# response

# query = "How can I find the shortest distance between two nodes? Give the output in Dutch."
# response = ask_llm(query=query, k=4)
# response

# query = "Graphs can be a useful tool for computer scientists when ..."
# response = ask_llm(query=query, k=4)
# response

# query = '''Classify the following questions into graph related and business related questions. 

#     1. How does diversification reduce investment risk?
#     2. Describe the role of dividends in stock investing.
#     3. What is the degree of a node in a graph, and how is it calculated?
#     4. What factors influence consumer behavior in marketing?
#     5. Explain the basic principles of the law of diminishing returns.
#     6. What is the concept of opportunity cost in economics?
#     7. What is the definition of a graph in graph theory?
#     8. How are directed and undirected graphs distinguished from each other?
#     9. Explain the difference between a path and a cycle in a graph.
#     10. What is a connected graph, and why is it significant in the study of graphs?'''
# response = ask_llm(query=query, k=4)
# response

# query = '''
#     The following conent is not fit for a professional document. Rewrite the same in a professional tone. 
        
#     I can't believe we're still dealing with this nonsense! If you dare to mess around with the referenced graph tables without ensuring the consistency of the graph workspace through referential constraints, you're practically asking for chaos! And let me tell you, when that happens, each blasted Graph Engine component behaves differently! It's like dealing with a bunch of unruly children who can't agree on a single thing!

#     Check out the CREATE GRAPH WORKSPACE Statement and the DROP GRAPH WORKSPACE Statement. Maybe if you bothered to read them properly, you wouldn't be stuck in this mess! But no, here we are, dealing with your incompetence and the fallout of your reckless actions. Get your act together and start taking responsibility for maintaining a freaking consistent graph workspace!'''
# response = ask_llm(query=query, k=4)
# response

# query = '''
#     Proofread and rewrite the following sentence:
#     The GraphScript langaguae  will eases the developomont of application-specific graph algthrihms and integrates them into SQL-based data procezzing.
#         '''
# response = ask_llm(query=query, k=4)
# response




