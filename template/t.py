import sys
sys.path.append("C:\\pynaoqi-python27\\lib")
from naoqi import ALProxy
import json
import time

# Connect to Pepper
robot_ip = "192.168.1.41"  # Replace with your Pepper's IP address
tablet_service = ALProxy("ALTabletService", robot_ip, 9559)
tts = ALProxy("ALTextToSpeech", robot_ip, 9559)

# Display the HTML page
tablet_service.showWebview("http://192.168.1.41:5000/pepper_tablet_ui.html")  # Use your server hosting the page

# Steps to guide user
steps_data = [
    {"instruction": "Step 1: Fill a pot with water and place it on the stove.", 
     "explanation": "This is necessary to cook the pasta.", 
     "safety_reminder": "Be careful with water."},
    {"instruction": "Step 2: Turn on the stove and wait for the water to boil.", 
     "explanation": "Boiling water is necessary for cooking pasta.", 
     "safety_reminder": "Beware of hot surfaces."},
    {"instruction": "Step 3: Add pasta to the boiling water.", 
     "explanation": "Adding pasta starts the cooking process.", 
     "safety_reminder": "Avoid splashing hot water."}
]

# Send JSON data to update the interface
with open("steps_config_updated.json", "w") as json_file:
    json.dump({"steps": steps_data}, json_file)

# Speech and tablet interaction
def say_and_update(instruction):
    tts.say(instruction)
    event_script = """
    var event = new CustomEvent('updateInstruction', {{ detail: {{ instruction: '{instruction}' }} }});
    window.dispatchEvent(event);
    """
    tablet_service.executeJS(event_script)

# Simulating the step-by-step guidance
for step in steps_data:
    instruction = step["instruction"]
    say_and_update(instruction)
    time.sleep(5)  # Simulate time between steps

tts.say("Cooking completed!")
