class CCandidacyNet:
    def forAllSiblings(self,process,*args):
        looped = [None]
        sibling = self
        while not (sibling in looped):
            args = process(sibling,*args)
            sibling = sibling.younger
        sibling = self.older
        while not (sibling in looped):
            args = process(sibling,*args)
            sibling = sibling.older

        return args
    
    def __init__(self, kind, sibling=None):
        self.kind=kind
        self.number = 0
        self.optional = -1
        self.candidacy = set()
        self.older = sibling
        self.younger = None
        while not (sibling is None):
            if sibling.younger is None:
                sibling.younger = self
                sibling = None
                break
            else:
                sibling = sibling.younger

    def getOldest(self):
        oldest = self
        while not oldest.older is None:
            oldest = oldest.older
            if oldest is self:
                return None

        return oldest
    
    def __repr__(self):
        def process(sibling,results):
            if(len(sibling.candidacy)==1):
                if sibling.candidacy != {0}:
                    results.append("%s^%s"%(*sibling.candidacy,sibling.kind))
            elif(len(sibling.candidacy)==0) and (sibling.optional!=0):
                results.append("0^%s"%(sibling.kind))

            return [results]
        
        results = []
        oldest = self.getOldest()
        results, = oldest.forAllSiblings(process,results)
        return ".".join(results)

    def findByKind(self,kind):
        def process(sibling,results):
            if sibling.kind == kind:
                results.append(sibling)
            return [results]
        
        results = []
        results, = self.forAllSiblings(process,results)
        if len(results)!=1:
            return None
        return results[0]

    def getKnowns(self):
        def process(sibling,result):
            if len(sibling.candidacy)==1:
                if sibling.candidacy != {0}:
                    result[sibling.kind] = list(sibling.candidacy)[0]
            return [result]
        
        result = dict()
        result, = self.forAllSiblings(process,result)
        return result

    def exclude(self,knowns):
        result = False
        for kind in knowns.keys():
            sibling = self.findByKind(kind)
            if knowns[kind] in sibling.candidacy:
                sibling.candidacy -= {knowns[kind]}
                if len(sibling.candidacy) == 1:
                    result = True
        return result
    
    def populate(self, number, optional = -1):
        if (number < 0):
            return False
        if (number == 0) and (optional == 0):
            return False
        self.number = number 
        self.optional = optional
        minVal = (1 if (self.optional==0) else 0)
        self.candidacy=set(range(minVal,self.number+1))
        return True

    def templateFrom(self):
        template = None
        younger = self
        while not (younger is None):
            template = CCandidacyNet(younger.kind,template)
            template.populate(younger.number,younger.optional)
            younger = younger.younger
            if younger is self:
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

    def mergeNet(self,other):
        younger = self.getOldest()
        looped = [None]
        while not younger in looped:
            looped.append(younger)
            compare = other.findByKind(younger.kind)
            if not (compare is None):
                younger.candidacy &= compare.candidacy
            younger = younger.younger

    def mimicInstance(self,attributes):
        result = True
        def process(sibling,attributes,result):
            if not sibling.setCandidacy(attributes):
                result = False
            return [attributes,result]
        
        attributes,result, = self.forAllSiblings(process,attributes,result)
        return result

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