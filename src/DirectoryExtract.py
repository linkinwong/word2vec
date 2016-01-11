

__author__ = 'linlin'
import os
import logging
from src import Extract
from src import Presenter

logger = logging.getLogger('main_module')

if __name__=="__main__":

    parDir = os.path.dirname( os.getcwd())
    path = parDir + "/ssr/ssr_ck"

    logFile = parDir + "/logFile.txt"
    logging.basicConfig(filename= logFile, level = logging.DEBUG)
    # # Set up formatter for logging first
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # # Setup Handler
    # console = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    # console.setFormatter(formatter)
    #
    # # Setup Logger
    # logger.addHandler(console)
    # logger.setLevel(logging.DEBUG)
    #

    text1=[]        # Original token
    text2=[]        # Part of speech tagging
    text3=[]        # Disfluency type
    text4=[]        # Reconstructed words
    text5=[]        # Semantic role
    for root, dirs, files in os.walk(path):
        for filespath in files:
            filePath_m = os.path.join(root, filespath)
            filePath_w = filePath_m[:-2] + ".w"
            if filePath_m[-1:] == 'm' and os.path.exists(filePath_w):
                [line1, line2, line3, line4, line5] = Extract.Extract(filePath_m, filePath_w)
                for i in range(min(len(line1), len(line2), len(line3), len(line4), len(line5))):
                    text1.append(line1[i])
                    text2.append(line2[i])
                    text3.append(line3[i])
                    text4.append(line4[i])          # text is many text files, line is one text file
                    text5.append(line5[i])          # line includes many sentences
    # print(text1[39])
    # print(text2[39])
    # print(text3[39])
    # print(len(text1))

    presenter = Presenter.Presenter(text1, text2, text3, text4, text5)

    presenter.Demo()

    assert isinstance(presenter, object)
    del presenter

