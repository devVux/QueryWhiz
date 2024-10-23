from app.core.base_model import Model
from app.core.base_request import UserRequest
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class DefogAI(Model):

    def __init__(self):
        self.__tokenizer = AutoTokenizer.from_pretrained("defog/sqlcoder-7b-2")
        self.__model = AutoModelForCausalLM.from_pretrained("defog/sqlcoder-7b-2")

        if torch.cuda.is_available():
            self.__model = self.__model.to("cuda")
        else:
            print("Warning: GPU not available. Using CPU.")

    def generate(self, data: UserRequest) -> str:
        question = data.question
        schema = data.context

        question = f"""
            ### Task
            Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

            ### Database Schema
            The query will run on a database with the following schema:
            {schema}

            ### Answer
            Given the database schema, here is the SQL query that [QUESTION]{question}[/QUESTION]
            [SQL]
        """

        # make sure the model stops generating at triple ticks
        eos_token_id = self.__tokenizer.eos_token_id
        pipe = pipeline(
            "text-generation",
            model=self.__model,
            tokenizer=self.__tokenizer,
            device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
            max_new_tokens=300,
            do_sample=False,
            return_full_text=False,  # Prevent splitting issues with question
            num_beams=5,  # Beam search with 5 beams for high-quality results
        )
        generated_query = (
            pipe(
                question,
                num_return_sequences=1,
                eos_token_id=eos_token_id,
                pad_token_id=eos_token_id,
            )[0]["generated_text"]
            .split(";")[0]
            .split("```")[0]
            .strip()
            + ";"
        )
        return generated_query


class SlimSQL(Model): 

    def __init__(self):

        self.__tokenizer = AutoTokenizer.from_pretrained("llmware/slim-sql-1b-v0")  
        self.__model = AutoModelForCausalLM.from_pretrained("llmware/slim-sql-1b-v0")  
        
        if torch.cuda.is_available():
            self.__model = self.__model.to("cuda")
        else:
            print("Warning: GPU not available. Using CPU.")

    def generate(self, data: UserRequest) -> str:

        # prepare question packaging used in fine-tuning process
        new_question = "<human>: " + data.context + "\n" + data.question + "\n" + "<bot>:"

        inputs = self.__tokenizer(new_question, return_tensors="pt")  
        start_of_output = len(inputs.input_ids[0])

        #   temperature: set at 0.3 for consistency of output
        #   max_new_tokens:  set at 100 - may prematurely stop a few of the summaries

        outputs = self.__model.generate(
                inputs.input_ids,
                eos_token_id=self.__tokenizer.eos_token_id,
                pad_token_id=self.__tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.3,
                max_new_tokens=100,
                )

        return self.__tokenizer.decode(outputs[0][start_of_output:],skip_special_tokens=True)

