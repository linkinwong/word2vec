__author__ = 'linlin'
import os
import logging

parDir = os.path.dirname(os.getcwd())


logger = logging.getLogger(__name__)
def DirProcessing():
    path = parDir + "/expr_0112"
    for root, dirs, files in os.walk(path):
        for filespath in files:
            abs_file_path = os.path.join(root, filespath)
            logger.debug("Visited one file!")
            ProcessLastLabel(abs_file_path)

def ProcessLastLabel(path):
    output_path = parDir + "/" + os.path.basename(path) + '.preprocess'
    output_file_obj = open(output_path,'w')

    file_obj = open(path)

    for line in file_obj:
        if len(line)<3:
            newLine = ''
        elif ' filler' in line:
            newLine = line[:54] + 'filler'
        elif 'repeat/' in line:
            newLine = line[:54] + 'repeat'
        elif 'restart frag' in line or 'Sub ' in line or 'Insert ' in line:
            newLine = line[:54] + 'false_start'
        elif -1 != line.rfind('OK', 50):
            newLine = line[:54] + 'OK'
        elif 0 !=len(line[13:]):
            newLine = line[:54] + 'false_start'
        output_file_obj.write(newLine)
        output_file_obj.write('\n')

    output_file_obj.close()
    file_obj.close()


if __name__ == '__main__':
    logFile = parDir + "/logFile.txt"
    logging.basicConfig(filename=logFile, level = logging.DEBUG)

    DirProcessing()
