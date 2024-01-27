from legend import contextToTree
from clueParserPrinter import Puzzle

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
        print(self.map)
        return result

    def assertDistinctWithinGroup(self):
        for group in self.matrix:
            members = self.matrix[group]
            keys = list(self.map.keys())
            k = 0
            while k < len(keys):                
                col = self.map[keys[k]]
                knowns = dict()
                o = 0
                while o <len(members):
                    if len(members[o][col])==1 and not (0 in members[o][col]):
                        knowns[o]=int(*members[o][col])
                    o += 1
                newKnowns = 0
                for known in knowns:
                    others = [o for o in range(len(members)) if o != known]
                    for other in others:
                        members[other][col]-={knowns[known]}
                        if len(members[other][col])==1:
                            if members[other][col]!={0} and not other in knowns:
                                newKnowns += 1
                if newKnowns>0:
                    k = 0
                else:
                    k += 1

    def assertQuotaWithinGroup(self):
        newKnowns = 0
        for group in self.matrix:
            members = self.matrix[group]
            for key in self.map.keys():                
                col = self.map[key]
                absences = 0
                for member in members:
                    if member[col]=={0}:
                        absences+=1
                if absences >= self.nulls[col]:
                    for member in members:
                        if len(member[col])>1 and 0 in member[col]:
                            member[col] -= {0}
                            if(len(member[col])==1):
                                newKnowns += 1
        subgroups = []
        o = 0
        while o<len(self.legend):
            shoot = self.legend[o]
            if shoot.data['type'] == ';':
                subgroups.append([])
                start = shoot.oldest
                while (not (shoot is None)) and shoot.oldest is start:
                    subgroups[-1].append(shoot.data['key'])
                    o += 1
                    shoot = shoot.younger
            else:
                o += 1

        for group in self.matrix:
            members = self.matrix[group]
            for member in members:
                for subgroup in subgroups:
                    absences = 0
                    for key in subgroup:
                        col = self.map[key]
                        if member[col]=={0}:
                            absences += 1
                    if absences+1 == len(subgroup):
                        for key in subgroup:
                            col = self.map[key]
                            if member[col]=={0}:
                                continue
                            if 0 in member[col]:
                                print("=========",member[col])
                                newKnowns += 1
                                member[col] -= {0}
        return newKnowns

    def matchAndMate(self):
        changed = False
        keys = list(self.map.keys())
        mates = {(key,value,): [] for key in keys for value in range(1,self.width[self.map[key]]+1)}
        for group in self.matrix:
            members = self.matrix[group]
            for key in keys:                
                col = self.map[key]
                o = 0
                while o <len(members):
                    if len(members[o][col])==1 and not (0 in members[o][col]):
                        mates[(key,int(*members[o][col]),)].append((group,o,))
                    o += 1
        for mate in mates:
            for o,member in enumerate(mates[mate]):                
                for oo,partner in enumerate(mates[mate]):
                    if oo == o:
                        continue
                    for key in keys:                
                        col = self.map[key]
                        self.matrix[group]
                        if(self.matrix[member[0]][member[1]][col] != self.matrix[partner[0]][partner[1]][col]):
                            self.matrix[member[0]][member[1]][col]&=self.matrix[partner[0]][partner[1]][col]
                            changed = True
        return changed
    
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

def main():

    print("Welcome from Python")

    part = Puzzle.split("#")
    unparsedCols = part[0]
    unparsedClues=part[1]
    hint = ";".join(part[2].strip().splitlines())
    #print(hint)
    context,tree = contextToTree(unparsedCols)
    fills,numbers,kinds = processContext(context)
    preamble = generatePreamble(context,kinds,numbers)

    solution = parseClues(preamble,hint)
    #print(solution)
    goal = CClueMatrix(tree,[*zip(kinds,fills)],solution)
    print(goal)

    clues = parseClues(preamble,unparsedClues)
    solver = CClueMatrix(tree,[*zip(kinds,fills)],clues)
    print(solver)
    tryAgain = True
    while tryAgain:
        solver.assertDistinctWithinGroup()
        newKnowns = solver.assertQuotaWithinGroup()
        changed = solver.matchAndMate()
        if newKnowns < 1 and not changed:
            tryAgain = False
        
    print(solver)


if __name__ == "__main__":
    main();