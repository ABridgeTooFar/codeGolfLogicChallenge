from candidacyNet import CCandidacyNet

class CCandidacyCycle():
    def __init__(self):
        self.cycle = []

    def __repr__(self):
        results = []
        for next in self.cycle:
            results.append(CCandidacyNet.__repr__(next))

        return ";".join(results)

    def pushInstance(self,other):
        self.cycle.append(other)

    def mergeCycles(self,other):
        mated = []
        theirs = [compare.getKnowns() for compare in other.cycle]
        for next in self.cycle:
            mine = next.getKnowns()
            myKinds = set(mine.keys())
            for pos,compare in enumerate(theirs):
                ourKinds = myKinds&set(compare.keys())
                for kind in ourKinds:
                    if mine[kind]==compare[kind]:
                        next.mergeNet(other.cycle[pos])            
                        other.cycle[pos].mergeNet(next)
                        mated.append(pos)            
        return mated
    
    def preventDuplicates(self):
        result = False
        o = 0
        while o < len(self.cycle):
            i = self.cycle[o]
            mine = i.getKnowns()
            newKnowns = False
            for u in self.cycle[:o]:
                newKnowns = u.exclude(mine)
            if newKnowns:
                result = True
                o = 0
            else:
                for u in self.cycle[o+1:]:
                    newKnowns = u.exclude(mine)
                if newKnowns:
                    result = True
                o = o + 1
                
        return result