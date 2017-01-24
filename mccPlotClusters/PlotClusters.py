import math, subprocess, os

def fix_neato_lines(lines):
    """Makes all lines contains '[' and '];'.

    Older versions of neato (ex. graphviz version 2.26.3 (20100126.1600))
    put all on the same lines, while newer ones do not.

    Example: old::

        graph G {
            graph [ratio=1, size="14,14!"];
            node [label="\N", shape=circle];
            graph [bb="0,0,516.03,505"];
            1 [pos="52.028,471", width="0.5", height="0.51389"];

    new::

         graph G {
            graph [bb="-99,-99,155.83,154.21",
                   ratio=1,
                   size="14,14!"
            ];
            node [label="\N",
                  shape=circle
            ];
            1 [height=0.5,
               pos="53.787,88.226",
               width=0.5];

    Since the functions PlotKidealsum() and PlotKrealsum are based on the old
    way, it is necessary to filter the output of a newer neato before using it.
    """
    out = []
    out_line = ''
    out.append(lines[0]) # 1st line graph { left as-is
    for line in lines[1:]:
        out_line += line.strip()
        if '];' in line:
            out_line += '\n'
            out.append(out_line)
            out_line=''
            continue
    if out_line != '':
        out.append(out_line)
    return out


class PlotClusters(object):
    def __init__(self, objects, R, K_names, K, RK, RKdet):

        self.objects = objects
        self.N = len(objects)
        self.R = R
        self.K_names = K_names
        self.K = K
        self.RK = RK
        self.RKdet = RKdet

    def PlotKideal(self, dir):

        sz = 700
        opos = {}
        cluster_width = {}
        sumwidth = 0.0
        for kname in self.K_names:
            n = len(self.K[kname])
            width = 0
            if n > 1:
                ct = 0.0
                for o in self.K[kname]:
                    opos[o] = [1 * math.cos(ct*3.14*2/n),1 * math.sin(ct*3.14*2/n)]
                    ct += 1
                dist = ((opos[self.K[kname][0]][0] - opos[self.K[kname][1]][0])**2+(opos[self.K[kname][0]][1] - opos[self.K[kname][1]][1])**2)**0.5
                if dist < 120:
                    fact = 120/dist
                    for o in self.K[kname]:
                        opos[o][0] *= fact
                        opos[o][1] *= fact
                width = ((opos[self.K[kname][0]][0])**2+(opos[self.K[kname][0]][1])**2)**0.5
            else:
                opos[self.K[kname][0]] = [0,0]
            if width < 50:
                width = 50
            cluster_width[kname] = width
            sumwidth += width
        Kpos = {}
        ct = 0.0
        for kname in self.K_names:
            ct += cluster_width[kname]/2.0
            Kpos[kname] = [200 * math.cos(ct*3.14*2/sumwidth),200 * math.sin(ct*3.14*2/sumwidth)]
            ct += cluster_width[kname]/2.0
        if len(self.K_names) > 1:
            mindist = float('inf')
            for i in range(len(self.K_names))[1:]:
                dist = ((Kpos[self.K_names[i-1]][0]-Kpos[self.K_names[i]][0])**2+(Kpos[self.K_names[i-1]][1]-Kpos[self.K_names[i]][1])**2)**0.5
                if mindist > dist:
                    mindist = dist
            if mindist < 250:
                fact = 250.0/mindist
                sz *= fact
                for kname in self.K_names:
                    Kpos[kname][0] *= fact
                    Kpos[kname][1] *= fact
        object_positions = {}
        for kname in self.K_names:
            cluster = self.K[kname]
            avg_x = 0
            avg_y = 0
            for o in cluster:
                avg_x += opos[o][0]
                avg_y += opos[o][1]
            avg_x /= float(len(cluster))
            avg_y /= float(len(cluster))
            for o in cluster:
                object_positions[o] = (Kpos[kname][0] + avg_x - opos[o][0],Kpos[kname][1] + avg_y - opos[o][1])
        # load asy template
        fileNameExt = 'templateKideal.asy'
        fo = open(fileNameExt, 'r')
        template = fo.readlines()
        fo.close()
        # write asy file
        fileNameExt = dir+'/Kideal.asy'
        fo = open(fileNameExt, 'w')
        # get arcs
        no_arcs = 0
        for kname in self.K_names:
            no_arcs += (len(self.K[kname]))*(len(self.K[kname])-1)/2
        fo.write('int sz = %d;'%sz)
        fo.write('int no_arcs = %d;\n'%no_arcs)
        fo.write('int no_cluster_arcs = %d;\n'%((len(self.K_names))*(len(self.K_names)-1)/2))
        line = 'real[] arcs_x1={'
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    line += str(object_positions[self.K[kname][i]][0])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] arcs_x2={'
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    line += str(object_positions[self.K[kname][j]][0])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] arcs_y1={'
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    line += str(object_positions[self.K[kname][i]][1])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] arcs_y2={'
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    line += str(object_positions[self.K[kname][j]][1])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_x1={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(Kpos[self.K_names[i]][0])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_x2={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(Kpos[self.K_names[j]][0])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_y1={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(Kpos[self.K_names[i]][1])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_y2={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(Kpos[self.K_names[j]][1])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_z1={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(cluster_width[self.K_names[i]])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arcs_z2={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                line += str(cluster_width[self.K_names[j]])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] arc_type={'
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    line += '0,'
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] cluster_arc_type={'
        for i in range(len(self.K_names)-1):
            for j in range(len(self.K_names))[i+1:]:
                if self.RK[self.K_names[i]][self.K_names[j]] == 'i':
                    line += '0,'
                elif self.RK[self.K_names[i]][self.K_names[j]] == 'p+':
                    line += '1,'
                elif self.RK[self.K_names[i]][self.K_names[j]] == 'p-':
                    line += '2,'
                else:
                    line += '3,'
        line = line[:-1]+'};'
        fo.write(line+'\n')
        # get point positions
        no_points = 0
        for kname in self.K_names:
            no_points += len(self.K[kname])
        fo.write('int no_points = %d;\n'%no_points)
        line1 = 'real[] points_x={'
        line2 = 'real[] points_y={'
        line3 = 'string[] labels={'
        for kname in self.K_names:
            for o in self.K[kname]:
                line1 += str(object_positions[o][0]) + ','
                line2 += str(object_positions[o][1]) + ','
                line3 += '"'+o+'",'
        fo.write(line1[:-1]+'};\n')
        fo.write(line2[:-1]+'};\n')
        fo.write(line3[:-1]+'};\n')

        for line in template:
            fo.write(line)
        fo.close()

        subprocess.call(["asy","-noV","-cd",dir,"Kideal.asy"])

    def PlotKreal(self, dir):

        sz = 700
        opos = {}
        cluster_width = {}
        sumwidth = 0.0
        for kname in self.K_names:
            n = len(self.K[kname])
            width = 0
            if n > 1:
                ct = 0.0
                for o in self.K[kname]:
                    opos[o] = [1 * math.cos(ct*3.14*2/n),1 * math.sin(ct*3.14*2/n)]
                    ct += 1
                dist = ((opos[self.K[kname][0]][0] - opos[self.K[kname][1]][0])**2+(opos[self.K[kname][0]][1] - opos[self.K[kname][1]][1])**2)**0.5
                if dist < 120:
                    fact = 120/dist
                    for o in self.K[kname]:
                        opos[o][0] *= fact
                        opos[o][1] *= fact
                width = ((opos[self.K[kname][0]][0])**2+(opos[self.K[kname][0]][1])**2)**0.5
            else:
                opos[self.K[kname][0]] = [0,0]
            if width < 50:
                width = 50
            cluster_width[kname] = width
            sumwidth += width
        Kpos = {}
        ct = 0.0
        for kname in self.K_names:
            ct += cluster_width[kname]/2.0
            Kpos[kname] = [200 * math.cos(ct*3.14*2/sumwidth),200 * math.sin(ct*3.14*2/sumwidth)]
            ct += cluster_width[kname]/2.0
        if len(self.K_names) > 1:
            mindist = float('inf')
            for i in range(len(self.K_names))[1:]:
                dist = ((Kpos[self.K_names[i-1]][0]-Kpos[self.K_names[i]][0])**2+(Kpos[self.K_names[i-1]][1]-Kpos[self.K_names[i]][1])**2)**0.5
                if mindist > dist:
                    mindist = dist
            if mindist < 250:
                fact = 250.0/mindist
                sz *= fact
                for kname in self.K_names:
                    Kpos[kname][0] *= fact
                    Kpos[kname][1] *= fact
        object_positions = {}
        for kname in self.K_names:
            cluster = self.K[kname]
            avg_x = 0
            avg_y = 0
            for o in cluster:
                avg_x += opos[o][0]
                avg_y += opos[o][1]
            avg_x /= float(len(cluster))
            avg_y /= float(len(cluster))
            for o in cluster:
                object_positions[o] = (Kpos[kname][0] + avg_x - opos[o][0],Kpos[kname][1] + avg_y - opos[o][1])
        # load asy template
        fileNameExt = 'templateKreal.asy'
        fo = open(fileNameExt, 'r')
        template = fo.readlines()
        fo.close()
        # write asy file
        fileNameExt = dir+'/Kreal.asy'
        fo = open(fileNameExt, 'w')
        # get arcs
        fo.write('int sz = %d;'%sz)
        fo.write('int no_obj = %d;\n'%self.N)
        line = 'real[] obj_x={'
        for i in range(self.N):
                line += str(object_positions[self.objects[i]][0])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] obj_y={'
        for i in range(self.N):
                line += str(object_positions[self.objects[i]][1])+','
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'real[] arc_type={'
        for i in range(self.N - 1):
            for j in range(self.N)[i+1:]:
                if self.R[self.objects[i]][self.objects[j]]['i'] == 1.0:
                    line += '0,'
                elif self.R[self.objects[i]][self.objects[j]]['p+'] == 1.0:
                    line += '1,'
                elif self.R[self.objects[i]][self.objects[j]]['p-'] == 1.0:
                    line += '2,'
                elif self.R[self.objects[i]][self.objects[j]]['j'] == 1.0:
                    line += '3,'
                else:
                    line += '3,'
        line = line[:-1]+'};'
        fo.write(line+'\n')
        line = 'string[] labels={'
        for i in range(self.N):
            line += '"'+self.objects[i]+'",'
        fo.write(line[:-1]+'};\n')

        for line in template:
            fo.write(line)
        fo.close()

        subprocess.call(["asy","-noV","-cd",dir,"Kreal.asy"])

    def PlotKidealsum(self, dir):

        # write dot file
        sz = 700
        fileNameExt = dir+'/Kidealsum.dot'
        fo = open(fileNameExt, 'w')
        fo.write('graph G{\n')
        fo.write('ratio=1;\n')
        fo.write('size="%d,%d!";\n'%(self.N,self.N))
        fo.write('node [shape = circle];\n')
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    fo.write('%s -- %s;\n'%(str(self.objects.index(self.K[kname][i])),str(self.objects.index(self.K[kname][j]))))
        for i in range(self.N):
            fo.write('%s;\n'%str(i))
        fo.write('}')
        fo.close()
        # execute neato
        fi = dir+'/Kidealsum.dot'
        fo = dir+'/Kidealsum.txt'
        subprocess.call(["neato",fi,"-o"+fo])
        # remove dot file
        os.remove(fi)
        # read neato result
        fileNameExt = dir+'/Kidealsum.txt'
        fo = open(fileNameExt, 'r')
        lines = fo.readlines()
        #
        lines = fix_neato_lines(lines)
        fo.close()
        # remove neato result file
        os.remove(fileNameExt)
        # get node positions
        positions = {}
        for line in lines:
            # ignore every line not starting with a number
            if line.strip()[0] not in ('0','1','2','3','4','5','6','7','8','9'):
                continue
            Y = line.split()
            if Y[1] != '--':
                positions[self.objects[int(Y[0])]] = (2*float(Y[1].split('"')[1].split(',')[0]),2*float(Y[1].split('"')[1].split(',')[1]))
        #get cluster width
        cluster_width = {}
        sumwidth = 0.0
        for kname in self.K_names:
            cluster = self.K[kname]
            avg_x = 0
            avg_y = 0
            for o in cluster:
                avg_x += positions[o][0]
                avg_y += positions[o][1]
            avg_x /= float(len(cluster))
            avg_y /= float(len(cluster))
            width = 0
            for o in cluster:
                dist = ((avg_x - positions[o][0])**2 + (avg_y - positions[o][1])**2)**0.5
                if dist > width:
                    width = dist
            if width < 50:
                width = 50
            cluster_width[kname] = width
            sumwidth += width
        Kpos = {}
        ct = 0.0
        for kname in self.K_names:
            ct += cluster_width[kname]/2.0
            Kpos[kname] = [200 * math.cos(ct*3.14*2/sumwidth),200 * math.sin(ct*3.14*2/sumwidth)]
            ct += cluster_width[kname]/2.0
        if len(self.K_names) > 1:
            mindist = float('inf')
            for i in range(len(self.K_names))[1:]:
                dist = ((Kpos[self.K_names[i-1]][0]-Kpos[self.K_names[i]][0])**2+(Kpos[self.K_names[i-1]][1]-Kpos[self.K_names[i]][1])**2)**0.5
                if mindist > dist:
                    mindist = dist
            if mindist < 250:
                fact = 250.0/mindist
                sz *= fact
                for kname in self.K_names:
                    Kpos[kname][0] *= fact
                    Kpos[kname][1] *= fact
        # load asy template
        fileNameExt = 'templateKsum.asy'
        fo = open(fileNameExt, 'r')
        template = fo.readlines()
        fo.close()
        # write asy file
        fileNameExt = dir+'/Kidealsum.asy'
        fo = open(fileNameExt, 'w')
        fo.write('int sz = %d;'%sz)
        fo.write('int no_clusters = %d;\n'%len(self.K_names))
        line = 'string[] cluster_name={'
        for kname in self.K_names:
            line += '"' + kname + '"' + ','
        fo.write(line[:-1]+'};\n')
        line1 = 'real[] cluster_x={'
        line2 = 'real[] cluster_y={'
        for kname in self.K_names:
            line1 += str(Kpos[kname][0])+','
            line2 += str(Kpos[kname][1])+','
        fo.write(line1[:-1]+'};\n')
        fo.write(line2[:-1]+'};\n')
        line1 = 'real[] cluster_i={'
        line2 = 'real[] cluster_p1={'
        line3 = 'real[] cluster_p2={'
        line4 = 'real[] cluster_j={'
        for k1 in range(len(self.K_names)):
            for k2 in range(len(self.K_names))[k1:]:
                if k1 == k2:
                    line1 += str(float(len(self.K[self.K_names[k1]])*(len(self.K[self.K_names[k1]])-1)/2))+','
                    line2 += str(0.0)+','
                    line3 += str(0.0)+','
                    line4 += str(0.0)+','
                else:
                    if self.RK[self.K_names[k1]][self.K_names[k2]] == 'i':
                        line1 += str(float(len(self.K[self.K_names[k1]])*len(self.K[self.K_names[k2]])))+','
                    else:
                        line1 += str(0.0)+','
                    if self.RK[self.K_names[k1]][self.K_names[k2]] == 'p+':
                        line2 += str(float(len(self.K[self.K_names[k1]])*len(self.K[self.K_names[k2]])))+','
                    else:
                        line2 += str(0.0)+','
                    if self.RK[self.K_names[k1]][self.K_names[k2]] == 'p-':
                        line3 += str(float(len(self.K[self.K_names[k1]])*len(self.K[self.K_names[k2]])))+','
                    else:
                        line3 += str(0.0)+','
                    if self.RK[self.K_names[k1]][self.K_names[k2]] == 'j':
                        line4 += str(float(len(self.K[self.K_names[k1]])*len(self.K[self.K_names[k2]])))+','
                    else:
                        line4 += str(0.0)+','
        fo.write(line1[:-1]+'};\n')
        fo.write(line2[:-1]+'};\n')
        fo.write(line3[:-1]+'};\n')
        fo.write(line4[:-1]+'};\n')

        for line in template:
            fo.write(line)
        fo.close()

        subprocess.call(["asy","-noV","-cd",dir,"Kidealsum.asy"])

    def PlotKrealsum(self, dir):

        # write dot file
        sz = 700
        fileNameExt = dir+'/Krealsum.dot'
        fo = open(fileNameExt, 'w')
        fo.write('graph G{\n')
        fo.write('ratio=1;\n')
        fo.write('size="%d,%d!";\n'%(self.N,self.N))
        fo.write('node [shape = circle];\n')
        for kname in self.K_names:
            for i in range(len(self.K[kname])-1):
                for j in range(len(self.K[kname]))[i+1:]:
                    fo.write('%s -- %s;\n'%(str(self.objects.index(self.K[kname][i])),str(self.objects.index(self.K[kname][j]))))
        for i in range(self.N):
            fo.write('%s;\n'%str(i))
        fo.write('}')
        fo.close()
        # execute neato
        fi = dir+'/Krealsum.dot'
        fo = dir+'/Krealsum.txt'
        subprocess.call(["neato",fi,"-o"+fo])
        # remove dot file
        os.remove(fi)
        # read neato result
        fileNameExt = dir+'/Krealsum.txt'
        fo = open(fileNameExt, 'r')
        lines = fo.readlines()
        fo.close()
        lines = fix_neato_lines(lines)
        # remove neato result file
        os.remove(fileNameExt)
        # get node positions
        positions = {}
        for line in lines:
            # ignore every line not starting with a number
            if line.strip()[0] not in ('0','1','2','3','4','5','6','7','8','9'):
                continue
            Y = line.split()
            if Y[1] != '--':
                positions[self.objects[int(Y[0])]] = (2*float(Y[1].split('"')[1].split(',')[0]),2*float(Y[1].split('"')[1].split(',')[1]))
        #get cluster width
        cluster_width = {}
        sumwidth = 0.0
        for kname in self.K_names:
            cluster = self.K[kname]
            avg_x = 0
            avg_y = 0
            for o in cluster:
                avg_x += positions[o][0]
                avg_y += positions[o][1]
            avg_x /= float(len(cluster))
            avg_y /= float(len(cluster))
            width = 0
            for o in cluster:
                dist = ((avg_x - positions[o][0])**2 + (avg_y - positions[o][1])**2)**0.5
                if dist > width:
                    width = dist
            if width < 50:
                width = 50
            cluster_width[kname] = width
            sumwidth += width
        Kpos = {}
        ct = 0.0
        for kname in self.K_names:
            ct += cluster_width[kname]/2.0
            Kpos[kname] = [200 * math.cos(ct*3.14*2/sumwidth),200 * math.sin(ct*3.14*2/sumwidth)]
            ct += cluster_width[kname]/2.0
        if len(self.K_names) > 1:
            mindist = float('inf')
            for i in range(len(self.K_names))[1:]:
                dist = ((Kpos[self.K_names[i-1]][0]-Kpos[self.K_names[i]][0])**2+(Kpos[self.K_names[i-1]][1]-Kpos[self.K_names[i]][1])**2)**0.5
                if mindist > dist:
                    mindist = dist
            if mindist < 250:
                fact = 250.0/mindist
                sz *= fact
                for kname in self.K_names:
                    Kpos[kname][0] *= fact
                    Kpos[kname][1] *= fact
        # load asy template
        fileNameExt = 'templateKsum.asy'
        fo = open(fileNameExt, 'r')
        template = fo.readlines()
        fo.close()
        # write asy file
        fileNameExt = dir+'/Krealsum.asy'
        fo = open(fileNameExt, 'w')
        fo.write('int sz = %d;'%sz)
        fo.write('int no_clusters = %d;\n'%len(self.K_names))
        line = 'string[] cluster_name={'
        for kname in self.K_names:
            line += '"' + kname + '"' + ','
        fo.write(line[:-1]+'};\n')
        line1 = 'real[] cluster_x={'
        line2 = 'real[] cluster_y={'
        for kname in self.K_names:
            line1 += str(Kpos[kname][0])+','
            line2 += str(Kpos[kname][1])+','
        fo.write(line1[:-1]+'};\n')
        fo.write(line2[:-1]+'};\n')
        line1 = 'real[] cluster_i={'
        line2 = 'real[] cluster_p1={'
        line3 = 'real[] cluster_p2={'
        line4 = 'real[] cluster_j={'
        for k1 in range(len(self.K_names)):
            for k2 in range(len(self.K_names))[k1:]:
                if k1 == k2:
                    line1 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['i'])+','
                    line2 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['p+']+self.RKdet[self.K_names[k1]][self.K_names[k2]]['p-'])+','
                    line3 += str(0.0)+','
                    line4 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['j'])+','
                else:
                    line1 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['i'])+','
                    line2 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['p+'])+','
                    line3 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['p-'])+','
                    line4 += str(self.RKdet[self.K_names[k1]][self.K_names[k2]]['j'])+','
        fo.write(line1[:-1]+'};\n')
        fo.write(line2[:-1]+'};\n')
        fo.write(line3[:-1]+'};\n')
        fo.write(line4[:-1]+'};\n')

        for line in template:
            fo.write(line)
        fo.close()

        subprocess.call(["asy","-noV","-cd",dir,"Krealsum.asy"])
