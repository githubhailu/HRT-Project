import sys
sys.path.append("C:\\pynaoqi-python27\\lib")
from naoqi import ALProxy
import time
import random
import logging
import json
from random import sample

# Common functions
def greet_participant(tts):
    tts.say("Hello, Welcome! I am Pepper, your cooking assistant today. Let's cook pasta together!")

def get_step_delay(step_index):
    # Example: Longer delay for critical steps
    if step_index in [3, 7, 10]:  # Critical steps (e.g., boiling water, adding pasta)
        return 5
    return 3

def post_task_survey(dialog):
    
    questions = {
        "transparency": "How clear were the robot's instructions?",
        "reliability": "How reliable were the robot's instructions?",
        "Proactivity": "How proactive was the robot during the interaction?"
    }
    results = {}
    for key, question in questions.items():
        while True:
            try:
                rating = int(input(question + " (1-5): "))
                if 1 <= rating <= 5:
                    results[key] = rating
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
                
                
    # Save results to a text file
    with open('Pasta_Cooking/logs/survey_results_participants.txt', 'a') as f:
        print("Survey results for participant {}:")
        for key, value in results.items():
            f.write("{}".format(key) + " :" +  " {}".format(value) +'\n')

    return results

