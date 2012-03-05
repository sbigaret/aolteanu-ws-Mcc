import os
import sys
import getopt
import subprocess

import PyXMCDA

from PreferenceRelation import *

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
        if not os.path.isfile (in_dir+"/alternativesComparisons.xml"):
            errorList.append("alternativesComparisons.xml is missing")
        if not os.path.isfile (in_dir+"/methodParameters.xml"):
            errorList.append("methodParameters.xml is missing")

    if not errorList:
        # We parse all the mandatory input files
        xmltree_alternatives = PyXMCDA.parseValidate(in_dir+"/alternatives.xml")
        xmltree_alternativesComparisons = PyXMCDA.parseValidate(in_dir+"/alternativesComparisons.xml")
        xmltree_methodParameters = PyXMCDA.parseValidate(in_dir+"/methodParameters.xml")
        
        # We check if all mandatory input files are valid
        if xmltree_alternatives == None :
            errorList.append("alternatives.xml can't be validated.")
        if xmltree_alternativesComparisons == None :
            errorList.append("alternativesComparisons.xml can't be validated.")
        if xmltree_methodParameters == None :
            errorList.append("methodParameters.xml can't be validated.")
            
        if not errorList :

            alternativesId = PyXMCDA.getAlternativesID(xmltree_alternatives)
            alternativesRel = PyXMCDA.getAlternativesComparisons (xmltree_alternativesComparisons, alternativesId)
            bipolar = PyXMCDA.getParameterByName(xmltree_methodParameters, "bipolar")
            cutlvl = PyXMCDA.getParameterByName(xmltree_methodParameters, "cutlvl")

            if not alternativesId :
                errorList.append("No active alternatives found.")
            if not alternativesRel :
                errorList.append("Problems between relation and alternatives.")
            if not bipolar:
                errorList.append("No bipolar parameter found.")
            if not cutlvl:
                errorList.append("No cutlvl parameter found.")
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
            if missing_eval:
                errorList.append("Not all alternatives from alternatives.xml contain evaluations in alternativesComparisons.xml. Possible inputs from different sources.")

        if not errorList :
            
            PR = PreferenceRelation(alternativesId, alternativesRel, bipolar, cutlvl)
            R = PR.ExtractR()
            L = ['i','p+','p-','j']
            
            fo = open(out_dir+"/preferenceRelation.xml",'w')
            PyXMCDA.writeHeader(fo)
            fo.write('<alternativesComparisons>\n')
            fo.write('\t<pairs>\n')
            for o in alternativesId:
                for p in alternativesId:
                    fo.write('\t\t<pair>\n')
                    fo.write('\t\t\t<initial>\n')
                    fo.write('\t\t\t\t<alternativeID>'+o+'</alternativeID>\n')
                    fo.write('\t\t\t</initial>\n')
                    fo.write('\t\t\t<terminal>\n')
                    fo.write('\t\t\t\t<alternativeID>'+p+'</alternativeID>\n')
                    fo.write('\t\t\t</terminal>\n')
                    fo.write('\t\t\t<values>\n')
                    for i in range(4):
                        fo.write('\t\t\t\t<value id="'+ L[i] +'">\n')
                        fo.write('\t\t\t\t\t<real>'+str(R[o][p][i])+'</real>\n')
                        fo.write('\t\t\t\t</value>\n')
                    fo.write('\t\t\t</values>\n')
                    fo.write('\t\t</pair>\n')
            fo.write('\t</pairs>\n')
            fo.write('</alternativesComparisons>\n')
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


            
