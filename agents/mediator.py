"""Agent providing a final response if necessary, taking into account the responses of all models."""
import google.generativeai as genai
import time
import json
from controllers.controllers import extract_json

class responderAgent():
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model=genai.GenerativeModel("gemini-1.5-flash")
        self.task='mediator'
        self.max_attempts=5

    def generate_prompt(self, exercise, question, options, responder_answer, responder_justification, evaluator1_answer, evaluator1_justification, evaluator2_answer, evaluator2_justification, blind_responder_answer, blind_responder_justification):
        l=['A', 'B', 'C']
        l.remove(responder_answer)

        prompt=f"""
Estás actuando como un agente mediador en un proceso de resolución de desacuerdos entre cuatro agentes. Cada uno tiene un enfoque diferente para abordar la pregunta planteada. Tu tarea es facilitar la resolución del desacuerdo y garantizar que todos los agentes lleguen a un consenso basado en la justificación de sus respuestas.

<AGENTS DESCRIPTIONS>
Agente 1: Responde a la pregunta basada en las posibles respuestas disponibles. Tiene que dar una justificación de la respuesta.
Agente 2: Responde a la pregunta sin ver las posibles respuestas disponibles. Posteriormente se realiza un match por similitud semántica entre su respuesta y las posibles respuestas disponibles.
Agente 3 y 4: Reciben las respuestas no seleccionadas por el Agente 1 y responden si esas respuestas son correctas o no. 
</AGENTS DESCRIPTIONS>

<TEXT>
{exercise}
</TEXT>

<QUESTION>
{question}
</QUESTION>

<OPTIONS>
A: {options[0]}
B: {options[1]}
C: {options[2]}
</OPTIONS>

<AGENTS ANSWERS>
*Agente 1: Respuesta: {responder_answer}. Justificacion: {responder_justification}
*Agente 2: Respuesta: {blind_responder_answer}.
*Agente 3: Respuesta para la opción {l[0]}: {evaluator1_answer}. Justificacion: {evaluator1_justification}
*Agente 4: Respuesta para la opción {l[1]}: {evaluator2_answer}. Justificacion: {evaluator2_justification}
</AGENTS ANSWERS>

<INSTRUCTIONS>
You have to generate a json:
{{
  "selected_option": "Chosen option A, B, or C (ONLY ONE)",
  "justification": "Explain why this option was selected based on the given input"
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
                selected_option=entry_result_json[0]
                justification=entry_result_json[1]

                return selected_option, justification
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
        return '', response.text

                





