class CLinkedTreeOverload():
    def walkIter(self):
        sibling = self.oldest
        while not (sibling is None):
            yield sibling
            recurse = self.descendent
            if not (recurse is None):
                for descendent in recurse.walkIter():
                    yield descendent
            sibling = sibling.younger

        return None

    def walkLine(self,process,*args):
        looped = [None]
        sibling = self.oldest
        while not any([sibling is other for other in looped]):
            args = process(sibling,*args)
            looped.append(sibling)
            sibling = sibling.younger

        return args
    
    def __init__(self, sibling=None, **kwargs):
        self.data = kwargs
        self.descendent = None
        if sibling is None:
            self.oldest = self
            self.younger = None
        else:
            self.oldest = sibling.oldest
            self.younger = sibling.younger
            sibling.younger = self

    def emit(self):
        return self.data['default']
    
    def __repr__(self):
        def process(self,results):
            results += self.emit()
            recurse = self.descendent
            if not (recurse is None):
                results += recurse.__repr__()
            return [results]
        
        results = ""
        results, = self.walkLine(process,results)
        return results

    def tee(self,branch):
        self.descendent = branch.oldest

def main():
    print("Welcome from Python")
    linkedTree = None
    word = "Hello, Linked Tree"
    for data in word:
        linkedTree = CLinkedTreeOverload(linkedTree,default=data)
    print(linkedTree)
    print(linkedTree.data)



if __name__=="__main__":
    main()