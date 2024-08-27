![example event parameter](https://github.com/enugalamanideepreddy/ChatBot-Langchain-RAG/actions/workflows/workflow.yml/badge.svg?event=push)

# ChatBot-Langchain-RAG Application

## Working website 
Link : [Streamlit app](https://rag-chatbot-app.streamlit.app/)

## Overview
This project involves developing a versatile chatbot application with two main components: a general chatbot and a Retrieval-Augmented Generation (RAG) chatbot.

## General Chatbot
- **Functionality**: Handles a wide range of general queries, engages in conversation, and provides basic information using a pre-trained language model (e.g., GPT-3 or GPT-4).
- **Features**: 
  - Natural language understanding and generation
  - Maintains short conversation context
  - Answers generic questions

## RAG Chatbot
- **Functionality**: Enhances the general chatbot by retrieving relevant documents from a knowledge base to provide more accurate and detailed responses.
- **Features**: 
  - Retrieves specific information
  - Provides contextually accurate and detailed answers
  - Suitable for fact-based queries

## Workflow
1. **User Query**: User inputs a query.
2. **General Chatbot**: Provides a response for general queries.
3. **RAG Chatbot**: Activates for specific information needs, retrieves documents, and generates detailed responses.
4. **Response**: Delivers the response to the user.

This setup provides a robust and interactive chatbot capable of both general conversation and detailed information retrieval.

## How to Run
To run the Streamlit application, execute the following command in your command prompt:


```bash
cd direcytory_name
streamlit run main.py


