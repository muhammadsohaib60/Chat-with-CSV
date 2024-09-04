
import subprocess
import pandas as pd

import subprocess
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


# Function to determine the file format (CSV or Excel) based on the data URI
def get_file_format(data_uri: str) -> str:
    """
    Takes in a data_uri, and returns the file format

    Args:
        data_uri (str): data_uri to be processed

    Returns:
        file_format (str): file format
    """

    if "csv" in data_uri.lower():
        return "csv"
    elif "xlsx" in data_uri.lower():
        return "excel"
    else:
        raise ValueError("Unknown file format: Cannot determine if it's CSV or Excel.")


# Function to get Chain Of Thought
def get_chain_of_thought(response: str) -> str:
    """
    Takes in the agent response and prepares a chain of thought

    Make sure to initialize the agent like

    `create_csv_agent(..., return_intermediate_steps=True)`
    """
    cot_list = []

    # Get all the intermediate steps
    steps = response["intermediate_steps"]
    final_output = response["output"]

    for ind, s in enumerate(steps):
        action = s[0]
        action_output = s[1]

        # Skip the Langchain tool for Chain Of Thought
        log_list = action.log.replace("Action: python_repl_ast\n", "").split("\n")

        # Thought
        if not log_list[0].startswith("Thought:"):
            log_list[0] = "Thought:" + log_list[0]

        # Action
        log_list[1] = log_list[1].replace("Action Input", "Action")

        # Output
        action_output = "Output: " + (
            str(action_output) if action_output != "" else "No output"
        )

        log_list.append(action_output)
        cot_list.append("\n\t".join(log_list))

    # Construct string
    cot = ""
    for i, step in enumerate(cot_list):
        cot += f"Step {i + 1}:\n"
        cot += f"\t{step}\n"

    cot += f"\nFinal Output: {final_output}"

    return final_output


def chat(text: str, agent) -> str:
    """
    Takes in a text, get information results from agent, and returns the information results

    Args:
        text (str): text to be processed

    Returns:
        result (str): information results

    """

    result = agent({"input": text})
    
    try:
        chain_of_thought = get_chain_of_thought(result)
    except:
        chain_of_thought = result["output"]


    return chain_of_thought

def visualize(text: str, data, agent, ray) -> str:
    """
    Takes in a text, gets information results from the agent, agent creates a graph using plotly,
    and returns the graph HTML embedded

    Args:
        text (str): text to be processed
        agent (Agent): agent to be used for processing

    Returns:
        html_graph (str): HTML embedded graph
    """
    agent_globals = {
        "df": data,
        "go": go,
        "px": px,
        "fig": None,  # This is where the agent can store the resulting plotly figure
    }

    try:
        # Get the code from the agent
        code = agent(
            {
                "input": f"Give me the code to visualize {text} using plotly, store result in variable 'fig'"
            }
        )

        if isinstance(code, dict):
            code1 = code.get("output", None)

        # Run the code using exec with the specified global and local dictionaries
        exec(code1, agent_globals)

        # Assuming the code successfully created a plotly graph and assigned it to the 'fig' variable
        if "fig" in agent_globals and isinstance(agent_globals["fig"], go.Figure):
            # Convert the plotly graph to HTML
            fig = go.Figure(agent_globals["fig"])
            html_graph = pio.to_html(fig, full_html=False)
            return html_graph, get_chain_of_thought(code, ray)
        else:
            # If the agent's code didn't create a valid plotly graph, try again with the agent
            print("Error: The agent's code didn't create a valid plotly graph.")

    except:
        result = "I've got the result but could you give me better instructions to visualizing data.\n"
        result += chat(text, agent, ray)
        return None, result

def process(text: str, data, agent, ray) -> pd.DataFrame:
    """
    Takes in a text, gets code that will process the data information results from the agent,
    and returns the processed data

    Args:
        text (str): text to be processed
        data (pandas.DataFrame): data to be processed
        agent (Agent): agent to be used for processing

    Returns:
        processed_data (pandas.DataFrame): processed data
    """
    try:
        # Create a dictionary to pass data and any other required variables to the agent's code
        agent_globals = {"df": data, "processed_data": pd.DataFrame()}

        # while True:
        # Get the code from the agent
        agent_code = agent(
            {
                "input": f"Give me the code to process {text} and store the result in the variable 'processed_data'"
            }
        )

        if isinstance(agent_code, dict):
            code1 = agent_code.get("output", None)

        # Run the code using exec with the specified global and local dictionaries
        exec(code1, agent_globals)

        # exec(agent_code, agent_globals)
        processed_data = agent_globals.get("processed_data")

        if isinstance(processed_data, pd.DataFrame) and not processed_data.empty:
            return processed_data, get_chain_of_thought(agent_code, ray)
        else:
            # If the agent's code didn't return a valid DataFrame, try again with the agent
            print("Error: The agent's code didn't return a valid or non-empty DataFrame.")
    except:
        result = "I've got the result but could you give me better instructions to processing data.\n"
        result += chat(text, agent, ray)
        return data, result
        