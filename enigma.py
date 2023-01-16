
class PlugLead:
    def __init__(self, mapping):
        if len(mapping)!=2 or mapping[0]==mapping[1]:
          raise ValueError
        self.store={}
        self.store[mapping[0]]=mapping[1]
        self.store[mapping[1]]=mapping[0]
    def encode(self, character):
        return self.store.get(character,character)

class Plugboard:
    def __init__(self):
        self.store=[]
    def add(self,lead):
        self.store.append(lead)
    def encode(self, character):
        for i in self.store:
            temp=i.encode(character)
            if temp != character:
                return temp
        return character
    
    
def limitA_Z(i):
    if i<65:
        i=i+26
    elif i>90:
        i=i-26
    return i


class Rotor:
    #ord() char()
    def __init__(self,code:str,pos=1,ringset=1,notch=None):
        self.code=code
        self.pos=pos
        self.ringset=ringset
        self.notch=notch
    def encode_right_to_left(self,inp):
        inp=ord(inp)+self.pos-self.ringset
        inp=limitA_Z(inp)
        temp=ord(self.code[inp-65])
        
        temp=temp-self.pos+self.ringset
        temp=limitA_Z(temp)
        tmp=chr(temp)
        
        return chr(temp)
    def encode_left_to_right(self,inp):
        inp=ord(inp)+self.pos-self.ringset
        
        inp=limitA_Z(inp)
        temp=self.code.index(chr(inp))+65
        temp=temp-self.pos+self.ringset
        temp=limitA_Z(temp)
        tmp=chr(temp)
        return chr(temp)
    def rotate(self):
        temp= (self.pos==self.notch)
        self.pos=(self.pos%26)+1
        return temp
    def on_notch(self):
        return (self.pos==self.notch)
        
def rotor_from_name(inp,pos=1,ringset=1):
    if inp=="I":
        return Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ",pos,ringset,17)
    elif inp=="II":
        return Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE",pos,ringset,5)
    elif inp=="III":
        return Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO",pos,ringset,22)
    elif inp=="IV":
        return Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB",pos,ringset,10)
    elif inp=="V":
        return Rotor("VZBRGITYUPSDNHLXAWMJQOFECK",pos,ringset,26)
    elif inp=="A":
        return Rotor("EJMZALYXVBWFCRQUONTSPIKHGD",pos,ringset)
    elif inp=="B":
        return Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT",pos,ringset)
    elif inp=="C":
        return Rotor("FVPJIAOYEDRZXWGCTKUQSBNMHL",pos,ringset)
    elif inp=="D":
        return Rotor("ABCDEFGHIJKLMNOPQRSTUVWXYZ",pos,ringset)
    elif inp=="Beta":
        return Rotor("LEYJVCNIXWPBQMDRTAKZGFUHOS",pos,ringset)
    elif inp=="Gamma":
        return Rotor("FSOKANUERHMBTIYCWLQPZXVGJD",pos,ringset)
class Enigma:
    def __init__(self,rotors,reflector,pos,ringset,alph=True):
        if len(rotors.split()) != len(pos) or len(rotors.split()) != len(ringset):
            raise ValueError
        self.rotors=[]
        if alph:            
            pos=tuple(map(lambda x:(ord(x.upper())-64),pos))
        for i,j in enumerate(rotors.split()):
            self.rotors.append(rotor_from_name(j,pos[i],ringset[i]))
        self.reflector=rotor_from_name(reflector)
        self.plugboard=Plugboard()
    def enter(self,inp):
        #step1
        onNotch=self.rotors[-2].on_notch()
        for i in (self.rotors[::-1])[:3]:
            if not (i.rotate()):
                break
        if onNotch:#double step
            self.rotors[-2].rotate()
            self.rotors[-3].rotate()
        temp=self.plugboard.encode(inp)
        for rotor in self.rotors[::-1]:
            temp=rotor.encode_right_to_left(temp)
        #step2
        temp=self.reflector.encode_right_to_left(temp)
        #step3
        for rotor in self.rotors:
            temp=rotor.encode_left_to_right(temp)
        
        return self.plugboard.encode(temp)
    def addLead(self,lead):
        self.plugboard.add(PlugLead(lead))
    def encode(self,inp):
        ret=""
        inp=inp.upper()
        for i in inp:
            ret+=self.enter(i)
        return ret    

