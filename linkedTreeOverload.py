from linkedTree import CShoot

class CLinkedTreeOverload(CShoot):
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

    
    def __init__(self, sibling=None, **kwargs):
        self.data = kwargs
        super().__init__(sibling)

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
        results, = self.walkAll(process,results)
        return results


def main():
    print("Welcome from Python")
    linkedTree = None
    word = "Hello, Linked Tree"
    for data in word:
        linkedTree = CLinkedTreeOverload(linkedTree,default=data)
    print(linkedTree)
    print(CShoot.__repr__(linkedTree))
    print(linkedTree.data)



if __name__=="__main__":
    main()