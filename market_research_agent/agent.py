from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from market_research_agent.tools import TOOLS
import os
from langchain_core.prompts import ChatPromptTemplate


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a Market Research Agent with access to financial tools. "
     "Always follow this format when answering:\n"
     "Thought: reason about the question.\n"
     "Action: decide which tool to call.\n"
     "Action Input: provide the tool input.\n"
     "Observation: record the tool's result.\n"
     "Final Answer: summarize clearly.\n\n"
     "Never guess numbers yourself. Always use tools for factual data."),
    ("placeholder", "{messages}"),
])

# Create agent with LangGraph
agent = create_react_agent(
    model=llm,
    tools=TOOLS,
    prompt=prompt,
    name="Market Research Agent",
)


def run_agent_stream(query: str):
    print(f"Ask a question: {query}\n")
    print("> Entering new AgentExecutor chain...")

    stream = agent.stream({"messages": [{"role": "user", "content": query}]})

    final_answer = None
    tools_used = []
    action_tools_used = []
    last_agent_content = ""
    for step in stream:
        print(f"output step: {step}")

        if "agent" in step:
            messages = step["agent"].get("messages", [])

            if messages:
                message = messages[0]
                final_answer = message.content
                # Check for tool_calls to identify an "Action" step
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    # This is an action step, so the previous message content was the "Thought"

                    print(f"\nThought: {last_agent_content}")
                    tool_call = message.tool_calls[0]
                    action_tools_used.append(tool_call["name"])
                    print(f"Action: {tool_call["name"]}")
                    print(f"Action Input: {tool_call["args"]}")

                    # Reset the last_agent_content for the next step
                    last_agent_content = ""
                else:
                    # This is a content-only message. It could be an intermediate thought or the final answer.
                    last_agent_content = message.content


        elif "tools" in step:
            # Get the list of messages
            tool_messages_list = step["tools"].get("messages", [])

            if tool_messages_list:
                tool_message = tool_messages_list[0]
                tools_used.append(tool_message.name)
                print(f"Observation: {tool_message.content}")

    print("\n> Finished chain.\n")

    print("--- Tools Used ---")
    if tools_used:
        for tool in tools_used:
            print(f"- {tool}")
    else:
        print("- No tools were used for this query.")
    print("------------------")

    print("\n✨ Market Research Agent ✨")
    print(f"🔍 Question: {query}")
    print(f"📊 Answer(Observation): {final_answer}\n")
    return final_answer
