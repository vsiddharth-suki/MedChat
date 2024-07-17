import openai
from pathlib import Path
import pygame


# function converts text to speech
def derived_speech_from_text(text):
	# Create a client using OpenAI API key
	client = openai.OpenAI(api_key="sk-proj-f2t71ZJg3ebk88Sn56v5T3BlbkFJQE9k4CAPw7LJZFF4YXPL")

	# Define the path to save the speech file
	speech_file_path = Path(__file__).parent / "speech.mp3"

	# Create speech using the OpenAI API
	response = client.audio.speech.create(
		model="tts-1",
		voice="alloy",
		input=text
	)

	# Save the response to a file
	with open(speech_file_path, 'wb') as f:
		f.write(response.content)

	# Initialize pygame
	pygame.mixer.init()

	# Load and play the audio file
	pygame.mixer.music.load(speech_file_path)
	pygame.mixer.music.play()

	# Keep the script running until the audio is finished
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(50)
