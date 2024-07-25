import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import warnings
import logging
from dotenv import load_dotenv

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN") # type: ignore

repo_id = "google/gemma-2b"

llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=256, top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03)

print("\u001b[1;32mLoaded LLM model successfully!\u001b[0m")

template = "You are a teacher's assistant at a university. You have been asked to make a new assignment for the students, which the teacher will give out. The assignment has to be a set of tasks. The assignment should be about the following topics: {keywords}. Write the assignment in a way that is clear and easy to understand for the students. Do not exceed 8 sentences."

prompt = PromptTemplate.from_template(template)

chain = prompt | llm