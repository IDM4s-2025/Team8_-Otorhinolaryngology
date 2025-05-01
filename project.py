from experta import *

class AcademicPerformance(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action=False)


    
    '''
    Paulina Leal Mosqueda
    Welcome the patient.
    '''
    @Rule(Fact(action=False), salience=1)
    def welcome(self):
        print("Welcome to our medical otorhinolaryngologist system. Thank you for choosing us today.")
        print(" ")
        print("We will be giving you some questions. Please answer carefully.")
        print(" ")
        name = input('What is your name? ')
        self.declare(Fact(name = name))
        print(" ")
        print("Hi %s, we will continue with the diagnosis and we'll try to help you as much as possible." % (name)) 
        print(" ")
        self.declare(Fact('name'))
        self.declare(Fact(action=False))
        
        
    '''
    Paulina Leal Mosqueda
    Ask if the patient has a sore throat.
    '''
    @Rule(Fact(action=False),
          NOT(Fact(sore_throat=W())),
          NOT(Fact(disease=W())))
    def ask_sore_throat(self):
        while True:
            answer = input("Do you have a sore throat? ").strip().lower()
            if answer in ('yes', 'no'):
                self.declare(Fact(sore_throat=answer== "yes"))
                print(" ")
                break
            else:
                print(" ")
                print("Please answer with 'yes' or 'no'. ")
                print(" ")
                
    
    
    '''
    Paulina Leal Mosqueda
    Ask if the patient has a ear pain,
    while making sure it doesn't have a sore throat, since it isn't a direct symptom of otitis nor Sinusitis.
    '''
    # Paulina Leal Mosqueda
    @Rule(Fact(action=False),
          Fact(sore_throat=False),
          NOT(Fact(ear_pain=W())),
          NOT(Fact(disease=W())))
    def ask_ear_pain(self):
        while True:
            answer = input("Does your ear hurt? ").strip().lower()
            if answer in ('yes', 'no'):
                self.declare(Fact(ear_pain=answer== "yes"))
                print(" ")
                break
            else:
                print(" ")
                print("Please answer with 'yes' or 'no'. ")
                print(" ")
                
        
    '''
    Paulina Leal Mosqueda
    Ask if the patient has a loss of balance to see if see if it might have otitis.
    If not the system will keep looking for answers.
    '''     
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = True),
          NOT(Fact(loss_balance=W())),
          NOT(Fact(disease=W())))
    def ask_loss_balance(self):
        while True:
            answer = input("Do you have a loss of balance? ").strip().lower()
            if answer in ('yes', 'no'):
                self.declare(Fact(loss_balance=answer== "yes"))
                print(" ")
                break
            else:
                print(" ")
                print("Please answer with 'yes' or 'no'. ")
                print(" ")
    
    
    '''
    Paulina Leal Mosqueda
    Ask if the patient has a runny nose, while making sure that it doesn't have a sore throat or loss of balance.
    This will help to determine if the patient has sinusitis.
    '''  
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = True),
          Fact(loss_balance = False),
          NOT(Fact(runny_nose=W())),
          NOT(Fact(disease=W())))
    def ask_runny_nose(self):
        while True:
            answer = input("Do you have a runny nose with thick yellow or green mucus? ").strip().lower()
            if answer in ('yes', 'no'):
                self.declare(Fact(runny_nose=answer== "yes"))
                print(" ")
                break
            else:
                print(" ")
                print("Please answer with 'yes' or 'no'. ")
                print(" ")
    

    '''
    Paulina Leal Mosqueda
    If the patient has a sore throat, it then has tonsillitis.
    Sore throat implies tonsillitis.
    '''  
    @Rule(Fact(action=False),
          Fact(sore_throat = True),
          NOT(Fact(disease=W())))
    def tonsillitis(self):
        self.declare(Fact(disease = 'tonsillitis'))
        print('You may have tonsillitis, we encourage you to go to the doctor for further examination.')
        print("")
        print('Thank you for choosing us, hopefully you will be getting better soon.')
        print("")
        
    
    '''
    Paulina Leal Mosqueda
    If the patient doesn't have a sore throat and it has ear pain and it has a runny nose, 
    but it doesn't have loss of balance, then the patient might have sinusitis.
    '''
    
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = True),
          Fact(loss_balance = False),
          Fact(runny_nose = True),
          NOT(Fact(disease=W())))
    def sinusitis(self):
        self.declare(Fact(disease = 'sinusitis'))
        print('You might have an inflammation, called Sinusitis.')
        print(" ")
        print('Thank you for choosing us, hopefully you will be getting better soon.')
        print(" ")
        
    '''
    Paulina Leal Mosqueda
    If the patient doesn't have a sore throat and it has ear pain
    then the patient might have sinusitis Acute Otitis Media.
    '''
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = True),
          Fact(loss_balance = True),
          NOT(Fact(disease=W())))
    def otitis(self):
        self.declare(Fact(disease = 'otitis'))
        print('You might have an ear infection, called Acute Otitis Media')
        print(" ")
        print('We recommend you go to the medic to receive attention. Thank you for choosing us, hopefully you will be getting better soon.')
        print(" ")

    '''
    Paulina Leal Mosqueda
    The patient should go to a doctor and check why he has ear pain.
    '''   
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = True),
          Fact(loss_balance = False),
          Fact(runny_nose = False),
          NOT(Fact(disease=W())))
    def inconclusive(self):
        self.declare(Fact(disease = 'inconclusive'))
        print('We apologise, but our database could not find a disease in your current situation. Please go to a doctor for further examination.')
        print(" ")
    
    '''
    Paulina Leal Mosqueda
    Although the patient has no clear symptoms, he should see a doctor to find out what's bothering him.
    '''   
    @Rule(Fact(action=False),
          Fact(sore_throat = False),
          Fact(ear_pain = False),
          NOT(Fact(disease=W())))
    def inconclusive2(self):
        self.declare(Fact(disease = 'inconclusive'))
        print('We apologise, but our database could not find a disease in your current situation. Please go to a doctor for further examination.')
        print(" ")
    
    



engine = AcademicPerformance()

engine.reset()
print(engine.facts)
engine.run()