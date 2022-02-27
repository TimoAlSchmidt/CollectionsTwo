import random

spelerEen = {"Aces" : 0,
            "Twos" : 0,
            "Threes" : 0,
            "Fours" : 0,
            "Fives" : 0,
            "Sixes" : 0,
            "Part1 Bonus" : 0,
            "Three of a kind" : 0,
            "Four of a kind" : 0,
            "Full house" : 0, #3 of a kind + pair
            "Small Straight" : 0, #4 oplopende dobbelstenen
            "Large Straight" : 0, #5 oplopende dobbelstenen
            "Yahtzee" : 0, #Yahtzee
            "Chance" : 0 #Totale score van gooi
            }

combinaties = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "Three of a kind", "Four of a kind", "Full house", "Small Straight", "Large Straight", "Yahtzee", "Chance"]

dobbelstenen = [0,0,0,0,0] #dobbelstenen
dobbelstenen2 = [] #geholden dobbelstenen

gooien = 1
ronde = 0

def gooiDobbelstenen(dobbelstenen):
    for i in range(len(dobbelstenen)):
        dobbelstenen[i] = random.randint(1,6)
    return dobbelstenen


def bepaalCombinaties(dobbelstenen):
    dobbelstenen.sort()
    mogelijkheden = []
    for i in range(6):
        if i+1 in dobbelstenen:
            mogelijkheden.append(combinaties[i])

    dobbelDict = {item:dobbelstenen.count(item) for item in dobbelstenen}
    
    if 3 in dobbelDict.values():
        mogelijkheden.append("Three of a kind")
        if 2 in dobbelDict.values():
            mogelijkheden.append("Full house")

    if 4 in dobbelDict.values():
        mogelijkheden.append("Four of a kind")
    
    if 5 in dobbelDict.values():
        mogelijkheden.append("Yahtzee")

    groei = 0    
    vorige = dobbelstenen[0]
    for i in range(4):
        if vorige+1 == dobbelstenen[i+1]:
            groei += 1
        vorige = dobbelstenen[i+1]
    
    if groei > 2:
        mogelijkheden.append("Small Straight")
    if groei > 3:
        mogelijkheden.append("Large Straight")            
    
    mogelijkheden.append("Chance")
    return mogelijkheden


def verwijderGekozenCombinaties(combi):
    #verwijder combinaties die al gekozen zijn
    combi2 = []
    for combinatie in combi:
        if spelerEen[combinatie] == 0:
            combi2.append(combinatie) # SOMS KRIJGEN WE CHANCE ALS EEN OPTIE OMDAT PYTHON HET GRAPPIG VINDT.
    return combi2

        
def combinatieInvullen(dobbelstenen, combi):
    dobbelDict = {item:dobbelstenen.count(item) for item in dobbelstenen}
    nummer = combinaties.index(combi)+1

    if combi in combinaties[0:6]: #Ones-Sixes
        spelerEen[combi] = dobbelDict[nummer]*nummer
        nummer = 0
        for combi in combinaties[0:6]:
            nummer += spelerEen[combi]
        if nummer >= 63:
            spelerEen["Part1 Bonus"] = 35
            
    
    if combi in combinaties[7:8]: #Three/Four of a kind
            for key, value in dobbelDict.items():
                if value == 3:
                    spelerEen[combi] = key * 3
                if value == 4: # we hebben 4 dobbelstenen
                    spelerEen[combi] = key * 4            

    if combi == "Full house":
        spelerEen[combi] = 25

    if combi in combinaties[9:12]: #Straights + Yahtzee
        spelerEen[combi] = 10 * (nummer-7)     

    if combi == "Chance":
        nummer = 0
        for dobbel in dobbelstenen:
            nummer += dobbel
        spelerEen[combi] = nummer       


def vraagOmSpecifiek(completeVraag, keuzes):
    while True:
        try:
            woord = input(completeVraag+"\n")
            if woord in keuzes:
                return woord
        except: 
            print("Vul alstublieft een correct antwoord in.\n")

while ronde != 13:
    input("Gooi de dobbelstenen ["+str(gooien)+"/3]")

    dobbelstenen = gooiDobbelstenen(dobbelstenen)

    print(dobbelstenen) #print result
    string = " "
    for i in range(len(dobbelstenen)):
        string += str(i+1)+"  "
    print(string)
    if dobbelstenen2:
        print("Geholden dobbelstenen: "+str(dobbelstenen2))

    houdStenen = True
    while houdStenen and gooien != 3 and len(dobbelstenen) > 1:
        try: 
            antwoord = int(input("\nTyp de nummer van de dobbelsteen die u wilt houden of typ een letter om door te gaan"))
            dobbelstenen2.append(dobbelstenen.pop(antwoord-1))
            print("Dobbelstenen: "+str(dobbelstenen))
            string = "               "
            for i in range(len(dobbelstenen)):
                string += str(i+1)+"  "
            print(string)
            print("Geholden dobbelstenen: "+str(dobbelstenen2))
            if len(dobbelstenen) < 2:
                houdStenen = False
        except:
            houdStenen = False

    dobbelstenen3 = dobbelstenen+dobbelstenen2
    print("Mogelijke combinaties:")
    spelerCombinaties = bepaalCombinaties(dobbelstenen3)
    spelerCombinaties = verwijderGekozenCombinaties(spelerCombinaties)
    antwoord = ""
    print(spelerCombinaties)

    if gooien != 3:
        antwoord = vraagOmSpecifiek("Wilt u 1) de dobbelstenen gooien of 2) een combinatie invullen", ("1", "2"))

    if(antwoord == "2" or gooien == 3):
        if not spelerCombinaties:
            print("Je kan geen combinaties invullen.")
        else:
            antwoord = vraagOmSpecifiek(("\nWelke combinatie wilt u invullen?"), spelerCombinaties)
            combinatieInvullen(dobbelstenen3, antwoord)
            gooien = 0
            ronde += 1
            while dobbelstenen2:
                dobbelstenen.append(dobbelstenen2.pop())           
            print("\n"+str(spelerEen)+"\nRonde "+str(ronde)+":\n")


    gooien += 1

totaalScore = 0
for value in spelerEen.values():
    totaalScore += value
print("\n\nTotaal Score: "+str(totaalScore))