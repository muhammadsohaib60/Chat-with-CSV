import io
import os
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI


def talkToData(data: pd.DataFrame, text: str, key: str):
    # Set the OpenAI API key
    os.environ["OPENAI_API_KEY"] = key

    # Convert the decoded data to a pandas DataFrame
    df = data

    df.to_csv('data.csv')
    # Create a pandas dataframe agent
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        df,
        verbose=False,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    # Build the prompt
    prompt = (
        """
        If the query requires creating a table, reply as follows:
        {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}
        
        If the query is not asking for a chart but requires a response, reply as follows:
        {"answer": "answer"}
        Example:
        {"answer": "The product with the highest sales is 'Minions'."}
                
        Let's proceed step by step. Don't give code, only answers.

        Here is your query:
        """ + text
    )

    # Run the agent with the user's query
    response = agent.run(prompt)

    # If no valid code found, just print the response
    print(response)
    return response
