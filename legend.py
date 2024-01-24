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

