import os
import sys
import getopt
import subprocess

import PyXMCDA
import base64

from PlotClusters import *

from optparse import OptionParser

def main(argv=None):
    
    if argv is None:
        argv = sys.argv
        
    parser = OptionParser()

    parser.add_option("-i", "--in", dest="in_dir")
    parser.add_option("-o", "--out", dest="out_dir")

    (options, args) = parser.parse_args(argv[1:])

    in_dir = options.in_dir
    out_dir = options.out_dir

    # Creating a list for error messages
    errorList = []
    
    if not in_dir:
        errorList.append("option --in is missing")
    if not out_dir:
        errorList.append("option --out is missing")
    
    if not errorList:
        if not os.path.isfile (in_dir+"/alternatives.xml"):
            errorList.append("alternatives.xml is missing")
        if not os.path.isfile (in_dir+"/preferenceRelation.xml"):
            errorList.append("preferenceRelation.xml is missing")
        if not os.path.isfile (in_dir+"/clusters.xml"):
            errorList.append("clusters.xml is missing")
        if not os.path.isfile (in_dir+"/alternativesAffectations.xml"):
            errorList.append("alternativesAffectations.xml is missing")
        if not os.path.isfile (in_dir+"/clustersRelations.xml"):
            errorList.append("clustersRelations.xml is missing")
        if not os.path.isfile (in_dir+"/clustersRelationsDetailed.xml"):
            errorList.append("clustersRelationsDetailed.xml is missing")

    if not errorList:
        # We parse all the mandatory input files
        xmltree_alternatives = PyXMCDA.parseValidate(in_dir+"/alternatives.xml")
        xmltree_preferenceRelation = PyXMCDA.parseValidate(in_dir+"/preferenceRelation.xml")
        xmltree_clusters = PyXMCDA.parseValidate(in_dir+"/clusters.xml")
        xmltree_alternativesAffectations = PyXMCDA.parseValidate(in_dir+"/alternativesAffectations.xml")
        xmltree_clustersRelations = PyXMCDA.parseValidate(in_dir+"/clustersRelations.xml")
        xmltree_clustersRelationsDetailed = PyXMCDA.parseValidate(in_dir+"/clustersRelationsDetailed.xml")
        
        # We check if all mandatory input files are valid
        if xmltree_alternatives == None :
            errorList.append("alternatives.xml can't be validated.")
        if xmltree_preferenceRelation == None :
            errorList.append("preferenceRelation.xml can't be validated.")
        if xmltree_clusters == None :
            errorList.append("clusters.xml can't be validated.")
        if xmltree_alternativesAffectations == None :
            errorList.append("alternativesAffectations.xml can't be validated.")
        if xmltree_clustersRelations == None :
            errorList.append("clustersRelations.xml can't be validated.")
        if xmltree_clustersRelationsDetailed == None :
            errorList.append("clustersRelationsDetailed.xml can't be validated.")
            
        if not errorList :

            alternativesId = PyXMCDA.getAlternativesID(xmltree_alternatives)
            alternativesRel = PyXMCDA.getAlternativesComparisonsValues(xmltree_preferenceRelation, alternativesId)
            clustersId = PyXMCDA.getCategoriesID(xmltree_clusters)
            alternativesAffectations = PyXMCDA.getAlternativesAffectations(xmltree_alternativesAffectations)
            K = {}
            for cid in clustersId:
                K[cid] = []
            for o in alternativesId:
                K[alternativesAffectations[o]].append(o)
            clustersRel = PyXMCDA.getCategoriesComparisonsValues(xmltree_clustersRelations, clustersId)
            RK = {}
            for cid1 in clustersId:
                RK[cid1] = {}
                for cid2 in clustersId:
                    if cid1 == cid2:
                        RK[cid1][cid2] = 'i'
                    else:
                        RK[cid1][cid2] = ''
            for cid1 in clustersId:
                for cid2 in clustersId:
                    if cid1 != cid2:
                        if cid1 in clustersRel:
                            if cid2 in clustersRel[cid1]:
                                RK[cid1][cid2] = clustersRel[cid1][cid2]
                        if cid2 in clustersRel:
                            if cid1 in clustersRel[cid2]:
                                if clustersRel[cid2][cid1] == 'p+':
                                    RK[cid1][cid2] = 'p-'
                                elif clustersRel[cid2][cid1] == 'p-':
                                    RK[cid1][cid2] = 'p+'
                                else:
                                    RK[cid1][cid2] = clustersRel[cid2][cid1]
            RKsum = PyXMCDA.getCategoriesComparisonsAllValues(xmltree_clustersRelationsDetailed, clustersId)

            if not alternativesId :
                errorList.append("No active alternatives found.")
            if not alternativesRel :
                errorList.append("Problems between relation and alternatives.")
            if not clustersId :
                errorList.append("Problems finding clusters names.")
            if not K :
                errorList.append("Problems with alternatives affectations.")
            if not RK :
                errorList.append("Problems with clusters relations.")
            if not RKsum :
                errorList.append("Problems with detailed clusters relations.")

        if not errorList :
            PC = PlotClusters(alternativesId, alternativesRel, clustersId, K, RK, RKsum)
            try:
                PC.PlotKideal(out_dir)
                fo = open(out_dir+"/Kideal.xml",'w')
                PyXMCDA.writeHeader(fo)
                fo.write('<alternativeValue mcdaConcept="Ideal Relations between Clusters">\n')
                fo.write('\t<value>\n')
                fo.write('\t\t<image>')
                fo.write(base64.b64encode(open(out_dir+"/Kideal.png","rb").read()))
                fo.write('</image>\n')
                fo.write('\t</value>\n')
                fo.write('</alternativeValue>\n')
                PyXMCDA.writeFooter(fo)
                fo.close()
                os.remove(out_dir+'/Kideal.png')
                
                PC.PlotKreal(out_dir)
                fo = open(out_dir+"/Kreal.xml",'w')
                PyXMCDA.writeHeader(fo)
                fo.write('<alternativeValue mcdaConcept="Real Relations between Clusters">\n')
                fo.write('\t<value>\n')
                fo.write('\t\t<image>')
                fo.write(base64.b64encode(open(out_dir+"/Kreal.png","rb").read()))
                fo.write('</image>\n')
                fo.write('\t</value>\n')
                fo.write('</alternativeValue>\n')
                PyXMCDA.writeFooter(fo)
                fo.close()
                os.remove(out_dir+'/Kreal.png')
                
                PC.PlotKidealsum(out_dir)
                fo = open(out_dir+"/Kidealsum.xml",'w')
                PyXMCDA.writeHeader(fo)
                fo.write('<alternativeValue mcdaConcept="Summary of Ideal Relations between Clusters">\n')
                fo.write('\t<value>\n')
                fo.write('\t\t<image>')
                fo.write(base64.b64encode(open(out_dir+"/Kidealsum.png","rb").read()))
                fo.write('</image>\n')
                fo.write('\t</value>\n')
                fo.write('</alternativeValue>\n')
                PyXMCDA.writeFooter(fo)
                fo.close()
                os.remove(out_dir+'/Kidealsum.png')
                
                PC.PlotKrealsum(out_dir)      
                fo = open(out_dir+"/Krealsum.xml",'w')
                PyXMCDA.writeHeader(fo)
                fo.write('<alternativeValue mcdaConcept="Summary of Real Relations between Clusters">\n')
                fo.write('\t<value>\n')
                fo.write('\t\t<image>')
                fo.write(base64.b64encode(open(out_dir+"/Krealsum.png","rb").read()))
                fo.write('</image>\n')
                fo.write('\t</value>\n')
                fo.write('</alternativeValue>\n')
                PyXMCDA.writeFooter(fo)
                fo.close()
                os.remove(out_dir+'/Krealsum.png')              

            except Exception as e:
                import traceback
                traceback.print_exc()
                errorList.append("Could not plot clusters.")
            
        # Creating log and error file, messages.xml
        fileMessages = open(out_dir+"/messages.xml", 'w')
        PyXMCDA.writeHeader (fileMessages)

        if not errorList :
            PyXMCDA.writeLogMessages (fileMessages, ["Execution ok"])
        else :
            PyXMCDA.writeErrorMessages (fileMessages, errorList)

        PyXMCDA.writeFooter(fileMessages)
        fileMessages.close()

if __name__ == "__main__":
    sys.exit(main())


            

