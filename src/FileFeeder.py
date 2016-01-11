__author__ = 'linlin'

class FileFeeder:

      def __init__(self,line1,line2,line3):
        self.line1=line1
        self.line2=line2
        self.line3=line3
        self.numPerLine=5
        self.wordWidth=18
        self.output_file = open('output.txt','w')

    def Demo(self,*arg ):

