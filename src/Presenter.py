#!/usr/bin/python3
import os

class Presenter:
    'Present necessary work on the screen as well as in the txt file'

    def __init__(self, line1, line2, line3, line4, line5):
        self.line1=line1
        self.line2=line2
        self.line3=line3
        self.line4=line4
        self.line5=line5

        parDir = os.path.dirname( os.getcwd())
        path = parDir + "/ck.txt"

        self.output_file = open(path, 'w')

    def Demo(self ):

        """
        :rtype : object
        """


        sentsNum = min(len(self.line1), len(self.line2),len(self.line3), len(self.line4), len(self.line5))
        for i in range(sentsNum):
            minWordNum = min(len(self.line1[i]), len(self.line2[i]), len(self.line4[i]), len(self.line3[i]), len(self.line5[i]))
            for j in range(minWordNum):
                tags = ''.join(self.line2[i][j]).strip('$')
                tags = tags.strip()
                token = ''.join(self.line1[i][j]).strip()
                label = self.line3[i][j].strip()
                # label = ''.join(word[:1])
                # label = label.strip()
                word = ''.join(self.line4[i][j]).strip()
                semantic = ''.join(self.line5[i][j].strip())
                if not token.strip():
                    token = "^"
                if not tags.strip():
                    tags = "^"
                if not label.strip():
                    label = "OK"
                if not word.strip():
                    word = "^"
                if not semantic.strip():
                    semantic = "^"
                lineFormat = "%-15s %-10s %-15s %-15s %-40s" % (token, tags,  word, semantic, label)
                print(lineFormat, end='\n')
                self.output_file.write(lineFormat)
                self.output_file.write('\n')
            self.output_file.write('\n')
        self.output_file.close()