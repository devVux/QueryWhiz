from app.core.base_model import Model
from app.core.base_request import UserRequest
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class DefogAI(Model):

    def __init__(self):

        self.__tokenizer = AutoTokenizer.from_pretrained("defog/sqlcoder-7b-2")
        self.__model = AutoModelForCausalLM.from_pretrained("defog/sqlcoder-7b-2")


    def generate(data: UserRequest) -> str:

        question = data.prompt
        schema = data.context

        prompt = f"""
            ### Task
            Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

            ### Database Schema
            The query will run on a database with the following schema:
            {schema}

            ### Answer
            Given the database schema, here is the SQL query that [QUESTION]{user_question}[/QUESTION]
            [SQL]
        """

        inputs = tokenizer(prompt, return_tensors="pt")

        outputs = model.generate(
            **inputs,
            max_length=100,
            num_return_sequences=1,
            do_sample=False
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)


