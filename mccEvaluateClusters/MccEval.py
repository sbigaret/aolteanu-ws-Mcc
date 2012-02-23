class MccEval(object):
    def __init__(self, objects, R, K_names, K, RK):
        
        self.objects = objects
        self.N = len(objects)
        self.R = R
        self.K_names = K_names
        self.K = K
        self.RK = RK
        self.Q = ['p+','p-']         
    
    def GetPerformances(self):
        
        return self.O_NR(),self.O_R(),self.O_T(),self.O_Q()
    
    def GetSummary(self):
        
        L = ['i','p+','p-','j']
        RKsum = {}
        for i in range(len(self.K_names)):
            k1 = self.K_names[i]
            RKsum[k1] = {}
            for j in range(len(self.K_names)):
                k2 = self.K_names[j]
                RKsum[k1][k2] = {}
                for m in L:
                    RKsum[k1][k2][m] = 0.0
                if i == j:
                    for k in range(len(self.K[k1])-1):
                        for l in range(len(self.K[k1]))[k+1:]:
                            o = self.K[k1][k]
                            p = self.K[k1][l]
                            for m in L:
                                RKsum[k1][k1][m] += self.R[o][p][m]
                else:
                    for k in range(len(self.K[k1])):
                        for l in range(len(self.K[k2])):
                            o = self.K[k1][k]
                            p = self.K[k2][l]
                            for m in L:
                                RKsum[k1][k2][m] += self.R[o][p][m]
        return RKsum

    def O_NR(self):
        o_NR = 0.0
        for i in range(len(self.K_names)):
            Y = self.K[self.K_names[i]]
            for k in range(len(Y)-1):
                for l in range(len(Y))[k+1:]:
                    o_NR += self.R[Y[k]][Y[l]]['i']
            for j in range(len(self.K_names))[i+1:]:
                Z = self.K[self.K_names[j]]
                for k in range(len(Y)):
                    for l in range(len(Z)):
                        o_NR += self.R[Y[k]][Z[l]]['p+']
                        o_NR += self.R[Y[k]][Z[l]]['p-']
                        o_NR += self.R[Y[k]][Z[l]]['j']
        return o_NR
    
    def O_R(self):
        o_R = 0
        for i in range(len(self.K_names)):
            Y = self.K[self.K_names[i]]
            for k in range(len(Y)-1):
                for l in range(len(Y))[k+1:]:
                    o_R += self.R[Y[k]][Y[l]]['i']
            for j in range(len(self.K_names))[i+1:]:
                Z = self.K[self.K_names[j]]
                for k in range(len(Y)):
                    for l in range(len(Z)):
                        o_R += self.R[Y[k]][Z[l]][self.RK[self.K_names[i]][self.K_names[j]]]

        return o_R
    
    def O_T(self):
        o_T = 0
        if len(self.K_names) > 2:
            for i in range(len(self.K_names)-2):
                for j in range(len(self.K_names)-1)[i+1:]:
                    for k in range(len(self.K_names))[j+1:]:
                        if self.RK[self.K_names[i]][self.K_names[j]] == self.RK[self.K_names[j]][self.K_names[k]] == self.RK[self.K_names[k]][self.K_names[i]]:
                            if self.RK[self.K_names[i]][self.K_names[j]] == 'p+' or self.RK[self.K_names[i]][self.K_names[j]] == 'p-':
                                o_T += 1
        return o_T
    
    def O_Q(self):
        o_Q = 0
        if len(self.K_names) > 1:
            for i in range(len(self.K_names)-1):
                Y = self.K[self.K_names[i]]
                for j in range(len(self.K_names))[i+1:]:
                    Z = self.K[self.K_names[j]]
                    ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                    for k in range(len(Y)):
                        for l in range(len(Z)):
                            ct['i'] += self.R[Y[k]][Z[l]]['i']
                            ct['p+'] += self.R[Y[k]][Z[l]]['p+']
                            ct['p-'] += self.R[Y[k]][Z[l]]['p-']
                            ct['j'] += self.R[Y[k]][Z[l]]['j']
                    max = ct[self.Q[0]]
                    sum = 0
                    for p in self.Q:
                        sum += ct[p]
                        if max < ct[p]:
                            max = ct[p]
                    o_Q += (sum - max)   
        return o_Q
    
