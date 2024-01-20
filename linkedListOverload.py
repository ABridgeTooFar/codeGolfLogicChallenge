from linkedList import CLinkedList

class CLinkedListOverload(CLinkedList):
    
    def __init__(self, data, sibling=None):
        self.data = data
        super().__init__(sibling)

    def __repr__(self):
        def process(sibling,results):
            results.append("%s"%(sibling.data))

            return [results]
        
        results = []
        oldest = self.getOldest()
        results, = oldest.forAllSiblings(process,results)
        return "".join(results)


def main():
    print("Welcome from Python")
    linkedList = None
    word = "Hello, Linked List"
    for data in word:
        linkedList = CLinkedListOverload(data,linkedList)
    print(linkedList)
    print(CLinkedList.__repr__(linkedList))
    print(linkedList.data)



if __name__=="__main__":
    main()