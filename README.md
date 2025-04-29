# FraudSleuth: An Intelligent Fraud Detection System

## Overview

FraudSleuth is a sophisticated fraud detection system that leverages the power of Google's Gemini LLM, LangChain, and LangGraph to identify and analyze potentially fraudulent activities. This system is designed to provide actionable insights and recommendations, empowering users to take swift and effective action.

## Key Features

- **AI-Powered Analysis:** Employs Gemini LLM for advanced reasoning and analysis of suspicious activities.
- **Orchestrated Reasoning:** Utilizes LangChain and LangGraph for structured and efficient orchestration of the detection process.
- **Vector Search:** Integrates ChromaDB for efficient retrieval of related fraud patterns and documents.
- **External Fraud Detection API:** Incorporates IPQualityScore for real-time risk assessment and fraud signal detection.
- **Evidence Synthesis:** Merges retrieved data and API responses to provide comprehensive evidence.
- **Actionable Insights:** Delivers fraud risk scores, explainability, and actionable recommendations.

## How It Works

FraudSleuth operates through a series of interconnected steps:

1.  **User Input:** The system receives an enquiry about a suspicious email ID or IP address.
2.  **Agent Core:** The core of the system, powered by Gemini LLM, LangChain, and LangGraph, orchestrates the reasoning process.
3.  **Tool Selection:** The system selects appropriate tools for analysis:
    - **Tool 1: Vector Search (ChromaDB):** Retrieves related fraud patterns and documents.
    - **Tool 2: External Fraud Detection API (IPQualityScore):** Provides real-time risk scores and fraud signals.
4.  **Data Retrieval & API Response:** The selected tools retrieve relevant data and provide responses.
5.  **Agentic Reasoning:** LangGraph merges the retrieved data and API responses, synthesizing the evidence.
6.  **Fraud Assessment:** The system assesses the fraud risk based on the synthesized evidence.
7.  **Response to User:** The system provides a detailed response to the user, including:
    - Fraud risk score
    - Explainability of the assessment
    - Actionable recommendations

## Architecture

![FraudSleuth Architecture](docs/ArchDiagram\_ MermaidChart.png)

## Tools Used

- [Gemini LLM](https://ai.google.com/gemini)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://python.langchain.com/docs/langgraph)
- [ChromaDB](https://www.trychroma.com/)
- [IPQualityScore](https://www.ipqualityscore.com/)

## Getting Started

### Prerequisites

- Python 3.x
- API keys for IPQualityScore

### Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/reema14a/fraudsleuth-gemini.git](https://github.com/reema14a/fraudsleuth-gemini.git)
    cd fraudsleuth-gemini
    ```

2.  Install dependencies from the repository:

    ```
    pip install -r requirements.txt
    ```

3.  Set up environment variables:

    - Create a `.env` file in the project root by copying the same from config folder.
    - Add your API keys for IPQualityScore and Gemini LLM to the `.env` file:

      ```
      GEMINI_API_KEY=YOUR_API_KEY
      FRAUD_API_KEY=YOUR_API_KEY
      ```

### Usage

Detailed usage instructions will be added.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements.

## Acknowledgements

- The FraudSleuth project is built upon the powerful tools and frameworks mentioned above.

## Further Information

For more details, please connect with me on [LinkedIn](https://www.linkedin.com/in/reema-raghava-pmp%C2%AE-28737a11/)
