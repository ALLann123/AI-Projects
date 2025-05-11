#!/usr/bin/python3
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
import os
from langchain.tools import tool

load_dotenv()


api_key = os.getenv("GITHUB_TOKEN")

# Create the LangChain chat model using the GitHub Marketplace endpoint
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)

@tool
def calculator(a: float, b:float) -> str:
    """Useful for performing basic arithmetic calculation with numbers"""
    print("\n[+]Calculator tool being called...")
    return f"The sum of {a} and {b} is {a+b}"

def say_hello(name:str) -> str:
    """Useful for greeting a user"""
    print("Tool has been called")
    return f"Hello {name}, I hope you are well today"

def main():
    model=llm

    tools=[calculator, say_hello]
    agent_executor=create_react_agent(model, tools)

    print("********************"*6)
    print("             BOtNET")
    print("********************"*6)
    print("\n Welcome! I'm your AI assistat. type 'quit' to exit")
    print("You can ask me to perform calculations or chat with me") 

    while True:
        user_input=input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("Bye!!")
            break

        print("\n Assistant: ", end="")
        #the agent will be typing one by word
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ): #check if response has agent and messages
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()


"""
 Welcome! I'm your AI assistat. type 'quit' to exit
You can ask me to perform calculations or chat with me

You: calculate the sum of 182 and 29343

 Assistant: 
[+]Calculator tool being called...
The sum of 182 and 29343 is 29525.

You: say hello to Alvin

 Assistant: Tool has been called
Hello Alvin, I hope you are well today!

You: 
"""