import string
import sys # for listing directory contents
import re



if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    InputFilePath=sys.argv[1]
    OutputFilePath=sys.argv[2]
    
    InputFile = open(InputFilePath, 'r')
    OutputFile = open(OutputFilePath, 'w')
    OutputFile.write("<settings>\n")
    OutputFile.write("<sageinput>\n")
    for line in InputFile:
        pattern = re.compile(r"""\#\s*
                                (?P<Index>\d*)\s*
                                (?P<FieldName>\w*)\s*
                                (?P<DataType>\w)\s*
                                (?P<Desc1>[a-zA-Z0-9_\.\s\/\\\(\)]*)?
                                (?P<Units>\[[a-zA-Z0-9_\.\/\\\]]*[ ]?[a-zA-Z0-9_\.\/\\\]]*)?
                                (?P<Desc2>[a-zA-Z0-9_\.\s\/\\\(\)]*)?
                                """, re.VERBOSE)
        match = pattern.match(line)
        DescTxt=(match.group("Desc1")+match.group("Desc2")).strip()
        FieldStr= "<Field Type=\""+match.group("DataType")+"\""
        if match.group("Units")!=None:
            FieldStr=FieldStr+" Units=\""+match.group("Units").strip("[]")+"\""
        if DescTxt!="":
            FieldStr=FieldStr+" Desc=\""+DescTxt+"\""
        FieldStr=FieldStr+">"+match.group("FieldName")+"</Field>"
        OutputFile.write(FieldStr+"\n")
    OutputFile.write("</sageinput>\n")
    OutputFile.write("</settings>")
    OutputFile.close()
    InputFile.close()
        