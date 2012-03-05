import os
import sys
import getopt
import subprocess

import PyXMCDA

from ClustersRelationSummary import *

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
        if not os.path.isfile (in_dir+"/alternativesAffectations.xml"):
            errorList.append("alternativesAffectations.xml is missing")

    if not errorList:
        # We parse all the mandatory input files
        xmltree_alternatives = PyXMCDA.parseValidate(in_dir+"/alternatives.xml")
        xmltree_preferenceRelation = PyXMCDA.parseValidate(in_dir+"/preferenceRelation.xml")
        xmltree_alternativesAffectations = PyXMCDA.parseValidate(in_dir+"/alternativesAffectations.xml")
        
        # We check if all mandatory input files are valid
        if xmltree_alternatives == None :
            errorList.append("alternatives.xml can't be validated.")
        if xmltree_preferenceRelation == None :
            errorList.append("preferenceRelation.xml can't be validated.")
        if xmltree_alternativesAffectations == None :
            errorList.append("alternativesAffectations.xml can't be validated.")
            
        if not errorList :

            alternativesId = PyXMCDA.getAlternativesID(xmltree_alternatives)
            alternativesRel = PyXMCDA.getAlternativesComparisonsValues(xmltree_preferenceRelation, alternativesId)
            
            if not alternativesId :
                errorList.append("No active alternatives found.")
            if not alternativesRel :
                errorList.append("Problems between relation and alternatives.")
            missing_eval = False
            for o in alternativesId:
                if not (o in alternativesRel):
                    missing_eval = True
                    break
                else:
                    for p in alternativesId:
                        if not (p in alternativesRel[o]):
                            missing_eval = True
                            break
                        else:
                            if not ('i' in alternativesRel[o][p]):
                                missing_eval = True
                                break
                            if not ('p+' in alternativesRel[o][p]):
                                missing_eval = True
                                break
                            if not ('p-' in alternativesRel[o][p]):
                                missing_eval = True
                                break
                            if not ('j' in alternativesRel[o][p]):
                                missing_eval = True
                                break
            if missing_eval:
                errorList.append("Not all alternatives from alternatives.xml contain evaluations in preferenceRelation.xml, or evaluations are incomplete. Possible inputs from different sources")
                
            alternativesAffectations = PyXMCDA.getAlternativesAffectations(xmltree_alternativesAffectations)
            Knames = []
            for o in alternativesId:
                clusterId = alternativesAffectations[o]
                if not (clusterId in Knames):
                    Knames.append(clusterId)
            
            if Knames == []:
                errorList.append("No clusters found.")
                
            K = {}
            for clusterId in Knames:
                K[clusterId] = []
            for o in alternativesId:
                K[alternativesAffectations[o]].append(o)

            if not errorList :
                CRS = ClustersRelationSummary(alternativesId, alternativesRel)
                RKsum = CRS.RKSummary(K)
            
                L = ['i','p+','p-','j']
            
                fo = open(out_dir+"/clustersRelationsDetailed.xml",'w')
                PyXMCDA.writeHeader(fo)
                fo.write('<categoriesComparisons>\n')
                fo.write('\t<pairs>\n')
                for i in Knames:
                    for j in Knames:
                        fo.write('\t\t<pair>\n')
                        fo.write('\t\t\t<initial>\n')
                        fo.write('\t\t\t\t<categoryID>'+i+'</categoryID>\n')
                        fo.write('\t\t\t</initial>\n')
                        fo.write('\t\t\t<terminal>\n')
                        fo.write('\t\t\t\t<categoryID>'+j+'</categoryID>\n')
                        fo.write('\t\t\t</terminal>\n')
                        fo.write('\t\t\t<values>\n')
                        for l in L:
                            fo.write('\t\t\t\t<value id="'+ l +'">\n')
                            fo.write('\t\t\t\t\t<real>'+str(RKsum[i][j][l])+'</real>\n')
                            fo.write('\t\t\t\t</value>\n')
                        fo.write('\t\t\t</values>\n')
                        fo.write('\t\t</pair>\n')
                fo.write('\t</pairs>\n')
                fo.write('</categoriesComparisons>\n')
                PyXMCDA.writeFooter(fo)
                fo.close()
                
            
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


            
