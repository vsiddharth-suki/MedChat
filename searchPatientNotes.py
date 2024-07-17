import string


# function obtains patient's medical notes and name
# returns a list of 2 elements - note and name of the patient
# if patient is not found, it returns None
def get_patient_notes_by_name(sentence, notes):
    sentence = ''.join(char for char in sentence if char not in string.punctuation)     # remove punctuations from sentence
    words = sentence.split()    # create an array of words in the sentence
    for i in range(len(words) - 1):     # iterate over the words
        first_word = words[i]
        second_word = words[i + 1]
        # iterate over the dictionary
        for key, value in notes.items():
            # check if the pair of adjacent words (all in lowercase) in sentence form a name present as a key in dictionary
            if [first_word.lower(), second_word.lower()] == [word.lower() for word in key[0].split()[:2]]:
                return [str(value), str(key[0])]
    return ["", ""]
