import sys
sys.path.append("C:\\pynaoqi-python27\\lib")
from reliable import *
from unreliable import *
from naoqi import ALProxy
import time
import random
import logging
import sys 

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

# Initialize experiment parameters

RELIABILITY_CONDITIONS = ["reliable", "unreliable"]
BEHAVIOR_TYPES = ["transparent_proactive", "transparent_reactive", "non_transparent_proactive", "non_transparent_reactive"]

# Generate a random participant ID
participant_id = random.randint(1, 4)  # Adjust the range as needed

print("Participant ID: {}".format(participant_id))

# Assign reliability condition based on participant ID
if participant_id % 2 == 0:
    reliability_condition = "Reliable"
else:
    reliability_condition = "Unreliable"


# Display assigned behavior type based on reliability condition
print("Assigned reliability condition:" + reliability_condition + " Group")

# Call and run the appropriate behavior based on the reliability condition
if reliability_condition == "Reliable":
    run_reliable_behavior(tts, participant_id)
elif reliability_condition == "Unreliable":
    run_unreliable_behavior(tts, participant_id)


if __name__ == "__main__":
    logging.basicConfig(filename='Pasta_Cooking/logs/interaction_log_participant_{}.txt'.format(participant_id), level=logging.INFO, format='%(asctime)s - %(message)s')
    print("The interaction is completed for Participant: {}" .format(participant_id))
    main()
    
