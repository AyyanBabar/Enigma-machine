from enigma import *
enigma=Enigma("I II III","B",('A','A','Z'),(1,1,1))
plugs="HL MO AJ CX BZ SR NI YW DG PK"
for i in plugs.split():
    enigma.addLead(i)
print(enigma.encode("helloworld"))

enigma=Enigma("I II III","B",('A','A','Z'),(1,1,1))
plugs="HL MO AJ CX BZ SR NI YW DG PK"
for i in plugs.split():
    enigma.addLead(i)
print(enigma.encode("RFKTMBXVVW"))
