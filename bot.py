

from botbuilder.core import ActivityHandler, TurnContext
# import json  # To handle JSON data
# import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
# import _snowflake  # For interacting with Snowflake-specific APIs
# import pandas as pd
# import streamlit as st  # Streamlit library for building the web app
# from snowflake.snowpark.context import get_active_session  # To interact with Snowflake sessions
# from snowflake.snowpark.exceptions import SnowparkSQLException
# Removed invalid import: snowflake.cortex
import snowflake.connector
from snowflake.snowpark import Session  # For Snowpark session management
import requests
# import jwt
# import os
# import requests
# import datetime
# from cryptography.hazmat.primitives import serialization

# with open("rsa_key.pem", "rb") as key_file:
#         private_key = serialization.load_pem_private_key(
#             key_file.read(),
#             password=None,
#         )
conn = snowflake.connector.connect(
    user="GOHEALTH",
    password="Pass@987654312",
    account="WGTYAGV-MDB78147",
    # private_key=private_key,
    warehouse="COMPUTE_WH",
    database="CORTEX_ANALYST_DEMO",
    schema="REVENUE_TIMESERIES"
)


session = Session.builder.configs({
    "connection":conn
}).create()

def cortex(input_text):
    # List of available semantic model paths in the format: <DATABASE>.<SCHEMA>.<STAGE>/<FILE-NAME>
    # Each path points to a YAML file defining a semantic model
    AVAILABLE_SEMANTIC_MODELS_PATHS = [
        # "DEMO_DB.REVENUE_TIMESERIES.RAW_DATA/HT_del1.yml",
        'CORTEX_ANALYST_DEMO.REVENUE_TIMESERIES.RAW_DATA/Audit_6.yaml'
    ]
        
    # API_ENDPOINT = "/api/v2/cortex/analyst/message"
    API_ENDPOINT = "https://OTBIIMK-LOB94305.snowflakecomputing.com/api/v2/cortex/analyst/message"
    API_TIMEOUT = 100000  # in milliseconds

    # Initialize a Snowpark session for executing queries
    # session = get_active_session()

    # st.set_page_config(layout='wide')

    def post_cortex_request(token: str, question: str):
        """Post request to Snowflake Cortex API"""
        headers={
            "Authorization": f'Snowflake Token="{token}"', 
            "Content-Type": "application/json", 
        }
        request_body = {
            "messages": [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": question
                }]
            }],

            "semantic_model_file": "@CORTEX_ANALYST_DEMO.REVENUE_TIMESERIES.RAW_DATA/Audit_6.yaml"
        
        }
        response = requests.post(API_ENDPOINT , json=request_body, headers=headers)
        print("\nResponse Code: ",response.json())
        return response.json()

    token = conn.rest.token
    # print("\nToken: ",token)

    response = post_cortex_request(token, input_text)
    # print("\nResponse: ",response["message"]["content"][1]["statement"])

    query = session.sql(f"""{response["message"]["content"][1]["statement"]}""").collect()

    return query


class EchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text
        # Echo the user's message back to them
        # print(f"Received message: {text}")
        # f"{cortex(text)[0]}"
        response = cortex(text)
        # print("-------- TYPE -----------:",type(cortex(text)))
        print(f"\n------- RESPONSE ----------:{response[0]}")

        
        await turn_context.send_activity(f"{response[0]}")

        # await turn_context.send_activity(f"You said: {turn_context.activity.text}")