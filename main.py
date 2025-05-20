#Importing libraries
from dotenv import load_dotenv
import os
from utils import utils
from agents import responder, blind_responder, evaluator, mediator, semantic_similarity
import pandas as pd
import time
from tqdm import tqdm
import sys

#Constants
load_dotenv() # Load .env variables
API_KEY = os.getenv("API_KEY")
# API_KEY = os.getenv("API_KEY_2")
MODEL_NAME='gemini-2.0-flash'
SEMANTIC_SIMILARITY_PATH='paraphrase-multilingual-MiniLM-L12-v2'
SEMANTIC_THRESHOLD=0.6

SELECTED_SET='test'
SET_PATH=f'datasets/{SELECTED_SET}_set.json'
PATH_TO_SAVE=f'datasets/{SELECTED_SET}_answer.pkl'

#Starting main structure
df=utils.load_dataset(SET_PATH)
if os.path.exists(PATH_TO_SAVE):
    df_answers=pd.read_pickle(PATH_TO_SAVE)
    print("Loaded DataFrame")
else:
    df_answers=utils.create_answers_df(df)
    print("Created new DataFrame")


#Loading models
responder_model=responder.responderAgent(API_KEY, MODEL_NAME)
blind_responder_model=blind_responder.blind_responderAgent(API_KEY, MODEL_NAME)
evaluator_model=evaluator.evaluatorAgent(API_KEY, MODEL_NAME)
mediator_model=mediator.mediatorAgent(API_KEY, MODEL_NAME)

semantic_similarity_model=semantic_similarity.semanticAgent(SEMANTIC_SIMILARITY_PATH)

#Creating pipeline process
for i in tqdm(range(len(df_answers))):
    # print(utils.check_nan(df_answers['final_answer'].iloc[i]))
    if utils.check_nan(df_answers['final_answer'].iloc[i]):
        question_id=df_answers['questionId'].iloc[i]
        row=df[df['questionId']==question_id].iloc[0]
        exercise=row['exercise_text']
        question=row['question_text']
        options=[row[f'{i}'] for i in ['A','B','C', 'D']]

        #Starting first step
        print("Starting First Step")
        responder_option, responder_justification=responder_model.do_inference(exercise, question, options)
        index_responder_option=utils.convert_letter_to_number(responder_option)
        df_answers.at[i, 'option_responder']=responder_option
        df_answers.at[i, 'justification_responder']=responder_justification


        blind_responder_answer=blind_responder_model.do_inference(exercise, question)
        df_answers.at[i, 'answer_blind_responder']=blind_responder_answer
        semantic_option,semantic_scores=semantic_similarity_model.get_scores(blind_responder_answer, options)
        # print(semantic_option)
        df_answers.at[i, 'semantic_option']=semantic_option
        df_answers.at[i, 'semantic_scores']=list(semantic_scores)
        

        if index_responder_option==semantic_option and semantic_scores[semantic_option]>SEMANTIC_THRESHOLD:
            print(f"Final Response -> {responder_option}")
            df_answers.at[i, 'final_answer']=responder_option
        else:
            print("Starting Evaluators")
            options_to_evaluate=options.copy()
            # print(options_to_evaluate)
            del options_to_evaluate[index_responder_option]
            # print(options_to_evaluate)
            if options_to_evaluate[0]=='':
                print('No option')
                evaluator1_option, evaluator1_justification = 'no', ''
            else:
                evaluator1_option, evaluator1_justification=evaluator_model.do_inference(exercise, question, options_to_evaluate[0])
            df_answers.at[i, 'option_evaluator1']=evaluator1_option
            df_answers.at[i, 'justification_evaluator1']=evaluator1_justification

            if options_to_evaluate[1]=='':
                print('No option')
                evaluator2_option, evaluator2_justification = 'no', ''
            else:   
                evaluator2_option, evaluator2_justification=evaluator_model.do_inference(exercise, question, options_to_evaluate[1])
            df_answers.at[i, 'option_evaluator2']=evaluator2_option
            df_answers.at[i, 'justification_evaluator2']=evaluator2_justification

            if options_to_evaluate[2]=='':
                print('No option')
                evaluator3_option, evaluator3_justification = 'no', ''
            else:
                evaluator3_option, evaluator3_justification=evaluator_model.do_inference(exercise, question, options_to_evaluate[2])
                df_answers.at[i, 'option_evaluator3']=evaluator3_option
                df_answers.at[i, 'justification_evaluator3']=evaluator3_justification
            # print(evaluator1_option)
            # print(evaluator1_justification)
            # print(evaluator2_option)
            # print(evaluator2_justification)
            if evaluator1_option=='no' and evaluator2_option=='no' and evaluator3_option=='no':
                print(f"Final Response -> {responder_option}")
                df_answers.at[i, 'final_answer']=responder_option
            else:
                print("Starting Mediator process")
                mediator_option, mediator_justification=mediator_model.do_inference(exercise, question, options, responder_option, responder_justification,blind_responder_answer, evaluator1_option, evaluator1_justification, evaluator2_option, evaluator2_justification, evaluator3_option, evaluator3_justification)
                df_answers.at[i, 'option_mediator']=mediator_option
                df_answers.at[i, 'justification_mediator']=mediator_justification
                df_answers.at[i, 'final_answer']=mediator_option
                print(f"Final Response -> {mediator_option}")
        df_answers.to_pickle(PATH_TO_SAVE, protocol=4)
        print("Saved Answers")
                # print(mediator_option)
                # print(mediator_justification)

