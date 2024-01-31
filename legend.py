from linkedTreeOverload import CLinkedTreeOverload

class CLegend(CLinkedTreeOverload):    
    def __init__(self, sibling=None,**kwargs):
        super().__init__(sibling,**kwargs)
        self.data.setdefault('key','')
        self.data.setdefault('value',-1)
        self.data.setdefault('type',']')
        if self.data['type']==']':
            self.data['type'] = self.oldest.data['type']
            
    def emit(self):
        return "(%s,%i,%s)"%(self.data['key'],self.data['value'],self.data['type'])
    
    def __repr__(self):
        def process(self,results):
            results += self.emit()
            recurse = self.descendent
            if not (recurse is None):
                results += "[" + recurse.__repr__() + "]"
            return [results]
        
        results = ""
        results, = self.walkAll(process,results)
        return results

    def flatten(self):
        def process(self,results):
            results.append(self)
            recurse = self.descendent
            if not (recurse is None):
                results += recurse.flatten()
            return [results]
        
        results = []
        results, = self.walkLine(process,results)
        return results

def handleOffshoots(shoot):
    tree = None
    for howMany,whatKind,offshoot,howBound, in shoot:
        tree = CLegend(tree,key=whatKind,value=int(howMany),type=howBound)
        if len(offshoot)>0:
            branch = handleOffshoots(offshoot)
            tree.tee(branch)
    return tree

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

def contextToTree(scope):
    shoot = parseContext(scope)
    tree = handleOffshoots(shoot)
    return shoot,tree

