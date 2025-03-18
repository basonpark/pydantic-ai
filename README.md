# Learning PydanticAI

This repo uses [PydanticAI](https://ai.pydantic.dev/) - a Python Agent Framework designed to make it easier to build production-grade applications with Generative AI.


## 🙏 Credits

This learning project is based on the excellent tutorial created by Dave Ebbelaar, founder of Datalumina®. The original tutorial provides comprehensive examples and explanations of PydanticAI's features and capabilities. 

If you're interested in learning more from Dave Ebbelaar, check out these resources:
- [Datalumina](https://www.datalumina.com/) - For AI and data solutions
- [Data Alchemy on Skool](https://www.skool.com/data-alchemy) - Free community for Python, AI and Data Science
- [Data Freelancer program](https://www.datalumina.com/data-freelancer) - For freelancing career development
- [GenAI Launchpad](https://launchpad.datalumina.com/) - For AI app development

## Introduction to PydanticAI

PydanticAI is a Python Agent Framework created by the team behind Pydantic, designed to streamline the development of production-grade applications with Generative AI. Building on the success and widespread adoption of Pydantic in the Python AI ecosystem, PydanticAI offers a type-safe, model-agnostic approach that seamlessly integrates with popular LLM providers like OpenAI, Gemini, and Groq. The framework emphasizes developer ergonomics by combining structured response validation, streamed responses, and a dependency injection system, all while allowing developers to leverage standard Python development practices for control flow and agent composition.

### Pydantic AI Core Concepts

1. [Agents](https://ai.pydantic.dev/agents/): The primary interface for interacting with LLMs, allowing you to define system prompts and manage interactions.
2. [Dependencies](https://ai.pydantic.dev/dependencies/): A type-safe system for injecting runtime context and accessing external services, making testing and integration easier.
3. [Results](https://ai.pydantic.dev/results/): Agents can return plain text, structured data, or streamed responses, all validated by Pydantic models.
4. [Messages and Chat History](https://ai.pydantic.dev/message-history/): Provides access to complete message history and tools for analyzing agent behavior and continuing conversations.
5. [Testing and Evals](https://ai.pydantic.dev/testing-evals/): Supports unit tests and evaluations to assess model performance and ensure application reliability.
6. [Debugging and Monitoring](https://ai.pydantic.dev/logfire/): Integrates with Pydantic Logfire for real-time debugging, performance monitoring, and querying of agent runs.

### Getting Started

To begin using PydanticAI, follow these steps:

1. **Python**: Ensure you have Python installed on your system. PydanticAI requires Python 3.9 or later.

2. **Install Requirements**: Navigate to the root directory of the repository and install the necessary dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**: Copy the provided `.env.example` file to a new file named `.env`. Open the `.env` file and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

    Make sure to replace `your_openai_api_key_here` with your actual OpenAI API key.

4. **Run the Introduction Script**: To get a feel for how PydanticAI works, execute the `introduction.py` script.

This script will guide you through the basic functionalities of PydanticAI, demonstrating how to interact with language models using the framework.

### Challenges I've Encountered

As I've been learning PydanticAI (which is still in early beta), I've noted some challenges:

- **Model Parameters**: Currently, I couldn't find a way to adjust model parameters like temperature.

- **Message History with Tools**: I've encountered a problem with message history when using tools. The following error occurs:

  ```
  BadRequestError: Error code: 400 - {'error': {'message': "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_KMMn5Bo6wPN3aZosdstleZO2", 'type': 'invalid_request_error', 'param': 'messages.[6].role', 'code': None}}
  ```
