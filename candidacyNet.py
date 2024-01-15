class CCandidacyNet:
    def __init__(self, kind, sibling=None):
        self.kind=kind
        self.number = 0
        self.optional = -1
        self.candidacy = set()
        self.older = sibling
        self.younger = None
        while not sibling is None:
            if sibling.younger is None:
                sibling.younger = self
                sibling = None
            else:
                sibling = sibling.younger
                if sibling == self.older:
                    # Avoid cyclic generation
                    break

    def getOldest(self):
        oldest = self
        while not oldest.older is None:
            oldest = oldest.older
            if oldest == self:
                return None

        return oldest
    
    def __repr__(self):
        oldest = self.getOldest()
        younger = oldest
        results = []
        while not younger is None:
            results.append("%s(%s,%s)"%(younger.kind,younger.candidacy,younger.optional))
            younger = younger.younger
            if younger == oldest:
                break
        return ".".join(results)

    def findByKind(self,kind):
        result = None
        if self.kind == kind:
            result = self
        checkOlder = self.older
        checkYounger = self.younger
        while not ((checkOlder is None) and (checkYounger is None)):
            if not checkOlder is None:
                if checkOlder.kind == kind:
                    if result is not None:
                        # avoid duplicate kinds
                        return None 
                    result = checkOlder
                checkOlder = checkOlder.older
                if checkOlder == self:
                    # Avoid cyclic generation
                    return None
            if not checkYounger is None:
                if checkYounger.kind == kind:
                    if result is not None:
                        # avoid duplicate kinds
                        return None 
                    result = checkYounger
                checkYounger = checkYounger.younger
                if checkYounger == self:
                    # Avoid cyclic generation
                    return None
        return result
    
    def populate(self, number, optional = -1):
        if (number < 0):
            return False
        if (number == 0) and (optional == 0):
            return False
        self.number = number 
        self.optional = optional
        self.candidacy=set(range(1,self.number+1))
        return True

    def templateFrom(self):
        template = None
        younger = self
        while not younger is None:
            template = CCandidacyNet(younger.kind,template)
            template.populate(younger.number,younger.optional)
            younger = younger.younger
            if younger==self:
                return None
        return template
    
    def getTemplate(self):
        oldest = self.getOldest()
            
        return CCandidacyNet.templateFrom(oldest)
                          
    def setCandidacy(self,attributes):
        value = -1
        if self.kind in attributes.keys():
            value = attributes[self.kind]

        if value > self.number:
            return False
        elif value > 0:
            self.candidacy=set([value])
        elif value < 0:
            self.candidacy=set(range(1,self.number+1))
        elif self.optional != 0:
            self.candidacy=set()
        else:
            return False
        
        return True

    def mimicInstance(self,attributes):
        checkOlder = self.older
        checkYounger = self.younger

        if not self.setCandidacy(attributes):
            return False

        while not ((checkOlder is None) and (checkYounger is None)):
            if not checkOlder is None:

                if not checkOlder.setCandidacy(attributes):
                    return False
                
                checkOlder = checkOlder.older
                if checkOlder == self:
                    # Avoid cyclic generation
                    return False
                
            if not checkYounger is None:

                if not checkYounger.setCandidacy(attributes):
                    return False
                
                checkYounger = checkYounger.younger
                if checkYounger == self:
                    # Avoid cyclic generation
                    return False
                
        return True

def instantiate(net,context,fills,numbers,kinds):
    from clueParserPrinter import parseClues,prependPreamble
    columns = tuple([fills,numbers,kinds])
    _,preamble = prependPreamble(context,columns)

    clues = parseClues(columns,preamble)
    for clue in clues:
        cycle = []
        for instance in clue:
            cycle.append(net.getTemplate())
            attributes = {}
            for value,attribute in instance:
                attributes[attribute]=int(value)
            if  not cycle[-1].mimicInstance(attributes):
                break
        print(cycle)

def main():
    from clueParserPrinter import unparsedCols,parseContext,processContext,prependPreamble
    print("Welcome from Python")
    context = parseContext(unparsedCols)
    fills,numbers,kinds = processContext(context)
    youngest = None
    for o,kind in enumerate(kinds):
        younger = CCandidacyNet(kind,youngest)
        younger.populate(numbers[o],fills[o])
        youngest = younger
    print(youngest)

    instantiate(youngest,context,fills,numbers,kinds)


if __name__=="__main__":
    main()