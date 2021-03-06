import glob
import csv
import os
import re


def parse_each_file(file):
    """Gets the name of the file and the citations specified in the file

    Returns
    -------
    str
        Returns a comma-delimited format of the file name, list of citations, and their descriptions
    """
    listOfCitations = ""
    citationsList = [];
    circumstanceStr = ""
    flag = False

    with open(file, 'rt', encoding="utf8") as fd:
        lineContents = fd.readlines()
        contents = "".join(lineContents)
        # Name Processing
        name = os.path.basename(fd.name).strip(".txt")


        # Citation Processing
        citMatches = re.findall(r'310 CMR 40.\d\d\d\d', contents);
        for m in citMatches:
            citationsList.append(m.replace(",", "."))

        uniqueCitations = set(citationsList)

        first = True
        for uc in uniqueCitations:
            if first:
                first = False
                listOfCitations = uc
            else:
                listOfCitations = listOfCitations + " / " + uc

        # Circumstance Processing

        #cirMatches = re.findall(r'DESCRIPTION OF ACT', contents);
        #print(len(cirMatches))
        #cirEndMatches = re.findall(r'DESCRIPTION OF REQ', contents);
        #print(len(cirEndMatches))

        for line in lineContents:
            if(re.match(r'DES', line)):
                flag = False
            if (re.match(r'DESCRIPTION OF ACT', line)):
                flag = True
            if(flag):
                circumstanceStr += line
        circumstanceStr.rstrip();
    return name,listOfCitations,circumstanceStr

def produce_csv(folder_path, output_filename):
    """Produces a csv of file name, citations and descriptions of a folder with text files

    Parameters
    ----------
    folder_path : str
        String representation of the folder path containing the text files.
    output_filename : str
        Name of the output file the merged lines will be written to.
    """
    # make sure there's a slash to the folder path
    folder_path += "" if folder_path[-1] == "/" else "/"
    # get all text files
    txt_files = glob.glob(folder_path + "*.txt")

    # write to file
    csvex = csv.writer(open(folder_path + output_filename, "wt"))
    headers = ['file name', 'citation', 'description']
    csvex.writerow(headers)

    for f in txt_files:
        s = parse_each_file(f)
        print(s)
        csvex.writerow(s)

produce_csv(r"C:\Users\Achu\PycharmProjects\NONs_txt_split\NONs_txt_split\DESCRIPTION OF ACTIVITY OR OMISSION CONSTITUTING NONCOMPLIANCE", r"\output")
