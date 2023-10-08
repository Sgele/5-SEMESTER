import openpyxl
import pandas as pd
import numpy as np
import random
import math
from sklearn.model_selection import train_test_split


#nuskaitome irisu duomenis
irisai = pd.read_excel('/Users/simonagelzinyte/Documents/Duomenų mokslas/5 semestras/AI/iris.xlsx', header = None)
irisai.columns = ["x1", "x2", "x3", "x4", "klase"]

# b - bias -  visa laika - 1
irisai["b"] = 1

irisaix_mok, irisaix_test, irisaiy_mok, irisaiy_test = train_test_split(
    np.array(irisai.loc[:, irisai.columns != "klase"]),
    np.array(irisai.loc[:, irisai.columns == "klase"]),
    test_size = 0.2, random_state = 2)

#print(irisu_duomenys)
#nuskaitome kruties vezio duomenis
kruties_vezio_duomenys = pd.read_excel('/Users/simonagelzinyte/Documents/Duomenų mokslas/5 semestras/AI/breast-cancer-wisconsin.xlsx')
#print(kruties_vezio_duomenys)

#shuffled = irisu_duomenys.sample(frac=1)
#result = np.array_split(shuffled, 2)
#for part in result:
#    print(part,'\n')
#Dalijam duomenu aibes i mokymo ir testavimo
#Susikuriam irisu mokymo aibe (80% duomenu)
#irisu_mokymo_aibe = irisu_duomenys.sample(frac=0.8)

#Susikuriam irisu testavimo aibe (20% duomenu)
#print(len(irisu_duomenys.index))
#irisu_testavimo_aibe = irisu_duomenys.drop(irisu_mokymo_aibe.index)

#print("\nirisu mokymo aibe: ")
#print(irisu_mokymo_aibe)
#irisu_mokymo_aibe = irisu_mokymo_aibe.to_numpy()
#print('\nirisu mokymo masyvas: \n',irisu_mokymo_aibe)

#print("\nirisu testavimo aibe: ")
#print(irisu_testavimo_aibe)
#irisu_testavimo_aibe = irisu_testavimo_aibe.to_numpy()
#print('\nirisu testavimo masyvas: \n',irisu_testavimo_aibe)

#Vezio kruties duomenu aibe
#Susikuriam kruties vezio mokymo aibe (80% duomenu)
kruties_vezio_mokymo_aibe = kruties_vezio_duomenys.sample(frac=0.8)

#Susikuriam kruties vezio testavimo aibe (20% duomenu)
kruties_vezio_testavimo_aibe = kruties_vezio_duomenys.drop(kruties_vezio_mokymo_aibe.index)

#print("\nvezio mokymo aibe: ")
#print(kruties_vezio_mokymo_aibe)
kruties_vezio_mokymo_aibe = kruties_vezio_mokymo_aibe.to_numpy()
print('\nkruties vezio mokymo masyvas: \n', kruties_vezio_mokymo_aibe)

#print("\nvezio testavimo aibe: ")
#print(kruties_vezio_testavimo_aibe)
kruties_vezio_testavimo_aibe = kruties_vezio_testavimo_aibe.to_numpy()
print('\nkruties vezio testavimo masyvas: \n', kruties_vezio_testavimo_aibe)

#Slenkstine aktyvacijos funkcija

#norimos reiksmes - t_i
#isejimo reiksmes - y
def nauji_svoriai(svoriai, eilute, y_i, t_i, mokymo_greitis):
    # Svorių koregavimas
    nauji_svoriai = []
    for i in range(len(svoriai)):
        nauji_svoriai.append(svoriai[i] + mokymo_greitis*(t_i - y_i)*eilute[i])
    return nauji_svoriai

def slenkstine_fja(eilute, svoriai):
    a = np.dot(eilute, svoriai)
    if a >= 0:
        return 1
    return 0

def mokymo_slenkstine(mokymo_greitis, epochos, irisaix_mok, irisaiy_mok):
    # Mokymo funkcija
    svoriai = [0.5, 0.5, 0.5, 0.5, 0.5]
    errors = []  # klaidu skaiciavimas
    for e in range(epochos):
        errorssum = 0 # klaidu skaiciavimas
        for i in range(len(irisaix_mok)):
            y = slenkstine_fja(irisaix_mok[i], svoriai)
            eilute = irisaix_mok[i]
            rezultatas = irisaiy_mok[i]
            svoriai = nauji_svoriai(svoriai, eilute, y, rezultatas, mokymo_greitis)

            errorssum += (rezultatas - y) ** 2  # error calculation

        errors.append([e, (0.5 * errorssum)[0]])  # error calculation
    #plot_error(pd.DataFrame(errors, columns = ["epochos", "error"]), "Binary error graph")
    return (svoriai, errors[-1][1])

def testavimo_slenkstine(svoriai, irisaix_test, irisaiy_test):
    success = 0
    for i in range(len(irisaix_test)):
        if slenkstine_fja(irisaix_test[i], svoriai) == irisaiy_test[i][0]:
            success +=1
    return success/len(irisaix_test)



onebinary = mokymo_slenkstine(1, 35, irisaix_mok, irisaiy_mok)
print("Final weights:", [round(i[0],4) for i in onebinary[0]], " ",
      "Final error:", onebinary[1],
      "Accuracy:", testavimo_slenkstine(onebinary[0], irisaix_test, irisaiy_test))

