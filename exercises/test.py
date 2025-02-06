import init_env
import variables

# init_env.set_environment_variables()
# # test whether the resource group is assigned correctly
# variables.RESOURCE_GROUP

# from gen_ai_hub.proxy.native.openai import chat

# messages = [
#     {   "role": "system", 
#         "content": "You are an SAP Consultant."
#     }, 
#     {
#         "role": "user", 
#         "content": "How does the data masking of the orchestration service work?"
#     }
# ]

# kwargs = dict(deployment_id=variables.LLM_DEPLOYMENT_ID, messages=messages)
# response = chat.completions.create(**kwargs)
# print(response.choices[0].message.content)



# import init_env
# import variables

# init_env.set_environment_variables()

# from gen_ai_hub.proxy.native.openai import embeddings

# def get_embedding(input_text):
#     response = embeddings.create(
#         input=input_text,            
#         model_name=variables.EMBEDDING_MODEL_NAME
#     )
#     embedding = response.data[0].embedding
#     return embedding

# apple_embedding = get_embedding("apple")
# orange_embedding = get_embedding("orange")
# phone_embedding = get_embedding("phone")
# dog_embedding = get_embedding("I love dogs")
# animals_embedding = get_embedding("I love animals")
# cat_embedding = get_embedding("I hate cats")

# print(apple_embedding)

# from scipy import spatial

# def get_cosine_similarity(vector_1, vector_2):
#     return 1 - spatial.distance.cosine(vector_1, vector_2)

# print("apple-orange")
# print(get_cosine_similarity(apple_embedding, orange_embedding))  



# init_env.set_environment_variables()

# # OpenAIEmbeddings to create text embeddings
# #from gen_ai_hub.proxy.native.openai import OpenAIEmbeddings
# from gen_ai_hub.proxy.langchain.openai import OpenAIEmbeddings

# # TextLoader to load documents
# from langchain_community.document_loaders import PyPDFDirectoryLoader

# # different TextSplitters to chunk documents into smaller text chunks
# from langchain_text_splitters import CharacterTextSplitter

# # LangChain & HANA Vector Engine
# from langchain_community.vectorstores.hanavector import HanaDB

# # connect to HANA instance
# connection = init_env.connect_to_hana_db()
# connection.isconnected()

# # Load custom documents
# loader = PyPDFDirectoryLoader('exercises/documents/')
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# texts = text_splitter.split_documents(documents)
# print(f"Number of document chunks: {len(texts)}")

# # Create embeddings for custom documents
# embeddings = OpenAIEmbeddings(deployment_id=variables.EMBEDDING_DEPLOYMENT_ID)
# db = HanaDB(
#     embedding=embeddings, connection=connection, table_name=variables.EMBEDDING_TABLE
# )

# # Delete already existing documents from the table
# db.delete(filter={})

# # add the loaded document chunks
# db.add_documents(texts)
# print(db.table_name)

# cursor = connection.cursor()

# # Use `db.table_name` instead of `variables.EMBEDDING_TABLE` because HANA driver sanitizes a table name by removing unaccepted characters
# embeddings = cursor.execute(f'SELECT VEC_TEXT, VEC_META, TO_NVARCHAR(VEC_VECTOR) FROM "{db.table_name}"')
# print(embeddings)
# for row in cursor:
#     print(row)
# cursor.close()


# init_env.set_environment_variables()

# from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
# from gen_ai_hub.proxy.langchain.openai import OpenAIEmbeddings

# from langchain.chains import RetrievalQA

# from langchain_community.vectorstores.hanavector import HanaDB

# # connect to HANA instance
# connection = init_env.connect_to_hana_db()
# connection.isconnected()

# # Create embeddings for custom documents
# embeddings = OpenAIEmbeddings(deployment_id=variables.EMBEDDING_DEPLOYMENT_ID)
# db = HanaDB(
#     embedding=embeddings, connection=connection, table_name=variables.EMBEDDING_TABLE
# )

# # Define which model to use
# chat_llm = ChatOpenAI(deployment_id=variables.LLM_DEPLOYMENT_ID)

# # Create a retriever instance of the vector store
# retriever = db.as_retriever(search_kwargs={"k": 2})

# # Create the QA instance to query llm based on custom documents
# qa = RetrievalQA.from_llm(llm=chat_llm, retriever=retriever, return_source_documents=True)

# # Send query
# query = "How does the data masking of the orchestration service work?"

# answer = qa.invoke(query)
# display(answer)

# for document in answer['source_documents']:
#     display(document.metadata)   
#     print(document.page_content)


import base64
import init_env
import variables

init_env.set_environment_variables()

from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

# with open("exercises/documents/ai-foundation-architecture.png", "rb") as image_file:
#     image_data = base64.b64encode(image_file.read()).decode('utf-8')

# message= {"role": "user", "content": [
#             {"type": "text", "text": "Describe the images as an alternative text"},
#             {"type": "image_url", "image_url": {
#                 "url": f"data:image/png;base64,{image_data}"}
#             }
#         ]}
    

# model = ChatOpenAI(deployment_id=variables.LLM_DEPLOYMENT_ID)

# response = model.invoke([message])
# print(response.content)


with open("exercises/documents/bananabread.png", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

message= {"role": "user", "content": [
            {"type": "text", "text": "Extract the ingredients and instructions in two different json files"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{image_data}"}
            }
        ]}
    

model = ChatOpenAI(deployment_id=variables.LLM_DEPLOYMENT_ID)

response = model.invoke([message])
print(response.content)







