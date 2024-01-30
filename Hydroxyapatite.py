
def generatePayload(delimiters, tape, pos=0, delimiter = ''):
    payloads = []
    assert (pos>=len(tape) or tape[pos].isupper()),"illegal start"

    lastpos = pos
    pos = pos + 1
    while pos<len(tape):
        c=tape[pos]
        if c.isupper():
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            payloads.append(payload)
            lastpos = pos
        elif c in delimiters.keys():
            assert (delimiter == delimiters[c]),"Unmatched delimiter"
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            payloads.append(payload)
            return payloads
        elif c in delimiters.values():
            payload={'pos':lastpos, 'key':tape[lastpos:pos]}
            payloads.append(payload)
            lastpos = pos
            recurse = generatePayload(delimiters,tape, pos + 1, delimiter = c)
            pos = recurse[-1]['pos']+len(recurse[-1]['key'])
            payloads.append(recurse)
            assert pos<len(tape),"Unmatched delimiter"
            assert (tape[pos] in delimiters),"Unmatched delimiter"
            assert (delimiters[tape[pos]] == c),"Unmatched delimiter"

        pos += 1

    payload={'pos':lastpos, 'key':tape[lastpos:pos]}
    payloads.append(payload)
    return payloads

def reorder(payloads):
    neworder = []
    adoptee = None
    for payload in payloads:
        if type(payload) is type([]):
            adoptee = reorder(payload)
        else:
            neworder.append(payload)
            if adoptee:
                neworder.append(adoptee)
                adoptee = None

    return neworder

def recast(neworder):
    newtype =[]
    for payload in neworder:
        if type(payload) is type([]):
            newtype[-1]['body'] = recast(payload)
        else:
            symbol = payload['key']
            pos = 0
            count = 1
            while symbol[pos-1].isdecimal():
                pos -= 1
            if pos<0:
                count = int(symbol[pos:])
                symbol=symbol[:pos]

            newtype.append({'count':count,'symbol':symbol,'body':None})

    return newtype

def compute(newtype):
    elements = []
    numbers = []
    keys=['count','symbol','body']
    
    for count,symbol,body in [tuple([entry[key] for key in keys]) for entry in newtype]:
            if body:
                result = compute(body)
                for element,number in result:
                    elements.append(element)
                    numbers.append(number * count)
            else:
                elements.append(symbol)
                numbers.append(count)

    return [(element,number) for element,number in zip(elements,numbers)]

def tally(results):
    combined = dict()
    for symbol,count in results:
        if symbol in combined:
            combined[symbol]+=count
        else:
            combined[symbol]=count
    return combined

def main():
    delimiters = { closer:opener for opener,closer in zip("{([","})]") }
    tape = "Hydroxyapatite{Ca10(PO4)6(OH)2}"
    payloads = generatePayload(delimiters,tape)
    neworder = reorder(payloads)
    newtype = recast(neworder)
    results = compute(newtype)
    print(tally(results))

if __name__=="__main__":
    main()