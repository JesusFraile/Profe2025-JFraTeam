"""Agent that evaluates the initial response."""

import google.generativeai as genai
import time
import json
from controllers.controllers import extract_json
class evaluatorAgent():
    def __init__(self, api_key, model_name):
        genai.configure(api_key=api_key)
        self.model=genai.GenerativeModel(model_name)
        self.task='evaluator'
        self.max_attempts=5

    def generate_prompt(self, exercise, question, option):
        prompt=f"""
Eres un experto evaluador en preguntas sobre el conocimiento de la lengua española. Tu objetivo es decidir si la respuesta que se ha dado para contestar a una pregunta es correcta o no y devolver una justificación de tu respuesta.
<TEXT>
{exercise}
</TEXT>

<QUESTION>
{question}
</QUESTION>

<ANSWER TO EVALUATE>
{option}
</ANSWER TO EVALUATE>

<INSTRUCTIONS>
You have to generate a json:
{{
  "valid_answer": "Yes or No (ONLY ONE)",
  "justification": "Explain why this option was selected based on the given input"
}}
</INSTRUCTIONS>
"""
        return prompt



    def do_inference(self, exercise, question, option):

        global current_tpm, current_rpd, start_time, responses_today
        attempts = 0
        while attempts < self.max_attempts:
            try:
                #Completar con el control de límite
                prompt=self.generate_prompt(exercise, question, option)
                response=self.model.generate_content(prompt)
                time.sleep(5)
                # print(response)
                entry_result_json = extract_json(response.text, self.task)
                selected_option=entry_result_json[0]
                justification=entry_result_json[1]

                return selected_option.lower(), justification
            except (json.JSONDecodeError, Exception) as error:
              print(f"Error encountered (attempt {attempts + 1}):", error)
            #   print(response)
              attempts += 1
              time.sleep(10)  
            except Exception as error:
                if "429" in str(error):  
                    print("Error 429: Resource has been exhausted. Waiting 20 seconds before trying again")
                    time.sleep(20)  
                    continue
                print(f"Error encountered (attempt {attempts + 1}):", error)
                attempts += 1
                time.sleep(10)  
        print("Failed after", self.max_attempts, "attempts.")
        return '', response.text

                





