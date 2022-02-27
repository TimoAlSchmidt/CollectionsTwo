import random, string, re
random.seed()

class Speler:
    def __init__(self, nummer, links, rechts):
        self.links = links      #wie links is (voor linksDraai)
        self.rechts = rechts    #wie rechts is (voor !linksDraai)
        self.nummer = nummer    #welk nummer hij is
        self.hand = []          #wat hij vast heeft


    def kiesKleur(self):
        handDict = {}
        for kaart in self.hand:
            x = re.search("\w+", kaart)
            if x:
                if x.group() != "Neem" and x.group() != "Keuze": #Neem-4 en Keuze is geen kleur
                    kleur = x.group()
                    try:
                        handDict[kleur] += 1
                    except:
                        handDict.update({kleur : 1})
        
        try: 
            return max(handDict, key=handDict.get)
        except: #Als dit de laatste kaart is, kies de kleur Rood.
            return "Rood" 


    def hebbenWeKaart(self, zoek):
        for kaart in self.hand:
            if zoek in kaart:
                return kaart
            
        return None


    def geefKaart(self, zoek):
        global stapel
        for kaart in self.hand:
            if zoek in kaart:
                print("Speler {} speelt {}! ({})".format(self.nummer, kaart, self.hand))
                if len(self.hand) == 2:
                    print("Speler {}: UNO! ({})".format(self.nummer, self.hand))
                elif len(self.hand) == 1:
                    print("Speler {}: Ik win!".format(self.nummer))
                    self.hand.pop(self.hand.index(kaart))
                    return
                return stapel.neemKaart(self.hand.pop(self.hand.index(kaart)))


    def pakEenKaart(self):
        global deck
        global stapel
        kaart = ""
        try: 
            kaart = deck.pop(0)
        except:
            print("Stapel wordt ge-reshuffled!")
            deck = stapel.hand[0:-1] #Pak elke kaart behalve de bovenste
            random.shuffle(deck)
            kaart = deck.pop(0)
    
        #verwijder kleur van keuze/neem-vier kaarten.
        if "Keuze" in kaart:
            kaart = "Keuze kaart"
        if "Neem-vier" in kaart:
            kaart = "Neem-vier kaart"
        self.hand.append(kaart)
        print("Speler {} pakt kaart {}".format(self.nummer, kaart))


    def speelKaart(self):
        global stapel
        global speciaal
        nummer = stapel.nummer
        kleur = stapel.kleur
        kaart = stapel.kaart
        liefsteKleur = self.kiesKleur()

        hand = self.hand


        
        #Kijk of dat we keuze kaart hebben
        geef = self.hebbenWeKaart("Keuze")
        if geef:
            return self.geefKaart(geef)
        
        #Als we dat niet hebben, kijk of dat we de kleur hebben
        geef = self.hebbenWeKaart(kleur)
        hebbenKleur = False
        if geef:
            hebbenKleur = True
        else:
            #Als we de kleur niet hebben, kijk of dat we neem-4 hebben.
            geef = self.hebbenWeKaart("Neem-vier")
            if geef:
                print("Er is een neem-vier gespeelt!\n \"{}\", {}\n{}".format(kleur, kaart, self.hand))
                return self.geefKaart(geef)


        #Als we geen kaart hebben gespeelt, kijk of dat de kaart neem-twee/keer-om/sla-beurt is        
        for spec in speciaal[0:3]:
            if spec in kaart:
                geef = self.hebbenWeKaart(spec)
                if geef:
                    return self.geefKaart(geef)

        #Als de kaart dat niet is:
        if hebbenKleur:
            # A) Speel de hoogste nummer met de kleur die we hebben
            hand.sort()
            hand.reverse()
            geef = self.hebbenWeKaart(kleur)
            if geef:
                return self.geefKaart(geef)
        else:
            # B) Kijk of dat we het nummer hebben
            geef = self.hebbenWeKaart(nummer)
            if geef:
                return self.geefKaart(geef)

        self.pakEenKaart()
        stapel.neemKaart(None)



class Stapel:
    def __init__(self):
        self.hand = []
        self.linksDraai = True
        self.hoeveelheidSpelers = -1
        self.volgendeBeurt = -1
        self.kaart = ""
        self.kleur = ""
        self.nummer = ""
       

    def beurtVooruit(self):
        if self.linksDraai:
            if self.volgendeBeurt+1 > self.hoeveelheidSpelers:
                self.volgendeBeurt = 1
            else:
                self.volgendeBeurt += 1
        else:
            if self.volgendeBeurt-1 < 1:
                self.volgendeBeurt = self.hoeveelheidSpelers
            else:
                self.volgendeBeurt -= 1
        

    def neemKaart(self, kaart):
        global spelers
        if kaart:

            if "Keuze" in kaart:
                kleur = spelers[self.volgendeBeurt].kiesKleur()
                print("Speler {} kiest voor kleur {}.".format(self.volgendeBeurt+1, kleur))
                kaart = kleur + " Keuze kaart"

            if "vier" in kaart:
                kleur = spelers[self.volgendeBeurt].kiesKleur()
                print("Speler {} kiest voor kleur {}.".format(self.volgendeBeurt+1, kleur))
                kaart = kleur + " Neem-vier kaart"

            self.hand.append(kaart)

            kler = re.search("\w+", kaart).group() #eerste woord

            self.kleur = kler
            
            numr = re.search("\d", kaart) #eerste getal [0-9]
            if numr: #als we een nummer vinden
                self.nummer = numr.group()
            
            self.kaart = kaart

            if "Sla-beurt-over" in kaart:
                print("Stapel: Speler {} slaat zijn beurt over!".format(self.volgendeBeurt + (int(self.linksDraai)*2)))
                self.beurtVooruit()
            
            if "Neem" in kaart:
                self.beurtVooruit()
                if "twee" in kaart:
                    print("Stapel: Speler {} moet twee kaarten pakken!".format(self.volgendeBeurt+1))
                    for i in range(2):
                        spelers[self.volgendeBeurt].pakEenKaart()
                else:
                    print("Stapel: Speler {} moet vier kaarten pakken!".format(self.volgendeBeurt+1))
                    for i in range(4):
                        spelers[self.volgendeBeurt].pakEenKaart()
            
            if "Keer" in kaart:
                self.linksDraai = not self.linksDraai
                print("Stapel: linksdraai is nu {}".format(self.linksDraai))
        

        self.beurtVooruit()
        print("Stapel: Speler {} is nu aan de beurt. ({})".format(self.volgendeBeurt+1, self.hand[-1]))
        spelers[self.volgendeBeurt].speelKaart()



kleuren = ["Blauw", "Rood", "Groen", "Geel"]
speciaal = ["Neem-twee kaart", "Keer-om kaart", "Sla-beurt-over kaart","Keuze kaart","Neem-vier kaart"]
deck = []
stapel = Stapel()
spelers = []
score = []

hoogsteScore = 0

def vraagOmSpelers():
    while True:
        try:
            nummer = int(input("Hoeveel spelers? (2-10)\n"))
            if nummer >= 2 and nummer <= 10:
                return nummer
            else:
                print("Vul alstublieft een nummer tussen 2 en 10 in.")
        except:
            print("Vul alstublieft een nummer in.") 


def voegKaartenAanDeck():
    deck = []
    for kleur in kleuren: #voeg bl/ro/gr/ge 0-9 *2 toe
        for i in range(2):
            for digit in string.digits:
                deck.append(kleur+" "+digit+" kaart")

    for kleur in kleuren: #0 kaart komt maar 1* voor in de deck
        deck.remove(kleur+" 0 kaart") 

    for i in range(3): #voeg 2* kleur van Neem-twee, keer-om en sla-beut-over kaarten.
        for n in range(2):
            for kleur in kleuren:
                deck.append(kleur+" "+speciaal[i])

    for spec in speciaal: #voeg 4 van keuze en neem-vier
        if spec == "Keuze kaart" or spec == "Neem-vier kaart":
            for i in range(4):
                deck.append(spec)

    
    
    random.shuffle(deck)
    
    return deck 
 

deck = voegKaartenAanDeck()
antwoord = vraagOmSpelers()


for i in range(antwoord): #voeg spelers toe met leeg hand
    if i == 0:
        spelers.append(Speler(i+1, antwoord, i+2))
    elif i != antwoord-1:
        spelers.append(Speler(i+1, i, i+2))
    else:
        spelers.append(Speler(i+1, i, 1))

stapel.hoeveelheidSpelers = antwoord-1


while hoogsteScore < 500:

    for speler in spelers: #pak een kaart voor het begin
        speler.pakEenKaart()
        score.append(0)


    nummers = []
    for speler in spelers:
        x = re.search("\d", speler.hand[0])
        try:
            nummers.append(int(x.group()))
        except: 
            nummers.append(0)


    #Beslis welke speler eerst begint
    start = 0
    nummer = 0
    for i in range(len(nummers)):
        if nummers[i] > nummer:
            start = i-1 #Degene links van deze in list
            nummer = nummers[i]

    print("\n\nStart-Speler: "+str(start+1))

    #elke speler krijgt 7 kaarten (6 meer)
    for speler in spelers:
        for i in range(6):
            speler.pakEenKaart()

    stapel.volgendeBeurt = start

    stapel.hand.append(deck.pop(0))


    print("\n\n\nSTART! ({})".format(stapel.hand[-1]))


    #check of dat hij niet neem-4 is (die mag niet bovenaan)
    while stapel.hand[-1] == "Neem-vier kaart":
        deck.append(stapel.hand.pop(0))
        stapel.hand.append(deck.pop(0))


    #Start het spel
    stapel.neemKaart(stapel.hand.pop())

    scoreOmhoog = 0
    winnaar = stapel.volgendeBeurt
    for speler in spelers:
        #geef punten aan de winnaar
        spelerScore = 0
        if speler.nummer != winnaar:
            for kaart in speler.hand:
                if "Neem-vier" in kaart or "Keuze" in kaart:
                    spelerScore += 50
                elif "Sla-beurt-over" in kaart or "Keer-om" in kaart or "Neem-twee" in kaart:
                    spelerScore += 20
                else:
                    numr = re.search("\d", kaart) #eerste getal [0-9]
                    if numr: #als we een nummer vinden
                        spelerScore += int(numr.group())
            scoreOmhoog += spelerScore
    
    score[winnaar] += scoreOmhoog
    hoogsteScore = max(hoogsteScore, score[winnaar])

    print("\nWinnaar {}: {} (+{})\n\n".format(winnaar+1, score[winnaar], scoreOmhoog))

            



print("\nEind resultaat:\n\n")
for speler in spelers:
    print(str(speler.nummer)+": "+str(speler.hand))