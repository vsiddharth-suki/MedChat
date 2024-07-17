from openai import OpenAI


# function converts speech into text
# returns string
def derived_text_from_speech():
	client = OpenAI(api_key="sk-proj-f2t71ZJg3ebk88Sn56v5T3BlbkFJQE9k4CAPw7LJZFF4YXPL")		# connect a client using API key
	audio_file= open("audio.wav", "rb")		# read audio file in binary format
	transcription = client.audio.transcriptions.create(
		model="whisper-1", 
		file=audio_file, 
		response_format="text"
	)
	return str(transcription).rstrip()	# remove trailing spaces, if any, from the text
