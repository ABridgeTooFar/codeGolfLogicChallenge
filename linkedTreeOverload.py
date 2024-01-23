from linkedTree import CShoot

class CLinkedTreeOverload(CShoot):
    
    def __init__(self, data, sibling=None):
        self.data = data
        super().__init__(sibling)

    def __repr__(self):
        def process(self,results):
            results += self.data
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
        linkedTree = CLinkedTreeOverload(data,linkedTree)
    print(linkedTree)
    print(CShoot.__repr__(linkedTree))
    print(linkedTree.data)



if __name__=="__main__":
    main()