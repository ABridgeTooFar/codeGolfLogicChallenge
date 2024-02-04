class CSolver():
    def __init__(self,matrix,allWidths,allFills):
        self.matrix = matrix
        self.allWidths = allWidths
        self.allFills=allFills
        subgroups = []
        subgroup = []
        col = 0
        while col<len(self.allFills):
            fill = self.allFills[col]
            if fill == 0:
                if len(subgroup):
                    subgroups.append(subgroup)
                subgroup = []
            else:
                subgroup.append(col)
            col += 1

        if len(subgroup):
            subgroups.append(subgroup)

        self.subgroups = subgroups

    def render(self):
        result = ""
        rowTally = 0
        for group,members in enumerate(self.matrix):
            result += "=".join(["="*(self.allWidths - f) for f in self.allFills])+"==\n"
            for o,row in enumerate(members):
                for oo,candidates in enumerate(row):
                    width = self.allWidths-self.allFills[oo]
                    tab = [" "]*width
                    if 0 in candidates:
                        if len(candidates) == 1:
                            tab = ["0"]*(width)
                        else:
                            tab = ["X"]*(width)
                            for candidate in candidates:
                                if candidate != 0:
                                    tab[candidate-1]="?"
                    elif len(candidates)==1:
                        tab = [" "]*(width)
                        for candidate in candidates:
                            tab[candidate-1]=str(candidate)
                    elif self.allFills[oo]>0:
                        tab = "-"*width #["%i"%self.allFills[oo]]*width

                    result +="|%s"%"".join(tab)
                rowTally += 1
                result += "| %i\n"%(rowTally)
        result += "=".join(["="*(self.allWidths - f) for f in self.allFills])+"==\n"
        return result

    def __repr__(self):
        return self.render()
    
    def assertDistinctWithinGroup(self):
        for members in self.matrix:
            col = 0 
            while col < len(self.allFills):
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
                    col = 0
                else:
                    col += 1

    def assertQuotaWithinGroup(self):
        newKnowns = 0
        for members in self.matrix:
            for subgroup in self.subgroups:
                for col in subgroup:
                    absences = 0
                    for member in members:
                        if member[col]=={0}:
                            absences+=1
                    assert absences <= self.allFills[col], "fill limit exceeded"
                    if absences == self.allFills[col]:
                        for member in members:
                            if len(member[col])>1 and 0 in member[col]:
                                member[col] -= {0}
                                if(len(member[col])==1):
                                    newKnowns += 1

        for members in self.matrix:
            for member in members:
                for subgroup in self.subgroups:
                    absences = 0
                    for col in subgroup:
                        if member[col]=={0}:
                            absences += 1
                    if absences+1 == len(subgroup):
                        for col in subgroup:
                            if member[col]=={0}:
                                continue
                            if 0 in member[col]:
                                newKnowns += 1
                                member[col] -= {0}
        return newKnowns

    def matchAndMate(self):
        changed = False
        mates = {(col,value,): [] for col,fill in enumerate(self.allFills) for value in range(1,self.allWidths-fill+1)}
        for group,members in enumerate(self.matrix):
            for col in range(len(self.allFills)):
                o = 0
                while o <len(members):
                    if len(members[o][col])==1 and not (0 in members[o][col]):
                        mates[(col,int(*members[o][col]),)].append((group,o,))
                    o += 1
        for mate in mates:
            for o,member in enumerate(mates[mate]):                
                for oo,partner in enumerate(mates[mate]):
                    if oo == o:
                        continue
                    for col in range(len(self.allFills)):
                        if(self.matrix[member[0]][member[1]][col] != self.matrix[partner[0]][partner[1]][col]):
                            self.matrix[member[0]][member[1]][col]&=self.matrix[partner[0]][partner[1]][col]
                            changed = True
        return changed
    

def solve(matrix,allWidths,allFills):
    solver = CSolver(matrix,allWidths,allFills)
    tryAgain = True
    goodMeasure = False #True
    while tryAgain:
        solver.assertDistinctWithinGroup()
        newKnowns = solver.assertQuotaWithinGroup()
        changed = solver.matchAndMate()
        if newKnowns < 1 and not changed:
            tryAgain = goodMeasure
            goodMeasure = False
        else:
            #goodMeasure = True
            pass
        
    return solver.render()

def unrender(Puzzle):
    matrix = []
    rows = []
    allFills = dict()
    allWidths = set()
    for line in Puzzle.splitlines():
        if len(line.strip())==0:
            continue
        if line.startswith("="):
            if len(rows):
                matrix.append(rows)
            rows = []
        else:
            cols = [col for col in line.split("|") if len(col)>0]
            row = []
            counts = [len(col) for col in cols[:-1]]
            width = max(counts)
            allWidths.add(width)
            fills = [width - len(col) for col in cols[:-1]]
            for o,fill in enumerate(fills):
                if o in allFills:
                    allFills[o].add(fill)
                else:
                    allFills[o]={fill}

            for col,count,fill in zip(cols[:-1],counts,fills):
                if col in [' '*count,'-'*count]:
                    row.append(set(range(1,count+1)))
                elif col == '?'*count:
                    row.append(set(range(0,count+1)))
                elif col == '0'*count:
                    row.append({0})
                else:
                    value = int(col.strip())
                    row.append({value})
            rows.append(row)
    assert len(allWidths)==1,""
    return solve(matrix,int(*allWidths),[int(*allFills[o]) for o in sorted(allFills.keys())])