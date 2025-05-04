from experta import KnowledgeEngine, Fact, Rule, DefFacts, W, NOT

def get_valid_input(prompt, options):
    """Reusable function to validate user input."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in options:
            return ans
        else:
            print(f"Invalid input. Please enter one of: {', '.join(options)}")

class Otorhinolaryngology(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        """Initial fact declaration and welcome message"""
        input("Welcome to the ENT Expert System!\n"
              "This assistant will help you identify common ear, nose, or throat conditions.\n"
              "You will be asked a series of yes/no questions.\n"
              "Press ENTER to begin.")
        yield Fact(diagnosis=None)

    # ------------------------------
    # GENERAL QUESTION
    #The symptoms can be located in the ears, nose or throat.
    # ------------------------------
    @Rule(Fact(diagnosis=None), 
          NOT(Fact(location=W())))
    def ask_location(self):
        """Author: Daniela - Asks the location of symptoms"""
        loc = get_valid_input("Where are the symptoms? (ear/nose/throat): ", ["ear", "nose", "throat"])
        self.declare(Fact(location=loc))

    # ------------------------------
    # EAR SECTION
    
    # If the patient has tragal tenderness -> otitis_externa.
    # If the patient doesn't have tragal tenderness, but has fluid in the middle ear -> Acute Otitis Media
    # If the patient doesn't have any of the above, but has ear fullness -> Meniere's Disease.
    # If the patient doesn't have any of the above, but has facial numbness and, very rarely, weakness or loss of muscle movement -> Acoustic Neuroma
    # If it has none of those symptoms, then the patient need to see a doctor.
    # ------------------------------
    @Rule(Fact(location='ear'), 
          NOT(Fact(ear_pain=W())))
    def ask_ear_pain(self):
        """Author: Paulina"""
        ans = get_valid_input("Do you have ear pain or discharge? (yes/no): ", ["yes", "no"])
        self.declare(Fact(ear_pain=(ans == 'yes')))

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          NOT(Fact(tragal_tenderness=W())))
    def ask_tragal(self):
        """Author: Santiago"""
        ans = get_valid_input("Do you have tragal tenderness or canal swelling? (yes/no): ", ["yes", "no"])
        self.declare(Fact(tragal_tenderness=(ans == 'yes')))

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=True))
    def diagnose_otitis_externa(self):
        """Author: Santiago"""
        print("Diagnosis: Otitis Externa")
        self.halt()

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=False), 
          NOT(Fact(middle_fluid=W())))
    def ask_middle_fluid(self):
        """Author: Paulina"""
        ans = get_valid_input("Do you have fever and fluid in the middle ear? (yes/no): ", ["yes", "no"])
        self.declare(Fact(middle_fluid=(ans == 'yes')))

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=False), 
          Fact(middle_fluid=True))
    def diagnose_otitis_media(self):
        """Author: Paulina"""
        print("Diagnosis: Acute Otitis Media")
        self.halt()

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=False), 
          Fact(middle_fluid=False), 
          NOT(Fact(meniere_symptoms=W())))
    def ask_meniere(self):
        """Author: Adrián"""
        ans = get_valid_input("Do you feel ear fullness? (yes/no): ", ["yes", "no"])
        self.declare(Fact(meniere_symptoms=(ans == 'yes')))

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=False), 
          Fact(middle_fluid=False), 
          Fact(meniere_symptoms=True))
    def diagnose_meniere(self):
        """Author: Adrián"""
        print("Diagnosis: Meniere's Disease")
        self.halt()

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=True), 
          Fact(tragal_tenderness=False), 
          Fact(middle_fluid=False), 
          Fact(meniere_symptoms=False),
          NOT(Fact(diagnose_neuroma=W())))
    def ask_diagnose_neuroma(self):
        """Author: Santiago"""
        ans = get_valid_input("Do you have facial numbness and, very rarely, weakness or loss of muscle movement? (yes/no): ", ["yes", "no"])
        self.declare(Fact(diagnose_neuroma=(ans == 'yes')))
    
    
    @Rule(Fact(location='ear'), 
      Fact(ear_pain=True), 
      Fact(tragal_tenderness=False), 
      Fact(middle_fluid=False), 
      Fact(meniere_symptoms=False),
      Fact(diagnose_neuroma=True))
    def diagnose_neuroma_confirmed(self):
        """Author: Santiago"""
        print("Diagnosis: Acoustic Neuroma")
        self.halt()
          

    @Rule(Fact(location='ear'), 
          Fact(ear_pain=False))
    def unclear_ear(self):
        """Author: Adrián"""
        print("Diagnosis: Unclear\nRefer to a specialist.")
        self.halt()
        
    @Rule(Fact(location='ear'), 
      Fact(ear_pain=True), 
      Fact(tragal_tenderness=False), 
      Fact(middle_fluid=False), 
      Fact(meniere_symptoms=False),
      Fact(diagnose_neuroma=False))
    def diagnose_neuroma_unconfirmed(self):
        """Author: Paulina"""
        print("Diagnosis: Unclear\nRefer to a specialist.")
        self.halt()
      

    # ------------------------------
    # NOSE SECTION
    # If the patient has nosebleed -> Epistaxis
    # If the patient has stuffy nose for less than 12 weeks -> Sinusitis
    # If the patient has none of the above, but is sneezing and has itchy eyes/nose, or clear discharge -> Allergic Rhinitis
    # If the patient has none of the above, but has persistent nasal blockage with loss of smell and taste not relieved by decongestants -> nasal polyps
    # If the patient doesn't show any of those symptoms, then it needs to go see a specialist.
    # ------------------------------
    @Rule(Fact(location='nose'), 
          NOT(Fact(nose_bleed=W())))
    def ask_nose_bleed(self):
        """Author: Daniela"""
        ans = get_valid_input("Do you have an active nosebleed? (yes/no): ", ["yes", "no"])
        self.declare(Fact(nose_bleed=(ans == 'yes')))

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=True))
    def diagnose_epistaxis(self):
        """Author: Daniela"""
        print("Diagnosis: Epistaxis")
        self.halt()

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          NOT(Fact(facial_pain=W())))
    def ask_facial_pain(self):
        """Author: Paulina"""
        ans = get_valid_input("Stuffy nose with facial pain/pressure for less than 12 weeks? (yes/no): ", ["yes", "no"])
        self.declare(Fact(facial_pain=(ans == 'yes')))

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=True))
    def diagnose_sinusitis(self):
        """Author: Paulina"""
        print("Diagnosis: Sinusitis")
        self.halt()

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=False), NOT(Fact(allergy=W())))
    def ask_allergy(self):
        """Author: Daniela"""
        ans = get_valid_input("Sneezing, itchy eyes/nose, or clear discharge? (yes/no): ", ["yes", "no"])
        self.declare(Fact(allergy=(ans == 'yes')))

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=False), Fact(allergy=True))
    def diagnose_rhinitis(self):
        """Author: Daniela"""
        print("Diagnosis: Allergic Rhinitis")
        self.halt()

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=False), 
          Fact(allergy=False), 
          NOT(Fact(nasal_blockage=W())))
    def ask_blockage(self):
        """Author: Adrián"""
        ans = get_valid_input("Persistent nasal blockage with loss of smell and taste not relieved by decongestants? (yes/no): ", ["yes", "no"])
        self.declare(Fact(nasal_blockage=(ans == 'yes')))

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=False), 
          Fact(allergy=False), 
          Fact(nasal_blockage=True))
    def diagnose_polyps(self):
        """Author: Adrián"""
        print("Diagnosis: Nasal Polyps")
        self.halt()

    @Rule(Fact(location='nose'), 
          Fact(nose_bleed=False), 
          Fact(facial_pain=False), 
          Fact(allergy=False), 
          Fact(nasal_blockage=False))
    def unclear_nose(self):
        """Author: Daniela"""
        print("Diagnosis: Unclear\nRefer to a specialist.")
        self.halt()

    # ------------------------------
    # THROAT SECTION
    # If the patient has sore throat or discomfort when swallowing with fever, it could have tonsillitis or pharyngitis.
    # To determine this, if the patient has white exudate on the tonsils, he has tonsillitis, if he
    # doesn't, the he has pharyngitis.
    # If the patient has a sore throat without fever -> Laryngitis
    # If the patient is snoring and has apnea, or daytime sleepiness -> Obstructive Sleep Apnea
    # If it doesn't present any of those symptoms, then the patient needs a specialist.
    # ------------------------------
    @Rule(Fact(location='throat'), 
          NOT(Fact(throat_pain=W())))
    def ask_throat_pain(self):
        """Author: Daniela"""
        ans = get_valid_input("Sore throat or discomfort when swallowing with fever? (yes/no): ", ["yes", "no"])
        self.declare(Fact(throat_pain=(ans == 'yes')))

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=True), 
          NOT(Fact(exudate=W())))
    def ask_exudate(self):
        """Author: Paulina"""
        ans = get_valid_input("White exudate on the tonsils? (yes/no): ", ["yes", "no"])
        self.declare(Fact(exudate=(ans == 'yes')))

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=True), 
          Fact(exudate=True))
    def diagnose_tonsillitis(self):
        """Author: Paulina"""
        print("Diagnosis: Tonsillitis")
        self.halt()

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=True), 
          Fact(exudate=False))
    def diagnose_pharyngitis(self):
        """Author: Daniela"""
        print("Diagnosis: Pharyngitis")
        self.halt()

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=False), 
          NOT(Fact(hoarseness=W())))
    def ask_hoarseness(self):
        """Author: Daniela"""
        ans = get_valid_input("Sore throat without fever? (yes/no): ", ["yes", "no"])
        self.declare(Fact(hoarseness=(ans == 'yes')))

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=False), 
          Fact(hoarseness=True))
    def diagnose_laryngitis(self):
        """Author: Paulina"""
        print("Diagnosis: Laryngitis")
        self.halt()

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=False), 
          Fact(hoarseness=False), 
          NOT(Fact(apnea=W())))
    def ask_apnea(self):
        """Author: Santiago"""
        ans = get_valid_input("Snoring, apnea, or daytime sleepiness? (yes/no): ", ["yes", "no"])
        self.declare(Fact(apnea=(ans == 'yes')))

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=False), 
          Fact(hoarseness=False), 
          Fact(apnea=True))
    def diagnose_apnea(self):
        """Author: Santiago"""
        print("Diagnosis: Obstructive Sleep Apnea")
        self.halt()

    @Rule(Fact(location='throat'), 
          Fact(throat_pain=False), 
          Fact(hoarseness=False), 
          Fact(apnea=False))
    def unclear_throat(self):
        """Author: Daniela"""
        print("Diagnosis: Unclear\nRefer to a specialist.")
        self.halt()

# ------------------------------
# RUNNING THE SYSTEM
# ------------------------------
if __name__ == '__main__':
    while True:
        engine = Otorhinolaryngology()
        engine.reset()
        engine.run()
        again = get_valid_input("\nWould you like to start a new diagnosis? (yes/no): ", ["yes", "no"])
        if again == 'no':
            print("Thank you for using the system. Goodbye!")
            break