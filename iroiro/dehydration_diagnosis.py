"""
Dehydration Diagnosis Program
This program allows a "medical professional" to list patients and run dehydration diagnoses based on patient symptoms.
"""

running = True

# region messages
messages = {
    "welcome": "Welcome professor, please choose an action.",
    "list_patients": "Listing all patients:",
    "new_diagnosis": "Running a new diagnosis.",
    "enter_name": "Please enter patient's name:",
    "appearance_note": "Anything to note with the patient's general appearance?",
    "eyes_condition": "How are the patient's eyes looking?",
    "skin_condition": "How does the patient's skin behave when pinched?",
    "invalid_selection": "Invalid selection. Please try again...",
    "operation_cancelled": "Operation cancelled.",
    "closing_program": "Closing program."
}

prompts = {
    "welcome": ("\n"
                + "(1) List all patients\n"
                + "(2) Run a new diagnosis\n"
                + "(0) Close program\n"),
    "appearance_note": ("\n"
                        + "(1) Patient looks normal.\n"
                        + "(2) Patient is irritable or lethargic.\n"
                        + "(0) Cancel diagnosis\n"),
    "eyes_condition": ("\n"
                       + "(1) Normal or slightly sunken\n"
                       + "(2) Markedly sunken\n"
                       + "(0) Cancel diagnosis\n"),
    "skin_condition": ("\n"
                       + "(1) Skin returns normally\n"
                       + "(2) Skin returns slowly\n"
                       + "(0) Cancel diagnosis\n")
}

symbols = {
    "error": "e",
    "cancel": "x"
}

results = {
    "severe": "Severe dehydration.",
    "mild": "Mild dehydration.",
    "normal": "No dehydration observed."
}
# endregion

diagnoses = [
    "Andrew: " + results["normal"],
    "Beatriz: " + results["severe"],
    "Chris: " + results["mild"] 
]

def list_patients():
    for entry in diagnoses:
        print(entry)

def create_diagnosis():
    patient_name = input(messages["enter_name"] + "\n")
    patient_results = assess_appearance()
    if patient_results == symbols["cancel"]:
        print(messages["operation_cancelled"])
    else:
        create_patient_entry(patient_name, patient_results)

    

def assess_appearance():
    while True:
        res = input(messages["appearance_note"] + prompts["appearance_note"] + '> ')
        match res:
            case "1":
                res = assess_eyes(input(messages["eyes_condition"] + prompts["eyes_condition"] + '> '))
                while res == symbols["error"]:
                    print(messages["invalid_selection"])
                    res = assess_eyes(input(messages["eyes_condition"] + prompts["eyes_condition"] + '> '))
                return res
            
            case "2":
                res = assess_skin(input(messages["skin_condition"] + prompts["skin_condition"] + '> '))
                while res == symbols["error"]:
                    print(messages["invalid_selection"])
                    res = assess_skin(input(messages["skin_condition"] + prompts["skin_condition"] + '> '))
                return res
            
            case "0":
                return symbols["cancel"]

            case _:
                print(messages["invalid_selection"])

def assess_skin(result):
    match result:
        case "1": return results["mild"]
        case "2": return results["severe"]
        case "0": return symbols["cancel"]
        case _: return symbols["error"]

def assess_eyes(result):
    match result:
        case "1": return results["normal"]
        case "2": return results["severe"]
        case "0": return symbols["cancel"]
        case _: return symbols["error"]

def create_patient_entry(name, results):
    diagnosis = "{}: {}".format(name, results)
    print("Creating entry for ", diagnosis)
    diagnoses.append(diagnosis)
    diagnoses.sort()

def quit_program():
    global running
    running = False

def complete_action():
    print("\n******\n")

def main():
    while (running):
        selection = input(messages["welcome"] + prompts["welcome"] + '> ')
        match selection:
            case "1": 
                print(messages["list_patients"])
                list_patients()
            case "2": 
                print(messages["new_diagnosis"])
                create_diagnosis()
            case "0":
                print(messages["closing_program"])
                quit_program()
        complete_action()

main()