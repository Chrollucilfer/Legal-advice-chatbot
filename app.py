from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone as PineconeV
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

class PromptTemplate:
    def __init__(self, template: str, input_variables: List[str]):
        self.template = template
        self.input_variables = input_variables

    def format(self, **kwargs):
        return self.template.format(**kwargs)

class RetrievalQAChain:
    def __init__(self, pinecone_api_key: str, index_name: str, model_path: str, model_type: str, prompt_template: PromptTemplate):
        self.pc = pinecone.Pinecone(api_key=pinecone_api_key)
        self.index = self.pc.Index(index_name)
        self.llm = CTransformers(
            model=model_path,
            model_type=model_type,
            config={'max_new_tokens': 512, 'temperature': 0.8}
        )
        self.prompt_template = prompt_template
        self.embedding_model = download_hugging_face_embeddings()

    def perform_semantic_search(self, query: str, top_k: int = 2):
        query_embedding = self.embedding_model.embed_query(query)
        result = self.index.query(
            vector=query_embedding,
            namespace="real",
            top_k=top_k,
            include_values=True,
            include_metadata=True
        )
        return result['matches']

    def generate_prompt(self, context: str, question: str):
        return self.prompt_template.format(context=context, question=question)

    def retrieve_answers(self, query: str, top_k: int = 2):
        search_results = self.perform_semantic_search(query, top_k)
        answers = []
        source_documents = []
        for match in search_results:
            context = match['metadata'].get('text', '')
            prompt = self.generate_prompt(context, query)
            answer = self.llm(prompt)
            answers.append(answer)
            source_documents.append({
                'id': match['id'],
                'score': match['score'],
                'context': context
            })
        return {
            'result': answers[0] if answers else "I don't know.",
            'source_documents': source_documents
        }

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
qa_chain = RetrievalQAChain(
    pinecone_api_key="your_pinecone_api_key",
    index_name="legal-chatbot",
    model_path="model/gemini_model.bin",
    model_type="gemini",
    prompt_template=PROMPT
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    result = qa_chain.retrieve_answers(msg)
    return str(result["result"])

if __name__ == '__main__':
    app.run(debug=True)
