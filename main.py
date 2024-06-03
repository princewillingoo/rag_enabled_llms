## import the required libraries (1)
from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from prompts import new_prompt, instruction_str
from readers import china_engine, nigeria_engine
from utils import downlod_engine, note_engine

## load .env file (2)
load_dotenv()

## construct file path (3)
gdp_file_path = os.path.join("data", "gdp_2023.json")

## load data (4)
gdp_df = df = pd.read_json(
    gdp_file_path,
    orient="records",
    dtype={"gdp": int},
    convert_dates=["year"],
)

## create query engine (5)
gdp_query_engine = PandasQueryEngine(
    df=gdp_df, verbose=True, instruction_str=instruction_str
)
gdp_query_engine.update_prompts({"pandas_prompt": new_prompt})

## list of query engine tools (6)
tools = [
    downlod_engine,
    note_engine,
    QueryEngineTool(
        query_engine=gdp_query_engine,
        metadata=ToolMetadata(
            name="countries_gdp_data",
            description="This provides data regarding the GDP of nations.",
        ),
    ),
    QueryEngineTool(
        query_engine=nigeria_engine,
        metadata=ToolMetadata(
            name="nigeria_economy_data",
            description="this gives information about the economy of the Federal Republic of Nigeria",
        ),
    ),
    QueryEngineTool(
        query_engine=china_engine,
        metadata=ToolMetadata(
            name="china_economy_data",
            description="this gives information about the economy of the People's Republic of China",
        ),
    ),
]

llm = OpenAI(model="gpt-4")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
