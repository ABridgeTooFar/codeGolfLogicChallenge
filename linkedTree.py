class CLinkedTree:
    def __iter__(self):
        sibling = self
        while sibling:
            yield sibling
            recurse = self.descendent
            if recurse and recurse.oldest:
                for descendent in recurse.oldest:
                    yield descendent
            sibling = sibling.younger
        return None

    def __init__(self, sibling=None, **kwargs):
        self.descendent = None
        self.payload = kwargs
        if sibling is None:
            self.oldest = self
            self.younger = None
        else:
            self.oldest = sibling.oldest
            self.younger = None
            adoptee=sibling.younger
            self.descendent = adoptee
            while adoptee:
                adoptee.oldest = sibling.younger
                adoptee = adoptee.younger
            sibling.younger = self

    def __repr__(self):
        results = []
        for i in self.oldest:
            results.append("%i"%(len(results)))
            if i.payload:
                results[-1]+=":(%s)"%(",".join(i.payload.keys()))
        
        return "["+",".join(results)+"]"


def generatePayload(delimiters, tape, pos=0, delimiter = '', shoot = None):
    assert (pos>=len(tape) or tape[pos].isupper()),"illegal start"

    parent = shoot
    lastpos = pos
    pos = pos + 1
    while pos<len(tape):
        c=tape[pos]
        #print(c)
        if c.isupper():
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            shoot = CLinkedTree(shoot,**payload)
            #print(shoot.payload)
            lastpos = pos
            pos += 1
        elif c in delimiters.keys():
            assert (delimiter == delimiters[c]),"Unmatched delimiter"
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            shoot = CLinkedTree(shoot,**payload)
            #print(shoot.payload)
            return (parent,shoot)
        elif c in delimiters.values():
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            shoot = CLinkedTree(shoot,**payload)
            lastpos = pos
            foster,shoot = generatePayload(delimiters,tape, pos + 1, delimiter = c, shoot = shoot)
            pos = shoot.payload['pos']+len(shoot.payload['key'])
            assert pos<len(tape),"Unmatched delimiter"
            assert (tape[pos] in delimiters),"Unmatched delimiter"
            assert (delimiters[tape[pos]] == c),"Unmatched delimiter"
            pos += 1
            #shoot = foster
        else:
            pos += 1

    payload={'pos':-1, 'key':tape[lastpos:pos]}
    shoot =  CLinkedTree(shoot,**payload)
    #print(shoot.payload)

    return (parent,shoot)

def main():
    #delimiters = { closer:opener for opener,closer in zip("(",")") }
    delimiters = { closer:opener for opener,closer in zip("{([","})]") }
    print(delimiters)
    tape = "Hydroxyapatite{Ca10(PO4)6(OH)2}"
    _,linkedTree = generatePayload(delimiters,tape)
    for shoot in linkedTree.oldest:
        print(shoot.payload)


if __name__=="__main__":
    main()