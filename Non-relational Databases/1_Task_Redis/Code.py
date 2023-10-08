import redis

r = redis.Redis(host='localhost', port=6379)
r.flushdb()

def pridetiDB(r, pard_id, prek_id, kiek, sold):
    r.hset(f'{pard_id}:{prek_id}', 'likutis', kiek) # sudetinis raktas, pard_id ir prek_id
    r.hset(f'{pard_id}:{prek_id}', 'parduota', sold)
    return None

def patikrintiLikuti(r, pard_id, prek_id):
    raktas = f'{pard_id}:{prek_id}'
    likutis = r.hget(raktas, "likutis")
    likutis = int(likutis.decode('utf-8'))
    print(f'Prekės {prek_id} likutis parduotuvėje {pard_id} yra {likutis} vnt.')
    return None

def parduotuKiekis(r, pard_id, prek_id):
    raktas = f'{pard_id}:{prek_id}'
    parduota = r.hget(raktas, 'parduota')
    parduota = int(parduota.decode('utf-8'))
    print(f'Parduotuvėje {pard_id} parduotų prekių {prek_id} kiekis yra {parduota} vnt.')
    return None

def pirkti(r, pard_id, prek_id, kiekis):
    with r.pipeline() as pipe:
        raktas = f'{pard_id}:{prek_id}'
        pipe.watch(raktas)
        likutis = r.hget(raktas, "likutis")
        likutis = int(likutis.decode("utf-8"))
        if likutis - kiekis >= 0:
            pipe.multi()
            pipe.hincrby(raktas, "likutis", -kiekis)
            pipe.hincrby(raktas, "parduota", kiekis)
            pipe.execute()
        else:
            pipe.unwatch()
            print(f"Prekės {prek_id} likutis parduotuvėje {pard_id} nepakankamas")
    return None



print("Įrašykite kiek skirtingų prekių norėsite įvesti: ")
sk = int(input())
print("Įveskite parduotuvės id: ")
pard_id = input()

while sk > 0:
        print("Įveskite prekės id: ")
        prek_id = input()
        print("Įveskite prekės kiekį (sveikieji skaičiai): ")
        kiekis = int(input())
        pridetiDB(r, pard_id, prek_id, kiekis, 0)
        print(f"Kiek vienetų norėtumėte nusipirkti prekės {prek_id}? ")
        kiek = int(input())
        pirkti(r, pard_id, prek_id, kiek)
        patikrintiLikuti(r, pard_id, prek_id)
        parduotuKiekis(r, pard_id, prek_id)
        print("Jeigu norėtumėte dar kartą pirkti tą pačią prekę, įrašykite 'T': ")
        x = input()
        while x == 'T' or x == 't':
            print(f"Kiek vienetų norėtumėte nusipirkti prekės {prek_id}? ")
            kiek = int(input())
            pirkti(r, pard_id, prek_id, kiek)
            patikrintiLikuti(r, pard_id, prek_id)
            parduotuKiekis(r, pard_id, prek_id)
            print("Jeigu norėtumėte toliau vykdyti pirkimą įrašykit 'T': ")
            x = input()
            if x == 'T' or x == 't':
                continue
        sk = sk - 1

















