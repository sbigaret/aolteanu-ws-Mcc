class PreferenceRelation(object):
    def __init__(self, objects, S, SCutType, SCutLevel):
        
        self.objects = objects
        self.N = len(objects)
        self.S = S
        self.Scuttype = SCutType
        self.Scutlvl = SCutLevel
        
    def ExtractR(self):
        R = {}
        for o in self.objects:
            R[o] = {}
            for p in self.objects:
                #        (i,p+,p-,j)
                R[o][p] = (1.0,0.0,0.0,0.0)
                
        for i in range(self.N - 1):
            for j in range(self.N)[i+1:]:
                o = self.objects[i]
                p = self.objects[j]
                oSp = 0
                pSo = 0
                if self.Scuttype == 'bipolar':
                    if self.Scutlvl == 0.0:
                        if self.S[o][p] < 0:
                            oSp = -1
                        elif self.S[o][p] > 0:
                            oSp = 1
                        if self.S[p][o] < 0:
                            pSo = -1
                        elif self.S[p][o] > 0:
                            pSo = 1
                    else:
                        if self.S[o][p] <= self.Scuttype:
                            oSp = -1
                        elif self.S[o][p] >= self.Scuttype:
                            oSp = 1
                        if self.S[p][o] <= self.Scuttype:
                            pSo = -1
                        elif self.S[p][o] >= self.Scuttype:
                            pSo = 1
                else:
                    if self.S[o][p] <= self.Scutlvl:
                        oSp = -1
                    else:
                        oSp = 1
                    if self.S[p][o] <= self.Scutlvl:
                        pSo = -1
                    else:
                        pSo = 1
                if oSp == 1:
                    if pSo == 1:
                        R[o][p] = (1.0,0.0,0.0,0.0)
                        R[p][o] = (1.0,0.0,0.0,0.0)
                    elif pSo == 0:
                        R[o][p] = (0.5,0.5,0.0,0.0)
                        R[p][o] = (0.5,0.0,0.5,0.0)
                    else:
                        R[o][p] = (0.0,1.0,0.0,0.0)
                        R[p][o] = (0.0,0.0,1.0,0.0)
                elif oSp == 0:
                    if pSo == 1:
                        R[o][p] = (0.5,0.0,0.5,0.0)
                        R[p][o] = (0.5,0.5,0.0,0.0)
                    elif pSo == 0:
                        R[o][p] = (0.25,0.25,0.25,0.25)
                        R[p][o] = (0.25,0.25,0.25,0.25)
                    else:
                        R[o][p] = (0.0,0.5,0.0,0.5)
                        R[p][o] = (0.0,0.0,0.5,0.5)
                else:
                    if pSo == 1:
                        R[o][p] = (0.0,0.0,1.0,0.0)
                        R[p][o] = (0.0,1.0,0.0,0.0)
                    elif pSo == 0:
                        R[o][p] = (0.0,0.0,0.5,0.5)
                        R[p][o] = (0.0,0.5,0.0,0.5)
                    else:
                        R[o][p] = (0.0,0.0,0.0,1.0)
                        R[p][o] = (0.0,0.0,0.0,1.0)
        return R