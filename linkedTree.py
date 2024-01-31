class CLinkedTree:
    def __iter__(self):
        sibling = self.oldest
        while sibling:
            yield sibling
            if self.recurse:
                for recurse in self.recurse:
                    yield recurse
            sibling = sibling.younger

        return

    def __init__(self, sibling=None,*recurse, **kwargs):
        self.recurse = recurse
        self.payload = ({**kwargs} if kwargs else dict())
        if sibling is None:
            self.oldest = self
            self.younger = None
        else:
            self.oldest = sibling.oldest
            self.younger = sibling.younger
            sibling.younger = self

    def __repr__(self):
        return "[%s{%i}]"%(str(self.payload),len(self.recurse))

def readTape(delimiters, tape, pos=0, delimiter = ''):
    assert (pos>=len(tape) or tape[pos] in delimiters.values()),"illegal start"
    payloads = []

    pos+=len(delimiter)
    lastpos = pos
    while pos<len(tape):
        c=tape[pos]
        if c in delimiters.values() and not (c == delimiter):
            if pos>lastpos:
                payload=tape[lastpos:pos]
                payloads.append(payload)
                lastpos = pos
            pos,recurse = readTape(delimiters,tape, pos, delimiter = c)
            assert pos<len(tape),"Unmatched delimiter"
            assert (tape[pos] in delimiters),"Unmatched delimiter"
            assert (delimiters[tape[pos]] == c),"Unmatched delimiter"
            payloads.append(recurse)
        elif c in delimiters.keys():
            assert (delimiter == delimiters[c]),"Unmatched delimiter"
            payload=tape[lastpos:pos]
            payloads.append(payload)
            return (pos,payloads)
        
        pos += 1

    payload=tape[lastpos:pos]
    payloads.append(payload)
    return (pos,payloads)

def embody(*args):
    pos = 0
    recurse = []
    while pos < len(args):
        if type(args[pos]) == type([]):
            recurse = args[pos]
        else:
            if recurse:
                result = CLinkedTree(None,*recurse,**{'meta':args[pos]})
                print(result)
            else:
                result = CLinkedTree(None,**{'meta':args[pos]})
                print(result)
            recurse = []
        pos+=1
    return recurse

def main():
    print("Welcome from Python")
    delimiters = { closer:opener for opener,closer in zip("{(<#","})>#") }
    tape = "<1#Hydroxyapatite#>{Ca10(PO4)6(OH)2}"
    pos,payloads = readTape(delimiters,tape)
    if pos == len(tape):
        print(payloads)
        embody(*payloads)

    linkedTree = None
    for id in range(10):
        linkedTree = CLinkedTree(linkedTree,**{'id':id})
    for shoot in linkedTree:
        pass #print(shoot)

if __name__=="__main__":
    main()