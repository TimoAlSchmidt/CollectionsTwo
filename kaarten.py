import random

random.seed() 

kleuren = ["harten", "klaveren", "schoppen", "ruiten"]
kaarten = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "boer", "vrouw", "heer", "aas"]
deck = ["joker", "joker"]

for kleur in kleuren:
    for kaart in kaarten:
        deck.append(kleur + " " + kaart)

random.shuffle(deck)

for i in range(7):
    print("kaart "+str(i+1)+": "+str(deck[0]))
    deck.pop(0)

print("\ndeck ("+str(len(deck))+" kaarten): "+str(deck))
