import random

random.seed()

lootjes = {}
loten = []

def vraagOmSpecifiek(completeVraag, keuzes):
    while True:
        try:
            woord = input(completeVraag+"\n")
            if woord in keuzes:
                return woord
        except: 
            print("Vul alstublieft een correct antwoord in.\n")

def vraagOmNaam():
    global lootjes
    antwoord = input("Voer een naam in.\n")
    lootjes.update({antwoord : ''})


flag = True
while flag:
    if len(lootjes) < 2:
        vraagOmNaam()
    else:
        antwoord = vraagOmSpecifiek("Wilt u 1) een naam invullen of 2) lootjes trekken", ("1", "2"))
        if antwoord == "1":
            vraagOmNaam()
        else:
            flag = False
            loten = list(lootjes.keys())
            for lot in loten:
                flag2 = True
                while flag2:
                    antwoord = loten[random.randint(0, len(loten)-1)]
                    if antwoord != lot:
                        flag2 = False
                lootjes[lot] = antwoord

print(lootjes)



