import json
import pymongo


# function returns the names of patient and doctor from a medical note
# returns a tuple of two strings
def get_patient_and_doctor_names(data):
    patient_name, doctor_name = "", ""      # initialize empty strings for names of patient and doctor
    stack = [data]  # create a list of data as a stack to perform depth first search
    # run the loop until stack is not empty or patient and doctor names are not obtained
    while stack and not (len(patient_name) and len(doctor_name)):
        current = stack.pop()   # fetch the last element of list and remove it
        if isinstance(current, dict):   # if the fetched element is a dictionary
            if "patient" in current:    # if the dictionary contains the key "patient"
                patient = current["patient"]    # get the value of the key "patient"
                if isinstance(patient, dict):   # if patient is a dictionary
                    person = patient.get("person", {})  # get the value of key "person" from patient
                    if isinstance(person, dict):    # if person is a dictionary
                        patient_name = person.get("firstName", None)    # get the value of key "firstName" from person
                        if person.get("middleName", None):  # if there is a middle name
                            patient_name += " " + person["middleName"]  # add it to the name
                        if person.get("lastName", None):    # if there is a last name
                            patient_name += " " + person["lastName"]    # add it to the name

            if "user" in current:   # if "user" is a key in current dictionary
                user = current["user"]  # fetch the value of "user"
                if isinstance(user, dict):  # if user is a dictionary
                    person = user.get("person", {}) # get the value of "person" from user
                    if isinstance(person, dict):    # if person is a dictionary
                        doctor_name = person.get("firstName", None)     # get the value of first name from person
                        if person.get("middleName", None):  # if middle name exists
                            doctor_name += " " + person["middleName"]   # add it to the name
                        if person.get("lastName", None):    # if last name exists
                            doctor_name += " " + person["lastName"]     # add it to the name

            # Add nested dictionaries to the stack
            for key, value in current.items():
                if isinstance(value, dict):
                    stack.append(value)

    return (patient_name, doctor_name)


# function returns useful medical content from a json file
# returns an string
def get_content(data):
    content = ""    # initialize content with empty string
    stack = [data]  # create a list of data as a stack to perform depth first search
    while stack:    # loop until stack is not empty
        current = stack.pop()   # fetch the last element of list and remove it
        if isinstance(current, dict):   # if current element is a dictionary
            if "string" in current:     # if key "string" exists in current
                # if value of "string" has a positive length and irrelevant phrases do not exist into it and it is not already added to content
                if len(current["string"]) and "Our team" not in current["string"] and current["string"][:20] not in content:
                    content += current["string"] + " "      # add data to the content
            for key, value in current.items():  # iterate over keys and their values in current dictionary
                if isinstance(value, dict):     # if a value is a dictionary
                    stack.append(value)     # add it to stack
                elif isinstance(value, list):   # if a value is a list
                    for item in value:      # iterate over elements of the list
                        stack.append(item)  # add each element to stack
                elif key == "content":      # if key is "content"
                    stack.append(json.loads(value))     # append its value in json format to stack
    return content


# Function fetches relevant medical data from all the notes
# Returns a dictionary with key: (patient_name -> str, doctor_name -> str) and value: content -> str
def retrieve_whole_data():
    notes = {}
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["medical_records"]
    collection = db["notes"]
    for doc in collection.find():  # Retrieve all documents from the collection and update the notes dictionary
        names = get_patient_and_doctor_names(doc["note_data"])
        content = get_content(doc["note_data"])
        if names in notes:
            notes[names] += content
        else:
            notes[names] = content
    return notes
