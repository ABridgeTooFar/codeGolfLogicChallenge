class CLinkedList:
    def forAllSiblings(self,process,*args):
        looped = [None]
        sibling = self
        while not any([sibling is other for other in looped]):
            args = process(sibling,*args)
            looped.append(sibling)
            sibling = sibling.younger
        sibling = self.older
        while not any([sibling is other for other in looped]):
            args = process(sibling,*args)
            looped.append(sibling)
            sibling = sibling.older

        return args
    
    def __init__(self, sibling=None):
        self.older = sibling
        self.younger = None
        if not (sibling is None):
            self.younger = sibling.younger
            sibling.younger = self

    def getOldest(self):
        looped = [None]
        oldest = self
        sibling = oldest.older
        while not any([sibling is other for other in looped]):
            looped.append(oldest)
            oldest = sibling
            sibling = oldest.older

        return oldest
    
    def __repr__(self):
        def process(sibling,results):
            results.append("%i"%(len(results)))

            return [results]
        
        results = []
        oldest = self.getOldest()
        results, = oldest.forAllSiblings(process,results)
        return "->".join(results)


def main():
    print("Welcome from Python")
    linkedList = None
    for i in range(10):
        linkedList = CLinkedList(linkedList)
    print(linkedList)



if __name__=="__main__":
    main()