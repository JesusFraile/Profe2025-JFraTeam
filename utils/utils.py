import pandas as pd
import json
import numpy as np


def convert_letter_to_number(letter):
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D':3}
    return mapping.get(letter, -1)


def load_dataset(path):
    """
    Loads a dataset from a JSON file and converts it into a pandas DataFrame.

    Parameters:
    path (str): The file path to the JSON dataset.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - 'exerciseID': ID of the exercise.
        - 'exercise_text': Text of the exercise.
        - 'questionId': ID of the question.
        - 'question_text': Text of the question.
        - 'A': Text of option A.
        - 'B': Text of option B.
        - 'C': Text of option C.
        - 'D': Text of option D.

    The function reads a JSON file containing exams, extracts exercises and their questions, 
    and constructs a structured DataFrame.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data=json.load(file)
        df=pd.DataFrame(columns=['exerciseID', 'exercise_text', 'questionId', 'question_text', 'A', 'B', 'C', 'D'])
        for exam in data['exams']:
            for exercise in exam['exercises']:
                exerciseID=exercise['exerciseID']
                exercise_text=exercise['exercise']['text']
                for question in exercise['exercise']['questions']:
                    questionId=question['questionId']
                    question_text=question['text']
                    a=next(item['text'] for item in question['options'] if item['optionId'] == 'A')
                    b=next(item['text'] for item in question['options'] if item['optionId'] == 'B')
                    try:
                        c=next(item['text'] for item in question['options'] if item['optionId'] == 'C')
                    except:
                        c=''
                    try:
                        d=next(item['text'] for item in question['options'] if item['optionId'] == 'D')
                    except:
                        d=''
                    row={'exerciseID':exerciseID, 'exercise_text':exercise_text, 'questionId':questionId,
                        'question_text':question_text, 'A':a, 'B':b, 'C':c, 'D':d}
                    df=pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        return df
    except:
        print(exercise)

def check_nan(value):
    try:
        # Converting value to float
        if np.isnan(float(value)):
            return True
        return False
    except (ValueError, TypeError):
        # If it cannot be converted, it is a non-NaN string.
        return False

def create_answers_df(df):
    answers_df=pd.DataFrame(columns=['option_responder', 'justification_responder', 
                                 'answer_blind_responder', 'semantic_option', 'semantic_scores',
                                 'option_evaluator1', 'justification_evaluator1',
                                 'option_evaluator2', 'justification_evaluator2',
                                 'option_evaluator3', 'justification_evaluator3',
                                 'option_mediator', 'justification_mediator', 
                                 'final_answer'])
    answers_df['questionId']=df['questionId']
    return answers_df

def get_question(df, i):
    exercise_text=df['exercise_text'].iloc[i]
    question_text=df['question_text'].iloc[i]
    a=df['A'].iloc[i]
    b=df['B'].iloc[i]
    c=df['C'].iloc[i]
    d=df['D'].iloc[i]
    return exercise_text, question_text, [a, b, c, d]