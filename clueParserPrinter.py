#!/bin/python3

Puzzle = """
5@All[5@P.5@C[3@B;2@G].5@W.5@I]
#
2^B.0^G;0^G.3^W;5^I
0^B.2^G.2^P
0^B.4^W.2^I
0^B.1^P
0^B.1^G.1^I
3^B.0^G.1^W
5^W.5^P
4^I.4^P
#
1^C.1^G.0^B.1^I.1^P.2^W
2^C.2^G.0^B.2^I.2^P.4^W
3^C.0^G.1^B.4^I.4^P.3^W
4^C.0^G.2^B.3^I.5^P.5^W
5^C.0^G.3^B.5^I.3^P.1^W
"""

part = Puzzle.split("#")
unparsedCols = part[0]
solution = ";".join(part[2].strip().splitlines())
# print(solution)
unparsedRows=part[1].rstrip()+"\n"+solution.lstrip()

def matchBrace(inner,labelEnd,maxL):
    bodyEnd=labelEnd
    if inner[labelEnd]=='[':
        nest = 1
        while nest > 0 and bodyEnd+1<maxL:
            bodyEnd += 1
            if inner[bodyEnd]=='[':
                nest += 1
            if inner[bodyEnd]==']':
                nest -= 1
        if nest > 0:
            return -1
    body = parseContext(inner[labelEnd+1:bodyEnd+1])
    return (bodyEnd+1,body)

def parseContext(scope):
    result = []
    maxL = len(scope.rstrip())
    minL = maxL - len(scope.strip())
    #print(scope[minL:maxL])

    l = minL
    numStop = -1
    labelStop = -1
    bodyStop = -1
    body = []
    phase = 0
    while l<maxL:
        if phase == 0:
            if not scope[l] in "@":
                l += 1
                numStop = l
                continue

            if numStop<=minL:
                print(phase)
                return None

            phase = 1

        if phase == 1:
            if not scope[l] in "[;.]":
                l += 1
                labelStop = l
                continue

            if labelStop<=numStop:
                print(phase)
                return None
                
            bodyStop = labelStop
            phase = 2
            if scope[bodyStop] == "[":
                bodyStop,body = matchBrace(scope,labelStop,maxL)
                if bodyStop <= labelStop:
                    print(phase)
                    return None
                
                l = bodyStop

        if phase == 2:
            if bodyStop<maxL and not scope[bodyStop] in ";.]":
                print(-phase,scope[numStop:bodyStop+1])
                return None
            
            howMany = scope[minL:numStop]
            whatKind = scope[numStop+1:labelStop]
            if bodyStop<maxL:
                howBound = scope[bodyStop]
            else:
                howBound = ''
            result.append(tuple([howMany,whatKind,body,howBound]))

            minL = bodyStop+1
            l = minL
            numStop = -1
            labelStop = -1
            bodyStop = -1
            body = []
            phase = 0

    return result


def parseClues():
    clues = []
    for line in unparsedRows.splitlines():
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
    # print(row)
    return row

def processClues(columns,clues):
    template = initializeRow(*columns)
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
    return (template,rows)

def showOutput(template,rows):
    legend = list(template.keys())
    colMembers = [len(template[l]) for l in legend]
    #print(legend)
    lastpar = '0'
    lastsec = 0
    separator = 0
    for row in rows:
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
                    xs[fill+pos-1]="_"
                result += "|"+"".join(xs)
            elif len(rows[row][col])==members:
                result += "|"+"-"*(members+fill)
            else:
                result += "|"+"?"*(members+fill)
        result += "|"
        if int(lastpar) < int(par):
            print("|"+"="*(separator-1)+"|")
        print(result)
        lastpar = par
        lastsec = sec
        #print(rows[row])
    if separator > 0:
        print("|"+"="*(separator-1)+"|")

def main():
    print("Welcome from Python")
    print(unparsedCols)
    context = parseContext(unparsedCols)
    columns = processContext(context)
    clues = parseClues()
    template,rows = processClues(columns,clues)
    showOutput(template,rows)

if __name__ == "__main__":
    main();