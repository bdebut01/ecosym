class ecosystem():
    def __init__(self, hdim, vdim):
        self.ocean = []
        for i in range(hdim):
            for j in range(vdim):
                tempblock = SeaBlock()
        self.orgsList = []
    
    