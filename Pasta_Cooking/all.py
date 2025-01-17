import sys
sys.path.append("C:\\pynaoqi-python27\\lib")
from naoqi import ALProxy
import time
import random
import logging
import json

# Common functions
def greet_participant(tts):
    tts.say("Hello, Welcome! I am Pepper, your cooking assistant today. Let's cook pasta together!")

def get_step_delay(step_index):
    # Example: Longer delay for critical steps
    if step_index in [3, 7, 10]:  # Critical steps (e.g., boiling water, adding pasta)
        return 5
    return 3

def post_task_survey():
    questions = {
        "transparency": "How clear were the robot's instructions?",
        "reliability": "How reliable were the robot's instructions?",
        "proactivity": "How proactive was the robot during the interaction?"
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
    
    with open('Pasta_Cooking/logs/survey_results_participants.txt', 'a') as f:
        for key, value in results.items():
            f.write("{}".format(key) + " :" +  " {}".format(value) + '\n')

    return results

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
    
    # Function to ask for feedback after each range of steps 
def ask_for_feedback(tts, behavior): 
    if behavior == 'transparent_proactive': 
        tts.say("How did you find the detailed instructions and explanations? Was everything clear and helpful?") 
    elif behavior == 'transparent_reactive': 
        tts.say("Did you find the quick explanations helpful? Was there anything you didn't understand?") 
    elif behavior == 'non_transparent_proactive': 
        tts.say("Were the brief instructions sufficient? Did you feel guided through the steps?") 
    elif behavior == 'non_transparent_reactive': 
        tts.say("How was the experience with minimal instructions? Did you feel you needed more guidance?")
        

# Define functions to handle reliable behavior
def run_reliable_behavior(tts, participant_id):
    greet_participant(tts)

    path = 'steps_config_updated.json'
    # Open and load the JSON file
    with open('Pasta_Cooking/steps_config_updated.json', 'r') as file:
        steps_config = json.load(file)

    # Define functions for instructions, explanations, and safety reminders
    def instruction(step):
        return step['instruction']

    def explanation(step):
        return step['explanation']

    def safety_reminder(step):
        return step['safety_reminder']

    
    # Define behavior types and generate behavior sequence
    behavior_types = ['transparent_proactive', 'transparent_reactive', 'non_transparent_proactive', 'non_transparent_reactive']
    
    # Shuffle the behavior types to generate a random sequence 
    behavior_sequence = behavior_types[:]
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
                        ask_for_feedback(tts, current_behavior)
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
                    handle_text_input(tts, "next")
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds 
                    handle_text_input(tts, "explain")
                    tts.say("Here's a quick explanation.") 
                    tts.say("{}.".format(explanation(step))) 
                    time.sleep(1) # Wait for 1 second 
                    tts.say("Finally, keep in mind: {}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                    
                    logging.info("Participant {}: Reliable Transparent Reactive | Step: {} | Instruction: {} | Explanation: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), explanation(step), safety_reminder(step)))
                    break
                elif behavior == 'non_transparent_proactive':
                    time.sleep(3) # Wait for 3 seconds 
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                     
                    logging.info("Participant {}: Reliable Non-Transparent Proactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), safety_reminder(step))) 
                    break
                elif behavior == 'non_transparent_reactive': 
                    time.sleep(3) # Wait for 3 seconds
                    handle_text_input(tts, "next")
                    tts.say("Step {}: {}.".format(step['id'], instruction(step))) 
                    time.sleep(2) # Wait for 2 seconds
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5) # Wait for 5 seconds
                     
                    logging.info("Participant {}: Reliable Non-Transparent Reactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], instruction(step), safety_reminder(step)))
                    break

        
    if current_behavior is not None: 
        ask_for_feedback(tts, current_behavior)
    feedback = post_task_survey()

    logging.info("Participant {}: Reliable Participant Feedback: {}".format(participant_id, feedback))

# Define functions to handle unreliable behavior
def run_unreliable_behavior(tts, participant_id):
    greet_participant(tts)

    path = 'steps_config_updated.json'
    # Open and load the JSON file
    with open('Pasta_Cooking/steps_config_updated.json', 'r') as file:
        steps_config = json.load(file)

    # Define functions for incorrect instructions, wrong explanations, and safety reminders
    def incorrect_instruction(step):
        return step['incorrect_instruction']

    def wrong_explanation(step):
        return step['wrong_explanation']

    def safety_reminder(step):
        return step['safety_reminder']

   
    # Define behavior types and generate behavior sequence
    behavior_types = ['transparent_proactive', 'transparent_reactive', 'non_transparent_proactive', 'non_transparent_reactive']
    
    # Shuffle the behavior types to generate a random sequence 
    behavior_sequence = behavior_types[:]
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
                        ask_for_feedback(tts, current_behavior)
                    current_behavior = behavior

                if behavior == 'transparent_proactive':
                    time.sleep(3)      
                    tts.say("Step {}: {}.".format(step['id'], incorrect_instruction(step))) 
                    time.sleep(1) 
                    tts.say("let's explain why this step is important.") 
                    tts.say("{}.".format(wrong_explanation(step))) 
                    time.sleep(2) 
                    tts.say("And remember, {}.".format(safety_reminder(step)))
                    time.sleep(5)
                    logging.info("Participant {}: Unreliable Transparent Proactive | Step: {} | Instruction: {} | Explanation: {} | Safety Reminder: {}".format(participant_id, step['id'], incorrect_instruction(step), wrong_explanation(step), safety_reminder(step)))
                    break
                elif behavior == 'transparent_reactive':
                    time.sleep(3) 
                    handle_text_input(tts, "next")
                    tts.say("Step {}: {}.".format(step['id'], incorrect_instruction(step))) 
                    time.sleep(2) 
                    handle_text_input(tts, "explain")
                    tts.say("Here's a quick explanation.") 
                    tts.say("{}.".format(wrong_explanation(step))) 
                    time.sleep(2) 
                    tts.say("Finally, keep in mind: {}.".format(safety_reminder(step)))
                    time.sleep(5)
                    logging.info("Participant {}: Unreliable Transparent Reactive | Step: {} | Instruction: {} | Explanation: {} | Safety Reminder: {}".format(participant_id, step['id'], incorrect_instruction(step), wrong_explanation(step), safety_reminder(step)))
                    break
                elif behavior == 'non_transparent_proactive':
                    time.sleep(3)      
                    tts.say("Step {}: {}.".format(step['id'], incorrect_instruction(step))) 
                    time.sleep(2) 
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5)
                    logging.info("Participant {}: Unreliable Non-Transparent Proactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], incorrect_instruction(step), safety_reminder(step))) 
                    break
                elif behavior == 'non_transparent_reactive': 
                    time.sleep(3) 
                    handle_text_input(tts, "next")
                    tts.say("Step {}: {}.".format(step['id'], incorrect_instruction(step))) 
                    time.sleep(2) 
                    tts.say("{}.".format(safety_reminder(step)))
                    time.sleep(5) 
                    logging.info("Participant {}: Unreliable Non-Transparent Reactive | Step: {} | Instruction: {} | Safety Reminder: {}".format(participant_id, step['id'], incorrect_instruction(step), safety_reminder(step)))
                    break
        
    if current_behavior is not None: 
        ask_for_feedback(tts, current_behavior)
    feedback = post_task_survey()
    logging.info("Participant {}: Reliable Participant Feedback: {}".format(participant_id, feedback))
    
# Main function to handle overall experiment logic
def main():
    # Connect to Pepper
    robot_ip = "192.168.1.41"
    try:
        tts = ALProxy("ALTextToSpeech", robot_ip, 9559)
        motion = ALProxy("ALMotion", robot_ip, 9559)
        dialog = ALProxy("ALDialog", robot_ip, 9559)
        asr = ALProxy("ALSpeechRecognition", robot_ip, 9559)
        video_recorder = ALProxy("ALVideoRecorder", robot_ip, 9559)
    except Exception as e:
        logging.error("Error connecting to Pepper: " + str(e))
        sys.exit(1)

    # Configure logging
    logging.basicConfig(filename='Pasta_Cooking/logs/interaction_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


    # Initialize experiment parameters
    RELIABILITY_CONDITIONS = ["reliable", "unreliable"]
    BEHAVIOR_TYPES = ["transparent_proactive", "transparent_reactive", "non_transparent_proactive", "non_transparent_reactive"]

    # Generate a random participant ID
    participant_id = random.randint(1, 2)  # Adjust the range as needed
    print("Participant ID: {}".format(participant_id))

    # Assign reliability condition based on participant ID
    if participant_id % 2 == 0:
        reliability_condition = "Reliable"
    else:
        reliability_condition = "Unreliable"

    print("Assigned reliability condition:" + reliability_condition + " Group")

    # Call and run the appropriate behavior based on the reliability condition
    if reliability_condition == "Reliable":
        run_reliable_behavior(tts, participant_id)
        
    else:
        run_unreliable_behavior(tts, participant_id)

    logging.basicConfig(filename='Pasta_Cooking/logs/interaction_log_participant.txt'.format(participant_id), level=logging.INFO, format='%(asctime)s - %(message)s')
    print("The interaction is completed for Participant: {}" .format(participant_id))
    main()

if __name__ == "__main__":
    main()
    
