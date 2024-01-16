from candidacyNet import CCandidacyNet

class CCandidacyCycle():
    def __init__(self):
        self.cycle = []

    def __repr__(self):
        results = []
        for next in self.cycle:
            results.append(CCandidacyNet.__repr__(next))

        return ";".join(results)

    def pushInstance(self,other):
        self.cycle.append(other)