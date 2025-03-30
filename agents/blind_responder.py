"""Agent that generates an initial response without any option visible"""

import google.generativeai as genai
import time
import json
from controllers.controllers import extract_json
class blind_responderAgent():
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model=genai.GenerativeModel("gemini-1.5-flash")
        self.task='blind_responder'
        self.max_attempts=5

    def generate_prompt(self, exercise, question):
        prompt=f"""
Eres un experto en el conocimiento de la lengua española y en la comprensión de textos. Tu tarea es analizar el siguiente texto y responder correctamente a una pregunta.
<TEXT>
{exercise}
</TEXT>

<QUESTION>
{question}
</QUESTION>


<INSTRUCTIONS>
Responde lo más breve posible. No hagas ninguna descripción ni justificación.
You have to generate a json:
{{
  "response": "Short answer without description",
}}
</INSTRUCTIONS>
"""
        return prompt



    def do_inference(self, exercise, question, options):

        global current_tpm, current_rpd, start_time, responses_today
        attempts = 0
        while attempts < self.max_attempts:
            try:
                #Completar con el control de límite
                prompt=self.generate_prompt(exercise, question, options)
                response=self.model.generate_content(prompt)
                # print(response)
                entry_result_json = extract_json(response.text, self.task)
                answer=entry_result_json[0]
                

                return answer
            except (json.JSONDecodeError, Exception) as error:
              print(f"Error encountered (attempt {attempts + 1}):", error)
              print(response)
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
        return response.text

                





