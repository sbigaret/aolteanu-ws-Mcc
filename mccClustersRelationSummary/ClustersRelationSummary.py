import copy, math, random
class ClustersRelationSummary(object):
    def __init__(self, objects, relation):
        
        self.objects = objects
        self.N = len(objects)
        self.R = relation
        self.Q = ['p+','p-']
        
    def RKSummary(self, K):
        
        L = ['i','p+','p-','j']
        RKsum = {}
        for k1 in K:
            RKsum[k1] = {}
            for k2 in K:
                RKsum[k1][k2] = {}
                for m in L:
                    RKsum[k1][k2][m] = 0.0
                if k1 == k2:
                    for k in range(len(K[k1])-1):
                        for l in range(len(K[k1]))[k+1:]:
                            o = K[k1][k]
                            p = K[k1][l]
                            for m in L:
                                RKsum[k1][k1][m] += self.R[o][p][m]
                else:
                    for k in range(len(K[k1])):
                        for l in range(len(K[k2])):
                            o = K[k1][k]
                            p = K[k2][l]
                            for m in L:
                                RKsum[k1][k2][m] += self.R[o][p][m]
        return RKsum
