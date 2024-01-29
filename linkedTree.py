class CLinkedTree:
    def walkIter(self):
        looped = [None]
        sibling = self.oldest
        while not any([sibling is other for other in looped]):
            yield sibling
            looped.append(sibling)
            sibling = sibling.younger

        return None

    def walkAll(self,process,*args):
        looped = [None]
        sibling = self.oldest
        while not any([sibling is other for other in looped]):
            args = process(sibling,*args)
            looped.append(sibling)
            sibling = sibling.younger

        return args
    
    def __init__(self, sibling=None):
        self.descendent = None
        if sibling is None:
            self.oldest = self
            self.younger = None
        else:
            self.oldest = sibling.oldest
            self.younger = sibling.younger
            sibling.younger = self

    def __repr__(self):
        def process(self,results):
            results.append("%i"%(len(results)))
            recurse = self.descendent
            if not (recurse is None):
                results.append(recurse.__repr__())
            return [results]
        
        results = []
        results, = self.walkAll(process,results)
        return "["+",".join(results)+"]"

    def flatten(self):
        def process(self,results):
            results.append(self)
            recurse = self.descendent
            if not (recurse is None):
                results += recurse.flatten()
            return [results]
        
        results = []
        results, = self.walkAll(process,results)
        return results

class CShoot(CLinkedTree):
    def __init__(self, sibling=None):
        self.descendent = None
        if sibling is None:
            self.oldest = self
            self.younger = None
        else:
            self.oldest = sibling.oldest
            self.younger = None
            adoptee=sibling.younger
            self.descendent = adoptee
            while not (adoptee is None):
                adoptee.oldest = sibling.younger
                adoptee = adoptee.younger
            sibling.younger = self

    def tee(self,branch):
        self.descendent = branch.oldest

def main():
    print("Welcome from Python")
    linkedTree = None
    for i in range(10):
        linkedTree = CLinkedTree(linkedTree)
    print(linkedTree)

    root = CShoot()
    trunk = CShoot()
    branch = CShoot()
    for i in range(5):
        trunk = CShoot(trunk)
    root.tee(trunk)
    for i in range(2):
        branch = CShoot(branch)
    segments = trunk.flatten()
    segments[3].tee(branch)
    print(root)

if __name__=="__main__":
    main()