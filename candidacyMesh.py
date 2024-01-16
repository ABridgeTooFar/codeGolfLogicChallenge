from candidacyNet import CCandidacyNet
from candidacyCycle import CCandidacyCycle
from clueParserPrinter import parseContext,processContext

class CCandidacyMesh:
    def __init__(self):
        self.template = None
        self.cycles = []

    def parseCols(self,unparsedCols):
        self.template = None
        context = parseContext(unparsedCols)
        fills,numbers,kinds = processContext(context)
        youngest = self.template
        for o,kind in enumerate(kinds):
            younger = CCandidacyNet(kind,youngest)
            younger.populate(numbers[o],fills[o])
            youngest = younger
            if self.template is None:
                self.template = youngest

        return context
    
    def prependPreamble(self,unparsedCols):
        preamble = []
        bodies = [self.parseCols(unparsedCols)]
        if not (self.template is None):
            morekinds = set()
            for subcontext in bodies:
                for (count,kind,body,_) in subcontext:
                    if len(body)>0:
                        bodies.append(body)
                        member = 0
                        membership = []
                        for siblings,childKind,_,bond in body:
                            for val in range(int(siblings)):
                                if member >= int(count):
                                    break
                                membership.append( "%i^%s.%i^%s"%(member+1,kind,val+1,childKind))
                                member += 1
                            if bond != ";":
                                break;
                        preamble.append( ";".join(membership))
                    else:
                        morekinds.update({kind})

            for kind in morekinds:
                candidacy = self.template.findByKind(kind)
                if candidacy is not None:
                    preamble.append( ";".join([str(val)+"^"+kind for val in candidacy.candidacy]))

        preamble = "\n".join(preamble)
        return preamble

    def parseRows(self,unparsedRows):
        net = self.template
        self.cycles = []
        if not net is None:
            for rowsInCycle in unparsedRows.splitlines():
                cycle = CCandidacyCycle()
                for individuals in rowsInCycle.split(";"):
                    attributes={}
                    for attribute in individuals.split("."):
                        pair = attribute.split("^")
                        attributes[pair[1]]=int(pair[0])
                    instance = net.getTemplate()
                    instance.mimicInstance(attributes)
                    cycle.pushInstance(instance)
                self.cycles.append(cycle)
        return self.cycles

    def simpleSolve(self):
        lag = 0
        while lag < len(self.cycles):
            lead = lag + 1
            lastMated = []
            while lead < len(self.cycles):
                mated = self.cycles[lag].mergeCycles(self.cycles[lead])
                if mated == lastMated:
                    lead = lead + 1
                lastMated = mated
            newKnowns = False
            for cycle in self.cycles:
                if cycle.preventDuplicates():
                    newKnowns = True
            if newKnowns:
                lag = 0
            else:
                lag = lag + 1

        return self.cycles

def main():
    from clueParserPrinter import Puzzle
    print("Welcome from Python")
    part = Puzzle.split("#")
    unparsedCols = part[0]
    unparsedClues=part[1]
    solution = ";".join(part[2].strip().splitlines())
    mesh = CCandidacyMesh()
    preamble = mesh.prependPreamble(unparsedCols)
    unparsedRows = preamble.rstrip()+"\n"+unparsedClues.lstrip()
    cycles=mesh.parseRows(unparsedRows)
    print(cycles)
    cycles=mesh.simpleSolve()
    print(cycles)

    print(solution.split(";"))

if __name__=="__main__":
    main()