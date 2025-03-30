import pandas as pd
import json


def convert_letter_to_number(letter):
    mapping = {'A': 0, 'B': 1, 'C': 2}
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

    The function reads a JSON file containing exams, extracts exercises and their questions, 
    and constructs a structured DataFrame.
    """

    with open(path, 'r', encoding='utf-8') as file:
        data=json.load(file)
    df=pd.DataFrame(columns=['exerciseID', 'exercise_text', 'questionId', 'question_text', 'A', 'B', 'C'])
    for exam in data['exams']:
        for exercise in exam['exercises']:
            exerciseID=exercise['exerciseID']
            exercise_text=exercise['exercise']['text']
            for question in exercise['exercise']['questions']:
                questionId=question['questionId']
                question_text=question['text']
                a=next(item['text'] for item in question['options'] if item['optionId'] == 'A')
                b=next(item['text'] for item in question['options'] if item['optionId'] == 'B')
                c=next(item['text'] for item in question['options'] if item['optionId'] == 'C')
                row={'exerciseID':exerciseID, 'exercise_text':exercise_text, 'questionId':questionId,
                    'question_text':question_text, 'A':a, 'B':b, 'C':c}
                df=pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    return df