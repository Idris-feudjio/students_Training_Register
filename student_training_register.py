from random import Random
import json 

DATABASE_PATH = "data.json"
col_widths = [6, 25, 8, 15, 15, 20]
headers = ["##", "Nom", "Genre", "Langage", "Durée(Mois)", "Coût"]

class Student: 
    def __init__(self,id, name,gender): 
        self.id = id
        self.name = name 
        self.gender = gender  
    def get_name(self): 
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def get_gender(self):
        return self.gender
    
    def set_gender(self,gender):
        self.gender=gender
        
    def get_id(self):
        return self.id
        
    def __str__(self):
        return f"Nom : {self.name} -> Genre : {self.gender}"
 
        
class Training: 
    def __init__(self, name, time,cost, id=None):
        self.id = id 
        self.name = name  
        self.time = time  
        self.cost = cost 

        
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def get_time(self):
        return self.time
    
    def set_time(self, time):
        self.time = time
    def get_cost(self):
        return self.cost
    
    def set_cost(self, cost):
        self.cost = cost
        
    def get_id(self):
        return self.id
 
    def __str__(self): 
        return f"Nom : {self.name} -> Durée : {self.time} mois- > Coût : ({self.cost} FCFA)"
    

class TrainingRegister:
    def __init__(self, id, student: Student, training: Training):
        self.id = id
        self.student = student
        self.training = training
        self.hasPayed = False
        
    def __str__(self):
        return f"## : {self.id} -> {self.student} -> {self.training}"
    
    def get_student(self):
        return self.student
    
    def set_student(self, student):
        self.student = student
        
    def get_training(self):
        return self.training
    
    def set_training(self, training):
        self.training = training 
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
        
    def get_hasPayed(self):
        return self.hasPayed
    
    def set_hasPayed(self, hasPayed):
        self.hasPayed = hasPayed
       
class TrainingRegisterManager:
    def __init__(self):
        self.registers = []
        
    def retreive_to_db(self):
        with open(DATABASE_PATH, "r") as f: 
            data = json.load(f) 
        return data["register"]

   
    def save_to_json_db(self, register: TrainingRegister):
        data = {}
        old_data = list(self.retreive_to_db() )
        studentDict = {"id":register.student.get_id(), "Name":register.student.get_name(),"gender":register.student.get_gender()}
        trainingDict = {"id":register.training.get_id(), "Name":register.training.get_name(),"time":register.training.get_time(),"cost":register.training.get_cost()}
        registerDict = {"id":register.get_id(), "student":studentDict,"training":trainingDict}
        old_data.append(registerDict)
        data["register"] = old_data

        with open(DATABASE_PATH, "w") as fichier: 
            json.dump(data, fichier,indent=2) 
            
        
    def remove_register(self, register: TrainingRegister):
        self.registers.remove(register)

    def get_all_registers(self):
        data= list(self.retreive_to_db() )
        listRegister = []
        for register in data:
            student = Student(register["student"]["id"], register["student"]["Name"], register["student"]["gender"])
            training = Training(register["training"]["Name"], register["training"]["time"], register["training"]["cost"], register["training"]["id"])
            training_register = TrainingRegister(register["id"], student, training)
            listRegister.append(training_register)
           # training_register.set_hasPayed(register["hasPayed"])
        return listRegister 

    def find_register_by_student(self, student: Student):
        for register in self.registers:
            if register.get_student() == student:
                return register
        return None

    def find_register_by_training(self, training: Training):
        for register in self.registers:
            if register.get_training() == training:
                return register
        return None 
    
    
def check_user_answer(question="", answer =("Oui","Non","o","n")):
    while True:
        user_input = input(question).strip().lower()
        if user_input in answer:
            return user_input
        else:
            print(f"Reponse invalide. SVP reessayer. Les reponses valides sont: {', '.join(answer)}")
    
def ask_student_info(): 
    # This function asks the user for student information and returns a Student object.
    print()
    studenName = input("Entrer le non de l'etudiant: ")
    print("----")
    studentGender = check_user_answer(question="Entrer le genre de l'étudiant (M/F): ",answer= ("m", "f", "M", "F")) 
    print("----")
    studentId = Random().randint(1000, 9999)
    student = Student(studentId, studenName, studentGender.upper())
    return student  

def get_all_training():
    # This function returns a list of all available training programs.
    trainingList = []
    trainingList.append(Training("Python", 3, 100000, Random().randint(1000, 9999)))
    trainingList.append(Training("Java", 4, 150000, Random().randint(1000, 9999)))
    trainingList.append(Training("C++", 5, 200000, Random().randint(1000, 9999)))
    trainingList.append(Training("JavaScript", 2, 80000, Random().randint(1000, 9999)))
    trainingList.append(Training("HTML/CSS", 1, 50000, Random().randint(1000, 9999)))
    return trainingList


def make_training_register(student: Student, training: Training):
    # This function creates a training register for a student and a training program.
    registerId = Random().randint(1000, 9999)
    register = TrainingRegister(registerId, student, training)
    return register


def display_training_options(trainingList):
    # This function displays the available training programs to the user.
    print("-----------------------------------------------")
    print("PROGRAMME DE FORMATION DISPONIBLE:")
    print("-----------------------------------------------")
    for i, training in enumerate(trainingList):
        print(f"{i + 1}. {training}")
        print("------------")
    print("0. Quit")
    
    
def ask_training_choice(trainingList):
    # This function asks the user to choose a training program from the list.
    while True:
        try:
            choice = int(input("Choisissez un programme de formation (0 to quit): "))
            if 0 <= choice <= len(trainingList):
                return trainingList[choice - 1] if choice > 0 else None
            else:
                print("Choix invalide. Veuillez choisir un nombre entre 0 et", len(trainingList))
        except ValueError:
            print("Mauvais choix. Veuillez entrer un nombre entier.")
 
 
def save_register_to_db(student_register:TrainingRegister):
    # This function saves the training register to the database.
   manager = TrainingRegisterManager()
   manager.save_to_json_db(register=student_register)
   

def associate_student_to_training():
    # This function manages the process of associating a student with a training program.
    while True: 
        student = ask_student_info()
        ask_to_associate_to_training_answer = check_user_answer(question="Voulez-vous l'associer a un programme de formation ? ")
        
        if(ask_to_associate_to_training_answer in ("oui", "o")): 
           trainingList = get_all_training()
           display_training_options(trainingList) 
           training_choice = ask_training_choice(trainingList)
           student_register = make_training_register(student ,training_choice) 
           save_register_to_db(student_register)
        else:
            pass
           
        newStudent = check_user_answer(question="Voulez-vous ajouter un autre étudiant? (Oui/Non): ", answer=("oui", "non", "o", "n"))
        if newStudent in ("non", "n"):
            print()
            print("1. Afficher tous les enregistrements")
            print("-----------------------------")
            print("2. Quitter")
            print()
            user_answer = check_user_answer(question="Choisissez une option (1/2): ", answer=("1", "2"))
            if user_answer == "1":
                 display_all_registers()
                 print()
            elif user_answer == "2":
               break
                
            else:
                print("Choix invalide. Veuillez choisir 1 ou 2.")
            break
        else:
            print("Ajout d'un autre étudiant...")
            print("-----------------------------------------------------")
            print()
            
    
def display_all_registers():
    # This function displays all the training registers in the database.
    print()
    manager = TrainingRegisterManager()
    print("Chargement des enregistrements...")
    try:
        manager.retreive_to_db()
    except FileNotFoundError:
        print("Aucun enregistrement trouvé.")
        return
    
    registers = manager.get_all_registers()
    print("LISTE DES ETUDIANTS ENREGISTRES POUR DES FORMATIONS:")
    print("-------------------------------------") 
    draw_line()
    print_row(headers)
    index = 0
    for register in registers:
        index += 1
        data = [
        index,
        register.student.name,
        register.student.gender,
        register.training.name,
        register.training.time,
        register.training.cost
        ]
        
        draw_line()
        print_row(data)
        if registers.index(register) == len(registers) - 1:
            draw_line()


def draw_line():
    line = "+"
    for width in col_widths:
        line += "-" * width + "+"
    print(line)
    

def print_row(row_data):
    line = "|"
    for i, cell in enumerate(row_data):
        line += f" {str(cell):<{col_widths[i] - 1}}|"
    print(line)

if __name__=="__main__": 
    # This function is the entry point of the program.
    print()
    print("BIENVENUE DANS LE SYSTEME D'ENREGISTREMENT DES ETUDIANTS")
    print("-----------------------------------------------------")
    print("1. Enregistrer un étudiant")
    print("-----------------------------")
    print("2. Afficher tous les enregistrements")
    print()
    user_answer = check_user_answer(question="Choisissez une option (1/2): ", answer=("1", "2"))
    if user_answer == "1":
        associate_student_to_training()
    elif user_answer == "2":
        display_all_registers()
        print()
    else:
        print("Choix invalide. Veuillez choisir 1 ou 2.")
    print("Merci d'avoir utilisé le système d'enregistrement des étudiants. Au revoir!")
    print()
    print("-----------------------------------------------------")
    print()