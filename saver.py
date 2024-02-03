from solver import solve

if __name__ == "__main__":
    import sys
    Puzzle = None
    with open("matrix.in") as file:
        lines=file.readlines()
        Puzzle="".join(lines)
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
    print(matrix,allWidths,allFills)
    assert len(allWidths)==1,""
    solve(matrix,int(*allWidths),[int(*allFills[o]) for o in sorted(allFills.keys())])