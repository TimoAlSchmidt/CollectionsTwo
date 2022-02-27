import random, string

random.seed()
speciale = ["@", "#", "$", "%", "&", "_", "?"]
wachtwoord = ""

for i in range(random.randint(2, 6)): # 2 tot 6 hoofdletters
    wachtwoord += random.choice(string.ascii_uppercase)

for i in range(3): # 3 speciale tekens uit de volgende reeks: @ # $ % & _ ?.
    wachtwoord += random.choice(speciale) 

for i in range(random.randint(4,7)):
    wachtwoord += random.choice(string.digits)

for i in range(24-len(wachtwoord)):
    wachtwoord += random.choice(string.ascii_lowercase)


wachtwoord2 = list(wachtwoord)
flag = True
print("preshuffle: \n"+wachtwoord)


while flag:
    print(wachtwoord2)
    random.shuffle(wachtwoord2)
    flag = False
    
    # De speciale tekens mogen niet op de eerste of laatste positie staan en ook niet op een vaste plek.
    if wachtwoord2[0] in speciale:
        flag = True
    if wachtwoord2[-1] in speciale:
        flag = True
    
    # Op de eerste 3 posities mag geen cijfer staan.
    for i in range(3):
        if wachtwoord2[i] in string.digits:
            flag = True

wachtwoord = ''.join(wachtwoord2)

print(wachtwoord)