from candidacyNet import CCandidacyNet
from clueParserPrinter import parseContext,processContext,prependPreamble

class CCandidacyMesh:
    def __init__(self):
        self.template = None

    def parse(self,unparsedCols):
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
        bodies = [self.parse(unparsedCols)]
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

def main():
    from clueParserPrinter import Puzzle
    print("Welcome from Python")
    part = Puzzle.split("#")
    unparsedCols = part[0]
    unparsedClues=part[1]
    solution = ";".join(part[2].strip().splitlines())
    #unparsedRows = unparsedClues.rstrip()+"\n"+solution.lstrip()
    mesh = CCandidacyMesh()
    preamble = mesh.prependPreamble(unparsedCols)
    print(preamble.rstrip()+"\n"+unparsedClues.lstrip())
    print(solution.split(";"))

if __name__=="__main__":
    main()