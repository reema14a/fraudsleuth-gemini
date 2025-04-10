from google import genai
from config.config import GENAI_MODEL, GEMINI_API_KEY

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from tools.fraud_api import FraudChecker
from tools.vector_search import ChromaVectorSearch

import re

from google.api_core import retry


# Authenticate Gemini
client = genai.Client(api_key = GEMINI_API_KEY)

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

genai.models.Models.generate_content = retry.Retry(
    predicate=is_retriable)(genai.models.Models.generate_content)

# Prompt template to synthesize context and external API result
prompt_template = PromptTemplate(
    input_variables=["query", "retrieved_docs", "fraud_api_result"],
    template="""
        You are a fraud analysis assistant.

        User Query:
        {query}

        Retrieved Knowledge Context:
        {retrieved_docs}

        Fraud Check Result (if applicable):
        {fraud_api_result}

        Based on all of the above, provide a clear and actionable response to the user.
        """
        )

# Set up LangChain Gemini Chat model
llm = ChatGoogleGenerativeAI(model = GENAI_MODEL, temperature = 0.2, google_api_key = GEMINI_API_KEY)
llm_chain = prompt_template | llm

# Initialize tools
fraud_checker = FraudChecker()
vector_search = ChromaVectorSearch()

def extract_ip_or_email(query: str):
    """Basic regex utility to extract IPs or emails from a query."""
    ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', query)
    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', query)
    return ip_match.group(0) if ip_match else email_match.group(0) if email_match else None

def combined_tool(query: str) -> str:
    # 1. Get vector search results
    vector_results = vector_search.query(query)
    retrieved_docs = "\n".join(vector_results["documents"][0])

    # 2. If IP or email found, call fraud API
    suspicious_input = extract_ip_or_email(query)
    fraud_api_result = ""
    if suspicious_input:
        fraud_api_result = fraud_checker.check_ip(suspicious_input)
    else:
        fraud_api_result = "No IP or email detected in query."

    # 3. Run final prompt
    return llm_chain.invoke({
            "query": query,
            "retrieved_docs": retrieved_docs,
            "fraud_api_result": fraud_api_result
        })

# Define LangChain tools
# tools = [
#     Tool(
#         name = "Check IP Fraud",
#         func = lambda ip: check_ip_fraud(ip),
#         description = "Use this to check if an IP address is potentially fraudulent."
#     ),
#     Tool(
#         name = "Search Similar Fraud Cases",
#         func = lambda query: vector_search.query(query),
#         description = "Use this to find similar fraud cases from the knowledge base."
#     )
# ]

# Create unified tool
combined_fraud_tool = Tool(
    name="FraudKnowledgeAndCheckTool",
    func=combined_tool,
    description="Use this to handle any query involving fraud detection, signs of fraud, or suspicious IP/email lookup."
)

# Memory for conversation context
memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)

# Initialize the agent
fraud_agent = initialize_agent(
    tools = [combined_fraud_tool],
    llm = llm,
    agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory = memory,
    verbose = True
)


# Optional entry point
def run_fraud_agent(query: str):
    return fraud_agent.run(query)

if __name__ == "__main__":
    run_fraud_agent("What can you tell me about this IP: 198.51.100.23? Is it suspicious?")