from legend import contextToTree

class CClueMatrix():
    def __init__(self,tree,fills,clues):
        self.legend = tree.flatten()
        self.map = {shoot.data['key']:pos for pos,shoot in enumerate(self.legend)}
        self.width = [shoot.data['value'] for shoot in self.legend]
        self.nulls = [0]*len(fills)
        for kind,fill in fills:
            self.nulls[self.map[kind]]=fill
        row = 0
        self.matrix = dict()
        for clue in clues:
            #print(row,clue)
            rows = []
            o = 0
            for entity in clue:
                #print(entity)
                o += 1
                template = [set(
                                range(( 0 if (shoot.data['type']==';') else 1),
                                        1+shoot.data['value'])) 
                            for shoot in self.legend]
                for attribute in entity:
                    #print(attribute)
                    pos = self.map[attribute[1]]
                    if int(attribute[0]) in template[pos]:
                        template[pos]={int(attribute[0])}
                    else:
                        template[pos].clear()
                rows.append(template)
            self.matrix[row]=rows
            row += o

    def __repr__(self):
        result = (",".join(self.map.keys()))+"\r\n"
        for group in self.matrix:
            result += "=".join(["="*w for w in self.width])+"==\n"
            for o,row in enumerate(self.matrix[group]):
                for oo,candidates in enumerate(row):
                    tab = [" "]*self.width[oo]
                    if 0 in candidates:
                        if len(candidates) == 1:
                            tab = ["0"]*self.width[oo]
                        else:
                            tab = ["X"]*self.width[oo]
                            for candidate in candidates:
                                if candidate != 0:
                                    tab[candidate-1]="?"
                    elif len(candidates)==1:
                        tab = [" "]*self.width[oo]
                        for candidate in candidates:
                            tab[candidate-1]=str(candidate)
                    elif self.nulls[oo]>0:
                        tab = ["%i"%self.nulls[oo]]*self.width[oo]

                    result +="|%s"%"".join(tab)
                result += "| %i\n"%(1+group+o)
        result += "=".join(["="*w for w in self.width])+"==\n"
        return result

    def export(self):
        result = ""
        for group in self.matrix:
            result += "=".join(["="*w for w in self.width])+"==\n"
            for o,row in enumerate(self.matrix[group]):
                for oo,candidates in enumerate(row):
                    tab = [" "]*self.width[oo]
                    if 0 in candidates:
                        if len(candidates) == 1:
                            tab = ["0"]*self.width[oo]
                        else:
                            tab = ["X"]*self.width[oo]
                            for candidate in candidates:
                                if candidate != 0:
                                    tab[candidate-1]="?"
                    elif len(candidates)==1:
                        tab = [" "]*self.width[oo]
                        for candidate in candidates:
                            tab[candidate-1]=str(candidate)
                    elif self.nulls[oo]>0:
                        tab = "-"**self.width[oo] #["%i"%self.nulls[oo]]*self.width[oo]

                    result +="|%s"%"".join(tab)
                result += "| %i\n"%(1+group+o)
        result += "=".join(["="*w for w in self.width])+"==\n"
        return result
    
def processContext(context):
    fills = []
    counts = []
    ids = []
    bonds = []
    bodies = []
    for (count,id,body,bond) in context:
        fills.append(0)
        counts.append(int(count))
        ids.append(id)
        bonds.append(bond)
        if len(body)>0:
            bodies.append(processContext(body))
        #else:
        #    bodies.append(None)
 
    setType = set([bond for bond in bonds if bond!=']'])
    if setType == {';'}:
        tally = sum(counts)
        fills = [tally - count for count in counts]
    for fill,count,id in bodies:
        fills += fill
        counts += count
        ids += id
    if len(setType) == 1:
        return tuple([fills,counts,ids])
    return tuple([[],[],[]])

def generatePreamble(context,kinds,numbers):
    preamble = []
    skipid = set()
    bodies = [context]
    for subcontext in bodies:
        for (count,id,body,_) in subcontext:
            if len(body)>0:
                skipid.update({id})
                bodies.append(body)
                member = 0
                membership = []
                for siblings,childId,_,bond in body:
                    for val in range(int(siblings)):
                        if member >= int(count):
                            break
                        membership.append( "%i^%s.%i^%s"%(member+1,id,val+1,childId))
                        member += 1
                    skipid.update({childId})
                    if bond != ";":
                        break
                preamble.append( ";".join(membership))
    for id,number in zip(kinds,numbers):
        if id in skipid:
            continue
        preamble.append( ";".join([str(val+1)+"^"+id for val in range(number)]))
    preamble = "\n".join(preamble)
    return preamble


def parseClues(preamble,scope):
    clues = []
    combo = preamble.rstrip()+"\n"+scope.lstrip()
    for line in combo.splitlines():
        if len(line.strip()) == 0:
            continue
        clues.append([])
        for mention in line.split(";"):
            clue = []
            for attribute in mention.split("."):
                id_group = attribute.split("^")
                id = id_group[0]
                group = id_group[1]
                clue.append(tuple([id,group]))
            clues[-1].append(clue)
    #print(clues)
    return clues

def generate(**kwargs):
    Puzzle = None
    with open(kwargs['puzzleFile']) as file:
        lines=file.readlines()
        Puzzle="".join(lines)
    part = Puzzle.split("#")
    unparsedCols = part[0]
    unparsedClues=part[1]

    context,tree = contextToTree(unparsedCols)
    fills,numbers,kinds = processContext(context)

    preamble = generatePreamble(context,kinds,numbers)
    clues = parseClues(preamble,unparsedClues)
    renderer = CClueMatrix(tree,[*zip(kinds,fills)],clues)
    return renderer,part[2:]

def main(**kwargs):
    from solver import unrender

    print("Welcome from Python")

    renderer,extraParts = generate(**kwargs)

    if len(extraParts)>0:
        sortedKeys = [shoot.data['key'] for shoot in renderer.legend]
        hint = ";".join(extraParts[0].strip().splitlines())
        solution = parseClues("",hint)
        group = solution[-1]
        #print(sortedKeys)
        for individual in group:
            attributes = {attribute:value for value,attribute in individual}
            print(",".join([attributes[key] for key in sortedKeys if key in attributes]))

    results = unrender(renderer.export())
    print(results)


if __name__ == "__main__":
    import sys
    puzzleFile = "PCgbWI.txt"
    if len(sys.argv)>1:
        puzzleFile = sys.argv[1]
    main( puzzleFile = puzzleFile )