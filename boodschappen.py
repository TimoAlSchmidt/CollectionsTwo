boodschappen = {}

while True:
    antwoord = input("Wilt u een item aan het lijstje toe voegen? (Y/N)\n")
    if antwoord == "Y":
        antwoord = input("Welk item wilt u toevoegen?\n")
        try:
            boodschappen[antwoord] += 1
        except:
            boodschappen.update({antwoord : 1})
    elif antwoord == "N":
        print(boodschappen)
        input()
        quit()
