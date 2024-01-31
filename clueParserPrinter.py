#!/bin/python3

from legend import contextToTree

def parseClues(preamble,scope):
    clues = []
    combo = preamble.rstrip()+"\n"+scope.lstrip()
    for line in combo.splitlines():
        if len(line.strip()) == 0:
            continue
        clues.append([]);
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
        pop = sum(counts)
        fills = [pop - count for count in counts]
    for fill,count,id in bodies:
        fills += fill
        counts += count
        ids += id
    if len(setType) == 1:
        return tuple([fills,counts,ids])
    return tuple([[],[],[]])

def initializeRow(fills,counts,ids):
    row = { (id,fill): set(range(1,count+1)) for fill,count,id in zip(fills,counts,ids) }
    return row

def prependPreamble(context,columns):
    template = initializeRow(*columns)
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
                        break;
                preamble.append( ";".join(membership))
    for id,fill in template:
        if id in skipid:
            continue
        members = len(template[(id,fill)])
        preamble.append( ";".join([str(val+1)+"^"+id for val in range(members)]))
    preamble = "\n".join(preamble)
    #print(preamble)
    return (template,preamble)

def processClues(template,clues):
    legend = list(template.keys())
    rows = {}
    rownumber = 0
    for clue in clues:
        rownumber += 1
        rowmember = 0
        for mention in clue:
            rowmember += 1
            attributes = []
            candidates = list(template.values())
            for attribute in mention:
                groups = [o for o,v in enumerate(legend) if v[0] == attribute[1]]
                for group in groups:
                    if int(attribute[0]) in candidates[group]:
                        candidates[group]={int(attribute[0])}
                    else:
                        if legend[group][1]>0:
                            candidates[group]={}
                        else:
                            candidates[group]=None
                attributes.append("^".join(attribute))
            nickname = (".".join(attributes),"%i.%i"%(rownumber,rowmember))
            rows[nickname]= candidates
    return rows

def reduce(rows):
    updated = False
    legend = list(rows.keys())
    members = len(legend)
#    colMembers = [len(template[l]) for l in legend]
#    lastpar = '0'
    rowGroups = {}
    for row in rows: 
        par,sec = row[1].split('.')
        if not int(par) in rowGroups:
            rowGroups[int(par)] = []
        rowGroups[int(par)].append(int(sec))

    reset = True
    rowNum = 0
    par=min(rowGroups.keys())
    while par<len(rowGroups):
        if reset:
            par=min(rowGroups.keys())
            rowNum = 0
            reset = False
            continue

        if rowNum>=members:
            break
        parNum = rowNum
        cols = len(rows[legend[parNum]])
        rowsInGroup = len(rowGroups[par])
        for colNum in range(cols):
            solutions = set()
            for section in range(rowsInGroup):
                secNum = parNum + section
                if len(rows[legend[secNum]][colNum])==1:
                    solutions.update(rows[legend[secNum]][colNum])
            for section in range(rowsInGroup):
                secNum = parNum + section
                if len(rows[legend[secNum]][colNum])>1:
                    if rows[legend[secNum]][colNum]&solutions:
                        updated = True
#                    rows[legend[secNum]][colNum]-=solutions #TODO.. remove known solutions
                    if len(rows[legend[secNum]][colNum])<=1:
                        reset = True
        if not reset:
            rowNum += rowsInGroup
            par += 1
    if not updated:
        return None
    
    return rows


def compareNotes(rows):
    updated = False

    rowKeys = list(rows.keys())
    maxRow = len(rowKeys)-5
    rowNum=0
    while rowNum < maxRow:
        altNum =  rowNum+1
        while altNum<maxRow:
            couples = list(zip(rows[rowKeys[rowNum]],rows[rowKeys[altNum]]))
            mate = False
            for col,couple in enumerate(couples):
                if couple[0]==couple[1] and len(couple[0])==1:
                    mate=True
                    break
            if mate:
                mated = False
                #print(rowNum+1,altNum+1,list(couples))
                for col,couple in enumerate(couples):
                    first = set(rows[rowKeys[rowNum]][col])
                    second = set(rows[rowKeys[altNum]][col]) 
                    if(first != second):
                        pair = first&second
                        #print(couples[col],pair)
                        rows[rowKeys[rowNum]][col]=pair
                        rows[rowKeys[altNum]][col]=pair
                        mated=True
                if mated:
                    updated = True
                    #print("back to start")
                    rowNum=0
                    altNum=1
                    continue
            altNum += 1
        rowNum += 1

    if not updated:
        return None
    
    return rows

def showOutput(template,rows,columns):
    template = initializeRow(*columns)
    legend = list(template.keys())
    colMembers = [len(template[l]) for l in legend]
    #print(template)
    lastpar = '0'
    lastsec = 0
    separator = 0
    rowNum = 0
    for row in rows:
        rowNum += 1
        par,sec = row[1].split('.')
        separator = 0
        result = ""
        for col,members in enumerate(colMembers):
            id,fill = legend[col]
            separator += members+fill+1
            candidates = rows[row][col]
            if len(candidates)<=1:
                xs = ["X" if (len(candidates)>0) else " "]*(members+fill)
                for pos in candidates:
                    #print(candidates)
                    xs[fill+pos-1]="_"
                result += "|"+"".join(xs)
            elif len(rows[row][col])==members:
                result += "|"+"-"*(members+fill)
            else:
                result += "|"+"?"*(members+fill)
        result += "|"
        if int(lastpar) < int(par):
            print("|"+"="*(separator-1)+"|")
        print(result,rowNum)
        lastpar = par
        lastsec = sec
        #print(rows[row])
    if separator > 0:
        print("|"+"="*(separator-1)+"|")

Puzzle = ""

def main(**kwargs):
    global Puzzle
    print("Welcome from Python")
    #print(unparsedCols)

    with open(kwargs['puzzleFile']) as file:
        lines=file.readlines()
        Puzzle="".join(lines)
    part = Puzzle.split("#")
    unparsedCols = part[0]
    unparsedRows=part[1]
    context,_ = contextToTree(unparsedCols)
    columns = processContext(context)
    template,preamble = prependPreamble(context,columns)

    clues = parseClues(preamble,unparsedRows)
    rows = processClues(template,clues)
    #showOutput(template,rows,columns)
    while True:
        reduce(rows)
        #if not (newRows is None):
        #    rows = newRows
        newRows = compareNotes(rows)
        if newRows is None:
            break
        #rows = newRows
        #break

    showOutput(template,rows,columns)

    if len(part)>2:
        solution = ";".join(part[2].strip().splitlines())
        goal = parseClues(preamble,solution)
        rows = processClues(template,goal)
        while True:
            reduce(rows)
            #if not (newRows is None):
            #    rows = newRows
            newRows = compareNotes(rows)
            if newRows is None:
                break
        showOutput(template,rows,columns)

if __name__ == "__main__":
    import sys
    puzzleFile = "PCgbWI.txt"
    if len(sys.argv)>1:
        puzzleFile = sys.argv[0]
    main( puzzleFile = puzzleFile )