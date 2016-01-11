#!/usr/bin/python3
import xml.sax
import logging
import re

logger = logging.getLogger(__name__)

class ChunkHandler_m(xml.sax.ContentHandler):
    'Chunk class refers to a set of annotation marks in the xml file'

    def __init__(self,dictionary):
        self.CurrentData = ""
        self.trans=""
        self.form=""
        self.m_ident=""        # every <m> has an identification
        self.dest=""
        self.pos=""             # used only when the <edit> == yes
        self.argType=""             # indicate currently what arg type the arg_node is
        self.origDict=dictionary
        self.line1=[]
        self.line2=[]
        self.line3=[]
        self.line4=[]
        self.line5=[]
        self.sent1=[]
        self.sent2=[]
        self.sent3=[]
        self.sent4=[]
        self.sent5=[]
        self.pos_reconstruct = 0
        self.w_counter = 0
        self.pos_increase = 0           #record the position in a m chunk, always increase
        self.ptr_in_sent = 0   # point to the pos in one sentence
        self.dict_id_in_sent_pos = {}   # Dictionary key is ID, value is pos in sentence
        self.dict_id_semanLabel = {}    # Dictionary key is ID, value is semantic role

    def startElement(self, tag, attributes):
        self.CurrentData=tag
        if tag == "m":
            self.m_ident = attributes["id"]
            self.pos_reconstruct = 0        # record the position of the reconstructed word in a m chunk
            self.w_counter = 0              # record how many words corresponding a m chunk
            self.pos_increase = 0
        if tag == "s":
            self.sent1=[]
            self.sent2=[]
            self.sent3=[]
            self.sent4 = []
            self.sent5=['',] * 100
            self.ptr_in_sent = 0
            self.dict_id_semanLabel.clear()
            self.dict_id_in_sent_pos.clear()

        if tag == "predicate":
            self.sent5[self.ptr_in_sent-1] = "predicate"

        if None != re.search(r"arg", tag) and None == re.search(r'arg_n', tag):
                self.argType = self.CurrentData

   # Call when an elements ends
    def endElement(self, tag):
        if tag == "s":
            for key in self.dict_id_semanLabel:
                key1 = "w-" + key[2:]
#                if len(self.dict_id_in_sent_pos) < 1 or len(self.dict_id_semanLabel) <1:
#                    logger.debug("Error! no element in a sentence")
                default = "problem"
                pos = self.dict_id_in_sent_pos.get(key1,default)       # If key1 can't be found, key can be found. Since dict_id_in_sent_pos also contain m_identifier
                if pos == default:
                    pos = self.dict_id_in_sent_pos.get(key, default)
                    if pos == default:
                        pos = 1
                        logger.debug("warning, in the word dictionary no id %s", key)
                semanLabel = self.dict_id_semanLabel[key]
                self.sent5[pos-1] = semanLabel

            max_sent_length = max(len(self.sent1),len(self.sent2),len(self.sent3),len(self.sent4))
            self.sent1 = self.sent1 + (max_sent_length-len(self.sent1)) * ['', ]
            self.sent2 = self.sent2 + (max_sent_length-len(self.sent2)) * ['', ]
            self.sent3 = self.sent3 + (max_sent_length-len(self.sent3)) * ['', ]
            self.sent4 = self.sent4 + (max_sent_length-len(self.sent4)) * ['', ]
            self.sent5 = self.sent5[0:max_sent_length]

            self.line1.append(self.sent1)
            self.line2.append(self.sent2)
            self.line3.append(self.sent3)
            self.line4.append(self.sent4)
            self.line5.append(self.sent5)

        if tag == "dest.rf":
            self.w_counter += 1                 # record how many words are there inside a m chunk
            self.ptr_in_sent +=1
            if self.dest in self.origDict:      # origDict's ID is w-fsh_117716#  without a w#
                self.sent1.append(self.origDict[self.dest][0])
                self.sent2.append(self.origDict[self.dest][1])
                self.dict_id_in_sent_pos[self.dest] = self.ptr_in_sent
            else:
                self.sent1.append("")
                self.sent2.append("")
                self.dict_id_in_sent_pos[self.dest] = self.ptr_in_sent

        if tag == "trans":
            if self.trans != "basic":
                self.sent3.append(self.trans)
                if self.m_ident[-6:] != self.dest[-6:]:
                    self.pos_increase += 1
            else:
                self.sent3.append("OK")
                self.pos_reconstruct = self.pos_increase + 1

                if self.m_ident[-6:] != self.dest[-6:]:
                    self.dict_id_in_sent_pos[self.m_ident] = self.ptr_in_sent

                if self.m_ident[-6:] != self.dest[-6:]:
                    self.pos_increase += 1

        if tag == "m":
            if self.pos_reconstruct > 0:
                base_pos = len(self.sent4)
                self.sent4 = self.sent4 + ['', ] * self.w_counter
                self.sent4[base_pos + self.pos_reconstruct - 1] = self.form
            else:
                base_pos = len(self.sent4)
                self.sent4 = self.sent4 + ['', ] * self.w_counter
                self.sent4[base_pos + self.w_counter - 1] = self.form
                # self.sent1.append('')
                # self.sent2.append(self.pos)
                # self.sent3.append("edit")
        if tag == "arg_node":
            self.dict_id_semanLabel[self.id_arg] = self.argType


   # Call when new elements are read
    def characters(self, content):
        if self.CurrentData == "dest.rf":
            if len(content.strip()) > 0:
                self.dest = content
                self.dest = self.dest[2:]       # w#w-fsh_   w# deleted

        elif self.CurrentData =="trans":
            if len(content.strip()) > 0:
                self.trans = content

        elif self.CurrentData == "form":
            if len(content.strip()) > 0:
                self.form = content

        elif self.CurrentData == "pos":
            if len(content.strip()) > 0:
                self.pos = content

        #elif (re.search(r'arg_no', self.CurrentData) != None):
        elif self.CurrentData == "arg_node":
            if len(content.strip()) > 0:
                self.id_arg = content



class ChunkHandler_w(xml.sax.ContentHandler):
    'ChunkHandler_w class refers to original word in the xml file'

    def __init__(self):
        self.CurrentData = ""
        self.token=""
        self.a1 = ""
        self.pos = ""
        self.identification=""
        self.origDict={}

    def startElement(self, tag, attributes):
        self.CurrentData=tag
        if tag == "w":
            self.identification = attributes["id"]

   # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "token":
            self.a1 = self.token
        if self.CurrentData == "pos":
            self.origDict[self.identification] = [self.a1, self.pos]
            #self.origDict[self.identification] = [a1, a2]


   # Call when an elements ends
    def characters(self, content):
        if self.CurrentData == "token":
            self.token= content
        if self.CurrentData == "pos":
            self.pos = content