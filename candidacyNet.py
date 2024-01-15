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

    def __repr__(self):
        return "%s,%s,%s"%(self.kind,self.candidacy,self.optional)

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
            template = CCandidacyNet(younger.kind,None)
            template.populate(younger.number,younger.optional)
            younger = younger.younger
            if younger==self:
                return None
        return template
    
    def getTemplate(self):
        oldest = self
        while not self.older is None:
            older = self.older
            if oldest == self:
                return None
            
        return CCandidacyNet.templateFrom(oldest)
                          
    def setCandidacy(self,instance):
        value = -1
        if self.kind in instance.keys():
            value = instance[self.kind]

        if value > self.number:
            return False
        elif value > 0:
            self.candidacy=set(value)
        elif value < 0:
            self.candidacy=set(range(1,self.number+1))
        elif self.optional != 0:
            self.candidacy=set()
        else:
            return False
        
        return True

    def mimicInstance(self,instance):
        checkOlder = self.older
        checkYounger = self.younger

        if not self.setCandidacy(instance):
            return False

        while not ((checkOlder is None) and (checkYounger is None)):
            if not checkOlder is None:

                if not checkOlder.setCandidacy(instance):
                    return False
                
                checkOlder = checkOlder.older
                if checkOlder == self:
                    # Avoid cyclic generation
                    return False
                
            if not checkYounger is None:

                if not checkYounger.setCandidacy(instance):
                    return False
                
                checkYounger = checkYounger.younger
                if checkYounger == self:
                    # Avoid cyclic generation
                    return False
                
        return True
    
def main():
    from clueParserPrinter import unparsedCols,parseContext,processContext,prependPreamble
    print("Welcome from Python")
    context = parseContext(unparsedCols)
    fills,numbers,kinds = processContext(context)
    instances = {kind:number for kind,number in zip(kinds,numbers)}
    youngest = None
    for o,kind in enumerate(kinds):
        younger = CCandidacyNet(kind,youngest)
        younger.populate(numbers[o],fills[o])
        youngest = younger
    if youngest is not None:
        for kind in kinds:
            print(youngest.findByKind(kind))


if __name__=="__main__":
    main()