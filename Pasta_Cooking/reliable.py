import sys
sys.path.append("C:\\pynaoqi-python27\\lib")
from naoqi import ALProxy
from flask import Flask, render_template, request, jsonify
import time
import random
import logging
import json
from random import sample

app = Flask(__name__)

# Connect to Pepper
robot_ip = "192.168.1.41"
try:
    tts = ALProxy("ALTextToSpeech", robot_ip, 9559)
    motion = ALProxy("ALMotion", robot_ip, 9559)
    tablet_service = ALProxy("ALTabletService", robot_ip, 9559)
    dialog = ALProxy("ALDialog", robot_ip, 9559)
    asr = ALProxy("ALSpeechRecognition", robot_ip, 9559)
except Exception as e:
    print("Error connecting to Pepper: " + str(e))
    sys.exit(1)


tablet_service.showWebview("/home/nao/HRT-Project/Pasta_Cooking/template/pepper_tablet_ui.html")
# Configure logging
logging.basicConfig(filename='Pasta_Cooking/logs/interaction_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initializing participant ID
total_participant = []

from shared_function import (greet_participant, get_step_delay, post_task_survey)

def run_reliable_behavior(tts, participant_id):
    greet_participant(tts)

    path = 'steps_config_updated.json'
    #participants = 2

    # Open and load the JSON file
    with open('Pasta_Cooking/steps_config_updated.json', 'r') as file:
        steps_config = json.load(file)

    # Define functions
    def instruction(step):
        return step['instruction']

    def explanation(step):
        return step['explanation']

    def safety_reminder(step):
        return step['safety_reminder']

    def handle_text_input(tts, text_input): 
        if "next" in text_input.lower(): 
            tts.say("I will provide you the instruction.")
        elif "repeat" in text_input.lower(): 
            tts.say("Ok, I can repeat it for you.")
        elif "explain" in text_input.lower(): 
            tts.say("Sure, I can explain again.") 
        elif "reminder" in text_input.lower(): 
            tts.say("Here is a safety reminder.") 
        elif "next" in text_input.lower(): 
            tts.say("Moving to the next step.") 
        else: 
            tts.say("I didn't understand that command.")
    
    # Main route for the web interface 
    @app.route('/') 
    def index(): 
        return render_template('/home/nao/HRT-Project/Pasta_Cooking/template/pepper_tablet_ui.html')
    
    # Route to handle commands sent from the web interface 
    @app.route('/send_command', methods=['POST']) 
    def send_command(): 
        text_input = request.form['command'] 
        step_id = int(request.form['step_id']) 
        step = next((step for step in steps_config['steps'] if step['id'] == step_id), None) 
        handle_text_input(text_input, step) 
        return jsonify(success=True)

    # Function to ask for feedback after each range of steps 
    def ask_for_feedback(behavior): 
        if behavior == 'transparent_proactive': 
            tts.say("How did you find the detailed instructions and explanations? Was everything clear and helpful?") 
        elif behavior == 'transparent_reactive': 
            tts.say("Did you find the quick explanations helpful? Was there anything you didn't understand?") 
        elif behavior == 'non_transparent_proactive': 
            tts.say("Were the brief instructions sufficient? Did you feel guided through the steps?") 
        elif behavior == 'non_transparent_reactive': 
            tts.say("How was the experience with minimal instructions? Did you feel you needed more guidance?")
            
   # Define behavior types and generate behavior sequence
    behavior_types = ['transparent_proactive', 'transparent_reactive', 'non_transparent_proactive', 'non_transparent_reactive']
    
   # Shuffle the behavior types to generate a random sequence 
    behavior_sequence = behavior_types[:]
    
    #random shuffle the behavior sequence
    random.shuffle(behavior_sequence)

    # Print the shuffled sequence for verification
    print("Shuffled behavior sequence:", behavior_sequence)

    # Define step ranges for each behavior in the random sequence
    behavior_ranges = {
        behavior_sequence[0]: range(1, 5),
        behavior_sequence[1]: range(5, 9),
        behavior_sequence[2]: range(9, 12),
        behavior_sequence[3]: range(12, 15)
    }

    # Iterate through the steps and generate the behavior sequence 
    current_behavior = None                                        
    for step in steps_config['steps']:
        for behavior, step_range in behavior_ranges.items():
            if step['id'] in step_range:
                if current_behavior != behavior:
                    if current_behavior is not None:
                        ask_for_feedback(current_behavior)
                    current_behavior = behavior

                if behavior == 'transparent_proactive':
                    
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(3) # Wait for 3 seconds 
                    tts.say("let's explain why this step is important.") 
                    tts.say("{}.".format(explanation(step))) 
                    time.sleep(2) # Wait for 2 seconds 
                    tts.say("And remember, {}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                    
                    logging.info("Participant {}: Reliable Transparent Proactive | Step: {} | Instruction: {} | Explanation: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), explanation(step), safety_reminder(step)))
                    break
                elif behavior == 'transparent_reactive':
                    time.sleep(3) # Wait for 3 seconds
                    text_input = "next" 
                    handle_text_input(tts, text_input)
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds 
                    text_input = "explain" 
                    handle_text_input(tts, text_input)
                    tts.say("Here's a quick explanation.") 
                    tts.say("{}.".format(explanation(step))) 
                    time.sleep(1) # Wait for 1 second 
                    tts.say("Finally, keep in mind: {}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                    
                    logging.info("Participant {}: Reliable Transparent Reactive | Step: {} | Instruction: {} | Explanation: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), explanation(step),safety_reminder(step)))
                    break
                elif behavior == 'non_transparent_proactive':
                    time.sleep(3) # Wait for 3 seconds 
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds
                    #tts.say("Please be cautious as you proceed.") 
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                     
                    logging.info("Participant {}: Reliable Non-Transparent Proactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), safety_reminder(step))) 
                    break
                elif behavior == 'non_transparent_reactive': 
                    time.sleep(3) # Wait for 3 seconds
                    text_input = "next" 
                    handle_text_input(tts, text_input)
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                     
                    logging.info("Participant {}: Reliable Non-Transparent Reactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), safety_reminder(step)))
                    break
    if current_behavior is not None: 
        ask_for_feedback(current_behavior)
        

    feedback = post_task_survey(tts)

    # Save results to a JSON file
    
    logging.info("Participant {}: Reliable Participant Feedback: {}".format(participant_id, feedback))

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=5000, debug=True)
    # Loop for participants
    for participant_id in range(2, 4):  
        # Configure logging for each participant
        run_reliable_behavior(tts, participant_id)
        logging.basicConfig(filename='Pasta_Cooking/logs/reliable_interaction_log_participant_{}.txt'.format(participant_id), level=logging.INFO, format='%(asctime)s - %(message)s')
        print("Completed interaction for Participant {participant_id}")
