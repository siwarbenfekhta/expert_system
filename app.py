# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import sys
from experta import *
import ast
nom =""
north="" 
temp="" 
rain =""
winter=""
fertil = ""
app = Flask(__name__)
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
        if request.method == 'POST':
            global nom 
            global north 
            global temp 
            global rain 
            global winter 
            global fertil
            nom = request.form['nom']
            north = request.form['north']
            temp = request.form['temp']
            rain = request.form['rain']
            winter = request.form['winter']   
            fertil = request.form['fertil']
            engine = CropExpert()
            engine.reset()
            engine.run()
            print('Les faits enregistrées sont :',cult) 
            return render_template('result.html', prediction=cult , nom=nom)

class CropExpert(KnowledgeEngine):
    username = "", 

    @DefFacts()
    def needed_data(self):
        """ 
        This is a method which is called everytime engine.reset() is called.
        It acts like a constructor to this class.
        """        
        yield Fact(findCulture = 'true')        

    @Rule(Fact(findCulture = 'true'),NOT(Fact(name=W())),salience = 1000)
    def ask_name(self):
        self.username = nom
        self.declare(Fact(name=self.username))

    @Rule(Fact(findCulture='true'), NOT (Fact(north = W())),salience = 995)
    def isNorth(self):
        self.north = north
        self.north = self.north.lower()
        self.declare(Fact(north = self.north.strip().lower()))

    @Rule(Fact(findCulture='true'), NOT (Fact(temp = W())),salience = 985)
    def hasHightemp(self):
        self.temp = temp
        self.temp = self.temp.lower()
        self.declare(Fact(temp = self.temp.strip().lower()))

    @Rule(Fact(findCulture='true'), NOT (Fact(rain = W())),salience = 975)
    def hasrain(self):
        self.rain = rain
        self.rain = self.rain.lower()
        self.declare(Fact(rain = self.rain.strip().lower()))

    @Rule(Fact(findCulture='true'), NOT (Fact(winter = W())),salience = 970)
    def Iswinter(self):
        self.winter = winter
        self.winter = self.winter.lower()
        self.declare(Fact(winter = self.winter.strip().lower()))

    @Rule(Fact(findCulture='true'), NOT (Fact(fertil = W())),salience = 960)
    def Isfertil(self):
        self.fertil = fertil
        self.fertil = self.fertil.lower()
        self.declare(Fact(fertil = self.fertil.strip().lower()))



    @Rule(Fact(findCulture='true'),Fact(north = 'yes'), Fact(temp = 'no'), Fact(rain = 'yes'),Fact(winter = 'yes'),Fact(fertil = 'yes'))
    def culture_0(self):
        self.declare(Fact(culture = 'ble'))

    @Rule(Fact(findCulture='true'),Fact(north = 'no'), Fact(temp = 'yes'), Fact(rain = 'yes'),Fact(winter = 'yes'),Fact(fertil = 'yes'))
    def culture_1(self):
        self.declare(Fact(culture = 'olive'))

    @Rule(Fact(findCulture='true'),Fact(north = 'no'), Fact(temp = 'yes'), Fact(rain = 'no'),Fact(winter = 'no'),Fact(fertil = 'yes'))
    def culture_2(self):
        self.declare(Fact(culture = 'datte'))
    
    @Rule(Fact(findCulture='true'),Fact(north = 'no'), Fact(temp = 'no'), Fact(rain = 'yes'),Fact(winter = 'yes'),Fact(fertil = 'yes'))
    def culture_3(self):
        self.declare(Fact(culture = 'argumes'))

    @Rule(Fact(findCulture='true'),NOT (Fact(culture = W())),salience = -1)
    def unmatched(self):
        self.declare(Fact(culture = 'unknown'))




    @Rule(Fact(findCulture = 'true'),Fact(culture = MATCH.culture),salience = 1)
    def getCulture(self, culture):
        
        if(culture == 'unknown'):
            map = []
            map.append('north')
            map.append('temp')
            map.append('rain')
            map.append('winter')
            map.append('fertil')
            #print('\n\nNous avons vérifié les critères suivants',map)
            map_val=[self.north,self.temp,self.rain,self.winter]
            #print('\n\nles réponses sont:', map_val)
            
            file = open("cultures.txt", "r")
            contents = file.read()
            dictionary = ast.literal_eval(contents)
            file.close()
            
            yes_symptoms = []
            for i in range(0,len(map_val)):
                if map_val[i] == 'yes':
                    yes_symptoms.append(map[i])
            
            max_val = 0
            print('\n\n les critères oui : ', yes_symptoms)
            for key in dictionary.keys():
                val = dictionary[key].split(",")
                count = 0
                print(key,":",val)
                for x in val:
                    if x in yes_symptoms:
                        count+=1
                #print('Count:',count)
                if count > max_val:
                    max_val = count
                    pred_dis = key
            global cult
            if max_val == 0:
                cult = "0"
                print("Pas de culture trouvé.Désolé!")
            else:
 
                cult = "0"+pred_dis
                print("\n\nNou n'avons pas pu déterminer la culture adéquate mais nous pensons que la plus probable est",pred_dis)
                
                print('\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
        else:
            cult = culture
            print('La culture la plus adéquate à cultiver est:',culture)
            print('\n\n')
            print('\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #')

if __name__ == '__main__':

    app.run(debug=True)
   
