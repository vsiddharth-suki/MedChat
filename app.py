from flask import Flask, request, jsonify, render_template
from recordVoice import record_audio
from speechToText import derived_text_from_speech
from fetchNotes import retrieve_whole_data, get_content, get_patient_and_doctor_names
from searchPatientNotes import get_patient_notes_by_name
from answerToQuery import response_to_query
from textToSpeech import derived_speech_from_text
import threading
import pymongo


app = Flask(__name__)

notes = None    # initialize medical notes as none

# function to render the index page in frontend
@app.route('/')
def index():
    return render_template('index.html')    # render the landing page of website


# function to record and process the query as text
@app.route('/record', methods=['POST'])
def record():
    try:
        # Record audio
        record_audio("./audio.wav")

        # Convert speech to text to process the query
        query = derived_text_from_speech()

        return jsonify({"query": query}), 200   # return 200 for OK status

    except Exception as e:
        return jsonify({"error": f"An error occurred while recording and processing query: {str(e)}"}), 500  # return 500 for internal server error


# function to fetch and read response to the query post data retrieval
@app.route('/medchat', methods=['POST'])
def medchat():
    global notes    # notes in global scope
    if notes is None:
        try:
            # Retrieve whole data
            notes = retrieve_whole_data()
        except Exception as e:
            return jsonify({"error": f"An error occurred while fetching all medical notes: {str(e)}"}), 500     # return 500 for internal server error

    try:
        query = request.json.get('message')     # fetch the query as text
        # if bye word is present in the query
        if "bye" in query.lower():
            response = "See you later!"
            threading.Thread(target=derived_speech_from_text, args=(response,)).start()
            return jsonify({"response": response, "query": query}), 200     # return 200 for OK status

        # Get patient's notes and name
        patient_note, patient_name = get_patient_notes_by_name(query, notes)

        # Generate response to query
        response = response_to_query(query, patient_note, patient_name)

        # Return response first, then read aloud
        # threading is used to first return the response to the frontend, till when the reading function waits
        threading.Thread(target=derived_speech_from_text, args=(response,)).start()
        return jsonify({"response": response, "query": query}), 200     # return 200 for OK status
    except Exception as e:
        return jsonify({"error": str(e)}), 500      # return 500 for internal server error


# function to greet the doctor
@app.route('/greet', methods=['POST'])
def greet():
    try:
        greeting_message = "Hi! I'm MedChat, your voice-based medical assistant. What can I help you with?"
        threading.Thread(target=derived_speech_from_text, args=(greeting_message,)).start()
        return jsonify({"response": greeting_message}), 200     # return 200 for OK status
    except Exception as e:
        return jsonify({"error": str(e)}), 500      # return 500 for internal server error
    

# function to handle the upload of new notes and accordingly update the database
@app.route('/upload', methods=['POST'])
def upload():
    global notes
    try:
        file_content = request.get_json()
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["medical_records"]
        collection = db["notes"]
        # Save the content to the MongoDB collection
        collection.insert_one({"note_data": file_content})
        
        # Update the in-memory notes dictionary
        if notes is None:
            notes = retrieve_whole_data()  # Retrieve all notes initially if not already done
        names = get_patient_and_doctor_names(file_content)
        content = get_content(file_content)
        if names in notes:
            notes[names] += content
        else:
            notes[names] = content
        return jsonify({'success': True}), 200      # return 200 for OK status
    except Exception as e:
        return jsonify({'error': str(e)}), 500      # return 500 for internal server error


if __name__ == "__main__":
    app.run(port=5000, debug=True)      # start the flask app on port 5000
