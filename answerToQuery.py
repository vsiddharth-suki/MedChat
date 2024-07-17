from openai import OpenAI


# function returns response to a query
def response_to_query(query, patient_note, patient_name):
	client = OpenAI(api_key="sk-proj-f2t71ZJg3ebk88Sn56v5T3BlbkFJQE9k4CAPw7LJZFF4YXPL")		# creating the API client using a key
	# response uses GPT-4o model, comes in text format
	# system role gives the model the details of an event or situation
	# user role gives the prompt to the model to respond according to the details provided
	response = client.chat.completions.create(
		model="gpt-4o",
		response_format={ "type": "text" },
		messages=[
			{"role": "system", "content": f"Details of {patient_name} are: " + patient_note if len(patient_name) else "You are a helpful medical assistant"}, 
			{"role": "user", "content": query}
		]
	)
	return response.choices[0].message.content
