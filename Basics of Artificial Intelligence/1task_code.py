import random
import math

#surasome turimus duomenis
duomenys = [[-0.3, 0.6, 0],
           [0.3, -0.6, 0],
           [1.2, -1.2, 1],
           [1.2, 1.2, 1]]

#Slenkstine aktyvacijos funkcija
def slenkstine_fja(w0, w1, x1, w2, x2):
    a = w1 * x1 + w2 * x2 + w0
    if a >= 0:
        return 1
    return 0

#Sigmoidine aktyvacijos funkcija
def sigmoidine_fja(w0, w1, x1, w2, x2):
    a = w1 * x1 + w2 * x2 + w0
    fa = 1 / (1 + math.exp(-a))
    if fa >= 0.5:
        return 1
    return 0

#atsitiktiniu skaiciu generavimas
def skaiciu_generavimas():
    w0 = round(random.uniform(-10, 10), 2)
    w1 = round(random.uniform(-10, 10), 2)
    w2 = round(random.uniform(-10, 10), 2)
    return w0, w1, w2

#atsitiktinai generuojame skaiciu 1000 kartu
for n in range(1, 1000):
    slenkstinei_fjai = []
    sigmoidinei_fjai = []
    geri_slenkst = []
    w0, w1, w2 = skaiciu_generavimas()
    for i in duomenys:
        a_slenkst = slenkstine_fja(w0, w1, i[0], w2, i[1])
        slenkstinei_fjai.append(a_slenkst)
        #tikriname gautos klases sutampa, jeigu taip - isvedami gautos svorius i ekrana
        if slenkstinei_fjai == [duomenys[0][2] ,duomenys[1][2], duomenys[2][2], duomenys[3][2]]:
            print(f"Slenkstines fjos gauti svoriai {w0}, {w1}, {w2}")
    for i in duomenys:
        a_sigmoid = sigmoidine_fja(w0, w1, i[0], w2, i[2])
        sigmoidinei_fjai.append(a_sigmoid)
    if sigmoidinei_fjai ==  [duomenys[0][2] ,duomenys[1][2], duomenys[2][2], duomenys[3][2]]:
            print(f"Sigmoidines fjos gauti svoriai {w0}, {w1}, {w2}")

