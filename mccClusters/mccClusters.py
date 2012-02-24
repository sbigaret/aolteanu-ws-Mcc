import os
import sys
import getopt
import subprocess

import PyXMCDA

from Mcc import *

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
        if not os.path.isfile (in_dir+"/methodParameters.xml"):
            errorList.append("methodParameters.xml is missing")

    if not errorList:
        # We parse all the mandatory input files
        xmltree_alternatives = PyXMCDA.parseValidate(in_dir+"/alternatives.xml")
        xmltree_preferenceRelation = PyXMCDA.parseValidate(in_dir+"/preferenceRelation.xml")
	xmltree_methodParameters = PyXMCDA.parseValidate(in_dir+"/methodParameters.xml")
        
        # We check if all mandatory input files are valid
        if xmltree_alternatives == None :
            errorList.append("alternatives.xml can't be validated.")
        if xmltree_preferenceRelation == None :
            errorList.append("preferenceRelation.xml can't be validated.")
        if xmltree_methodParameters == None :
            errorList.append("methodParameters.xml can't be validated.")
            
        if not errorList :

            alternativesId = PyXMCDA.getAlternativesID(xmltree_alternatives)
            alternativesRel = PyXMCDA.getAlternativesComparisonsValues(xmltree_preferenceRelation, alternativesId)
	    method_type = PyXMCDA.getParameterByName(xmltree_methodParameters, "type")

            if not alternativesId :
                errorList.append("No active alternatives found.")
            if not alternativesRel :
                errorList.append("Problems between relation and alternatives.")
	    if not method_type:
                errorList.append("No method type found.")

        if not errorList :
            
            alg = Mcc(alternativesId, alternativesRel, method_type)
            K, RK = alg.Run()
            
            fo = open(out_dir+"/clusters.xml",'w')
            PyXMCDA.writeHeader(fo)
            fo.write('<categories>\n')
            for i in range(len(K)):
                fo.write('\t<category id="'+str(i+1)+'"/>\n')
            fo.write('</categories>\n')
            fo.write('<alternativesAffectations>\n')
            for i in range(len(K)):
                for o in K[i]:
                    fo.write('\t<alternativeAffectation>\n\t\t<alternativeID>'+o+'</alternativeID>\n\t\t<categoryID>'+str(i+1)+'</categoryID>\n\t</alternativeAffectation>\n')
            fo.write('</alternativesAffectations>')
            PyXMCDA.writeFooter(fo)
            fo.close()
            
            fo = open(out_dir+"/clustersRelations.xml",'w')
            PyXMCDA.writeHeader(fo)
            fo.write('<categoriesComparisons>\n')
            fo.write('\t<pairs>\n')
            for i in range(len(K)):
                for j in range(len(K)):                        
                    fo.write('\t\t<pair>\n')
                    fo.write('\t\t\t<initial>\n')
                    fo.write('\t\t\t\t<categoryID>'+str(i+1)+'</categoryID>\n')
                    fo.write('\t\t\t</initial>\n')
                    fo.write('\t\t\t<terminal>\n')
                    fo.write('\t\t\t\t<categoryID>'+str(j+1)+'</categoryID>\n')
                    fo.write('\t\t\t</terminal>\n')
                    fo.write('\t\t\t<value>\n')
                    fo.write('\t\t\t\t<label>'+RK[i][j]+'</label>\n')
                    fo.write('\t\t\t</value>\n')
                    fo.write('\t\t</pair>\n')
            fo.write('\t</pairs>\n')
            fo.write('</categoriesComparisons>')
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


            
