import pytest
import string
from searchPatientNotes import get_patient_notes_by_name


def test_get_patient_notes_by_name_found():
    notes = {
        ("John Doe",): "Note for John",
        ("Jane Smith",): "Note for Jane",
    }
    sentence = "I met John Doe yesterday."
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["Note for John", "John Doe"]


def test_get_patient_notes_by_name_not_found():
    notes = {
        ("John Doe",): "Note for John",
        ("Jane Smith",): "Note for Jane",
    }
    sentence = "I met Alice Johnson yesterday."
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["", ""]


def test_get_patient_notes_by_name_with_punctuation():
    notes = {
        ("John Doe",): "Note for John",
    }
    sentence = "Hey, have you seen John Doe?"
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["Note for John", "John Doe"]


def test_get_patient_notes_by_name_case_insensitive():
    notes = {
        ("John Doe",): "Note for John",
    }
    sentence = "I talked to john doe this morning."
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["Note for John", "John Doe"]


def test_get_patient_notes_by_name_partial_name():
    notes = {
        ("John Doe",): "Note for John",
    }
    sentence = "I met John yesterday."
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["", ""]


def test_get_patient_notes_by_name_multiple_matches():
    notes = {
        ("John Doe",): "Note for John",
        ("Jane Smith",): "Note for Jane",
    }
    sentence = "I met John Doe and Jane Smith today."
    result = get_patient_notes_by_name(sentence, notes)
    assert result == ["Note for John", "John Doe"]  # Only the first match is returned
