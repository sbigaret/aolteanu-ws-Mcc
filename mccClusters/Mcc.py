import copy, math, random
class Mcc(object):
    def __init__(self, objects, relation, methodType):
        
        self.objects = objects
        self.N = len(objects)
        self.R = relation
        self.type = methodType
        self.Q = ['p+','p-']
        if methodType == "NR":
            self.Neighbours = self.Neighbours_1
            self.Fitness = self.O_1
        elif methodType == "R":
            self.Neighbours = self.Neighbours_2
            self.Fitness = self.O_2
        elif methodType == "O":
            self.Neighbours = self.Neighbours_3
            self.Fitness = self.O_3
        elif methodType == "QR":
            self.Neighbours = self.Neighbours_4
            self.Fitness = self.O_4
        elif methodType == "QO":
            self.Neighbours = self.Neighbours_5
            self.Fitness = self.O_5
        
    def Neighbours(self):
        return 0
    def Fitness(self):
        return 0
    
    def ExtractRK(self, K):
        
        RK = {}
        for i in range(len(K)):
            RK[i] = {}
            for j in range(len(K)):
                RK[i][j] = 'i'
                
        for i in range(len(K)-1):
            for j in range(len(K))[i+1:]:
                l = self.ExtractRK12(K[i], K[j])
                RK[i][j] = l
                if l == 'p+':
                    RK[j][i] = 'p-'
                elif l == 'p-':
                    RK[j][i] = 'p+'
                else:
                    RK[j][i] = l
        return RK
    
    def ExtractRK12(self, K1, K2):
        
        R = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
        for o in K1:
            for p in K2:
                R['i'] += self.R[o][p]['i']
                R['p+'] += self.R[o][p]['p+']
                R['p-'] += self.R[o][p]['p-']
                R['j'] += self.R[o][p]['j']
        L = ['p+','p-','j']
        if self.type == "O" or self.type == "QO":
            L = L[:-1]

        p = 0
        max = -1
        for l in L:
            if max < R[l]:
                max = R[l]
                p = l
                
        return p                 
    
    def Run(self):
        
        C = self.FindCores()
        K1 = self.ExpandCores(C)
        K = self.RefineClusters(K1)
        RK = self.ExtractRK(K)
        return K, RK
    
    def FindCores(self):
        
        max_cliques = self.EnumBK_K()
        perf_max_cliques = []
        for mc in max_cliques:
            perf = self.Fitness_Core(mc)
            perf_max_cliques.append([perf,mc])
        perf_max_cliques.sort(reverse = True)
        
        C = []
        while perf_max_cliques:
            perf = perf_max_cliques[0][0]
            mc = perf_max_cliques[0][1]
            C.append(mc)
            
            new_perf_max_cliques = []
            for pmc in perf_max_cliques[1:]:
                overlapping = False
                for o in mc:
                    if o in pmc[1]:
                        overlapping = True
                        break
                if not overlapping:
                    new_perf_max_cliques.append(pmc)
            perf_max_cliques = new_perf_max_cliques
        
        return C
    
    def EnumBK_K(self):
        
        results = []
        self.IK_G([],set(self.objects),set(), results)
        return results

    def IK_G(self,R,P,X,MC):
        
        if len(P) == 0 and len(X) == 0:
            MC.append(R)
        else:
            if len(P) > 0:
                tempP = copy.deepcopy(P)
                OIN_v = set()
                for u in P:
                    OIN_u = self.OIN(u)
                    if len(OIN_u) > len(OIN_v):
                        OIN_v = OIN_u
                for u in P:
                    if not(u in OIN_v):
                        tempP.remove(u)
                        R1 = copy.deepcopy(R)
                        R1.append(u)
                        P1 = copy.deepcopy(tempP)
                        OIN_u = self.OIN(u)
                        P1 = tempP.intersection(OIN_u)
                        X1 = X.intersection(OIN_u)
                        self.IK_G(R1,P1,X1,MC)
                        X.add(u)
    
    def ExpandCores(self, C):
        
        K1 = copy.deepcopy(C)
        objects = copy.deepcopy(self.objects)
        for c in C:
            for o in c:
                objects.remove(o)
        for o in objects:
            index = 0
            max_mm = -self.N - 1
            for i in range(len(C)):
                mm = self.MIM(o,C[i])
                if mm > max_mm:
                    max_mm = mm
                    index = i
            K1[index].append(o)
        
        return K1
    
    def RefineClusters(self, K1):
        
        RK1 = self.ExtractRK(K1)
        best_K = []
        best_RK = []
        best_f = (float('-inf'),float('-inf'),0.0)
        for i in range(5):
            K = self.SA(K1,RK1,100,30)
            RK = self.ExtractRK(K)
            f = self.Fitness(K,RK)
            better = True
            if f[0] < best_f[0]:
                better = False
            elif f[0] == best_f[0]:
                if f[1] < best_f[1]:
                    better = False
                elif f[1] == best_f[1]:
                    if f[2] <= best_f[2]:
                        better = False
            if better:
                best_K = K
                best_RK = RK
                best_f = f
                
        K1 = best_K
        RK1 = best_RK
        for i in range(5):
            K = self.SA(K1,RK1,100,30)
            RK = self.ExtractRK(K)
            f = self.Fitness(K,RK)
            better = True
            if f[0] < best_f[0]:
                better = False
            elif f[0] == best_f[0]:
                if f[1] < best_f[1]:
                    better = False
                elif f[1] == best_f[1]:
                    if f[2] <= best_f[2]:
                        better = False
            if better:
                best_K = K
                best_f = f
        return best_K
        
    def SA(self, s0, o0, Imax, Tmax):
        #initial energy
        f0 = self.Fitness(s0,o0)
        #initial best
        best_s = s0
        best_f = f0
        best_o = o0
        #generate neighbours
        N = self.Neighbours(s0,o0)
        #generate initial temperature
        T0 = 1
        for n in N:
            if n[0] > 0:
                T0+=n[0]
        T0 /= -math.log(0.8)#kirkpatrick
        #Min temp
        Tmin = 0.00001
        #cooling rate
        dT = (Tmin/T0)**(1.0/Imax)
        #iterations
        T = T0
        s = s0
        o = o0
        f = f0
        idle = 0
        for i in range(Imax):
            #generate neighbours
            N = self.Neighbours(s,o)
            for n in N:
                if n[0] > 0:
                    n[0] = 1
                else:
                    n[0] = math.exp(n[0]/T)
            n = self.Select_RW(N)
            s = self.GenerateS(s,n)
            o = self.ExtractRK(s)
            f = self.Fitness(s,o)
            better = True
            if f[0] < best_f[0]:
                better = False
            elif f[0] == best_f[0]:
                if f[1] < best_f[1]:
                    better = False
                elif f[1] == best_f[1]:
                    if f[2] <= best_f[2]:
                        better = False
            if better:
                best_f = f
                best_s = s
                best_o = o
            else:
                idle += 1
                if idle > Imax/5:
                    idle = 0
                    s = best_s
                    o = best_o
            #print i+1, best_f
            #new temperature
            T *= dT
        return best_s
    
    def Select_RW(self, N):
        
        sum = 0
        for n in N:
            sum += n[0]
        val = random.random()*sum
        for n in N:
            if val - n[0] <= 0:
                return n
            else:
                val -= n[0]
        return N[-1]
    
    def GenerateS(self, s, n):
        fr = n[1]
        to = n[2]
        o = n[3]
        ns = copy.deepcopy(s)
        if to == -1:
            ns.append([o])
            ns[fr].remove(o)
            if ns[fr] == []:
                ns.remove(ns[fr])
        else:
            ns[to].append(o)
            ns[fr].remove(o)
            if ns[fr] == []:
                ns.remove(ns[fr])
        return ns
    
    #--------------- Additional Procedures -----------#
        
    def OIN(self, x):
        
        result = set()
        for o in self.objects:
            if o != x:
                if self.R[x][o]['i'] >= 0.5:
                    result.add(o)
        return result
    
    def MIM(self, o, Y):
        
        mim = 0.0
        for p in Y:
            if o != p:
                mim += self.R[o][p]['i']
        return mim
    
    def Fitness_Core(self, Y, PI = None):
        
        performance = 0.0
        
        if PI == None:
            PI = {}
            for o in self.objects:
                PI[o] = self.MIM(o, Y)
                
        for o in self.objects:
            if o in Y:
                performance += PI[o] / float(self.N)
            else:
                performance -= PI[o] / float(self.N)
        performance = (performance / (self.N) + 1.0) / 2.0
        
        return performance
    
    def O_NR(self, K, RK = None):
        o_NR = 0.0
        for i in range(len(K)):
            Y = K[i]
            for k in range(len(Y)-1):
                for l in range(len(Y))[k+1:]:
                    o_NR += self.R[Y[k]][Y[l]]['i']
            for j in range(len(K))[i+1:]:
                Z = K[j]
                for k in range(len(Y)):
                    for l in range(len(Z)):
                        o_NR += self.R[Y[k]][Z[l]]['p+']
                        o_NR += self.R[Y[k]][Z[l]]['p-']
                        o_NR += self.R[Y[k]][Z[l]]['j']
        return o_NR * 2.0 / float(self.N) / float(self.N - 1)
    
    def O_R(self, K, RK):
        o_R = 0
        for i in range(len(K)):
            Y = K[i]
            for k in range(len(Y)-1):
                for l in range(len(Y))[k+1:]:
                    o_R += self.R[Y[k]][Y[l]]['i']
            for j in range(len(K))[i+1:]:
                Z = K[j]
                for k in range(len(Y)):
                    for l in range(len(Z)):
                        o_R += self.R[Y[k]][Z[l]][RK[i][j]]

        return o_R * 2.0 / float(self.N) / float(self.N - 1)
    
    def O_T(self, K, RK):
        o_T = 0
        if len(K) > 2:
            for i in range(len(K)-2):
                for j in range(len(K)-1)[i+1:]:
                    for k in range(len(K))[j+1:]:
                        if RK[i][j] == RK[j][k] == RK[k][i]:
                            if RK[i][j] == 'p+' or RK[i][j] == 'p-':
                                o_T -= 1
        return o_T
    
    def O_Q(self, K, RK):
        o_Q = 0
        if len(K) > 1:
            for i in range(len(K)-1):
                Y = K[i]
                for j in range(len(K))[i+1:]:
                    Z = K[j]
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
                    o_Q -= (sum - max)   
        return o_Q
    
    def O_1(self, K,RK):
        return (0,0,self.O_NR(K,RK))
    
    def O_2(self, K,RK):
        return (0,0,self.O_R(K,RK))
    
    def O_3(self, K,RK):
        return (0,self.O_T(K,RK),self.O_R(K,RK))
    
    def O_4(self, K,RK):
        return (0,self.O_Q(K,RK),self.O_R(K,RK))
    
    def O_5(self, K,RK):
        return (self.O_T(K,RK),self.O_Q(K,RK),self.O_R(K,RK))
    
    def Neighbours_1(self, K, RK):
        N = []
        for i in range(len(K)):
            Ki = K[i]
            for o in Ki:
                
                fi = 0.0
                for p in Ki:
                    if p != o:
                        fi += self.R[o][p]['i']
                for l in range(len(K)):
                    if l != i:
                        Kl = K[l]
                        for p in Kl:
                            fi += self.R[o][p]['p+']
                            fi += self.R[o][p]['p-']
                            fi += self.R[o][p]['j']

                for j in range(len(K)):
                    if j != i:
                        Kj = K[j]
                        
                        fj = 0.0
                        for p in Kj:
                            fj += self.R[o][p]['i']
                        for l in range(len(K)):
                            if l != j:
                                Kl = K[l]
                                for p in Kl:
                                    if p != o:
                                        fj += self.R[o][p]['p+']
                                        fj += self.R[o][p]['p-']
                                        fj += self.R[o][p]['j']
                                        
                        N.append([(fj-fi)/(self.N - 1),i,j,o])
                        
                fj = 0.0
                for p in self.objects:
                    if p != o:
                        fj += self.R[o][p]['p+']
                        fj += self.R[o][p]['p-']
                        fj += self.R[o][p]['j']
                        
                N.append([(fj-fi)/(self.N - 1),i,-1,o])
        return N
    
    def Neighbours_2(self, K, RK):
        N = []
        for i in range(len(K)):
            Ki = K[i]
            for o in Ki:
                
                fi = 0.0
                for p in Ki:
                    if p != o:
                        fi += self.R[o][p]['i']
                for l in range(len(K)):
                    if l != i:
                        Kl = K[l]
                        for p in Kl:
                            fi += self.R[o][p][RK[i][l]]

                for j in range(len(K)):
                    if j != i:
                        Kj = K[j]
                        
                        fj = 0.0
                        for p in Kj:
                            fj += self.R[o][p]['i']
                        for l in range(len(K)):
                            if l != j:
                                Kl = K[l]
                                for p in Kl:
                                    if p != o:
                                        fj += self.R[o][p][RK[j][l]]
                                        
                        N.append([(fj-fi)/(self.N - 1),i,j,o])
                        
                fj = 0.0
                for j in range(len(K)):
                    RKj = self.ExtractRK12([o],K[j])
                    for p in K[j]:
                        if p != o:
                            fi += self.R[o][p][RKj]
                        
                N.append([(fj-fi)/(self.N - 1),i,-1,o])
        return N
    
    
    def Neighbours_3(self, K, RK):
        
        N = self.Neighbours_2(K, RK)
        
        cy1 = 0
        if len(K) > 2:
            for k in range(len(K)-2):
                for l in range(len(K)-1)[k+1:]:
                    for m in range(len(K))[l+1:]:
                        if RK[k][l] == RK[l][m] == RK[m][k]:
                            if RK[k][l] == 'p+' or RK[k][l] == 'p-':
                                cy1 += 1
        K2 = copy.deepcopy(K)
        for n in N:
            f = n[0]
            i = n[1]
            j = n[2]
            o = n[3]
            K2[i].remove(o)
            if j == -1:
                K2.append([o])
            else:
                K2[j].append(o)
            remi = False
            if K2[i] == []:
                K2.remove([])
                remi = True
            RK2 = self.ExtractRK(K2)
            cy2 = 0
            if len(K2) > 2:
                for k in range(len(K2)-2):
                    for l in range(len(K2)-1)[k+1:]:
                        for m in range(len(K2))[l+1:]:
                            if RK2[k][l] == RK2[l][m] == RK2[m][k]:
                                if RK2[k][l] == 1 or RK2[k][l] == 2:
                                    cy2 += 1
            n[0] += (cy1-cy2)
            
            if remi:
                K2 = K2[:i] + [[]] + K2[i:]
            if j == -1:
                K2.remove([o])
            else:
                K2[j].remove(o)
            K2[i].append(o)
        return N
 
    def Neighbours_4(self, K, RK):
        
        N = self.Neighbours_2(K, RK)
        
        for n in N:
            f = n[0]
            i = n[1]
            j = n[2]
            o = n[3]
            
            q1 = 0
            if len(K) > 1:
                for k in range(len(K)):
                    if k != i:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        sum = 0
                        for p in self.Q:
                            if p != RK[i][k]:
                                sum += ct[p]
                        q1 += sum
                        
            q2 = 0
            if j != -1:
                for k in range(len(K)):
                    if k != j:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        sum = 0
                        for p in self.Q:
                            if p != RK[j][k]:
                                sum += ct[p]
                        q2 += sum
            else:
                for k in range(len(K)):
                    if k != j:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        max = ct[self.Q[0]]
                        sum = 0
                        for p in self.Q:
                            sum += ct[p]
                            if max < ct[p]:
                                max = ct[p]
                        q2 += (sum - max) 
                
                    
            n[0] += (q1-q2)
            
        return N
    
    def Neighbours_5(self, K, RK):
        
        N = self.Neighbours_3(K, RK)
        
        for n in N:
            f = n[0]
            i = n[1]
            j = n[2]
            o = n[3]
            
            q1 = 0
            if len(K) > 1:
                for k in range(len(K)):
                    if k != i:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        sum = 0
                        for p in self.Q:
                            if p != RK[i][k]:
                                sum += ct[p]
                        q1 += sum
                        
            q2 = 0
            if j != -1:
                for k in range(len(K)):
                    if k != j:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        sum = 0
                        for p in self.Q:
                            if p != RK[j][k]:
                                sum += ct[p]
                        q2 += sum
            else:
                for k in range(len(K)):
                    if k != j:
                        ct = {'i':0.0, 'p+':0.0, 'p-':0.0, 'j':0.0}
                        for l in range(len(K[k])):
                            ct['i'] += self.R[o][K[k][l]]['i']
                            ct['p+'] += self.R[o][K[k][l]]['p+']
                            ct['p-'] += self.R[o][K[k][l]]['p-']
                            ct['j'] += self.R[o][K[k][l]]['j']
                        max = ct[self.Q[0]]
                        sum = 0
                        for p in self.Q:
                            sum += ct[p]
                            if max < ct[p]:
                                max = ct[p]
                        q2 += (sum - max) 
                
                    
            n[0] += (q1-q2)
            
        return N
