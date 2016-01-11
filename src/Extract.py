import xml.sax
from src import ChunkHandler

#if __name__=="__main__":
def Extract(filePath_m, filePath_w):
    # filePath_m="/home/linlin/crfsuite/ssr_all/train/ssr_tr/connie_dev2_fsh_110103_A.w"
    # #
    # filePath_w="/home/linlin/crfsuite/ssr_all/train/ssr_tr/connie_dev2_fsh_110103_A.m"

    # filePath_m="/home/linlin/sf_GoogleDrive/now/feature/ssr_all/test/ssr_ck/connie_dev2_fsh_117716_A.m"
    # #
    # filePath_w="/home/linlin/sf_GoogleDrive/now/feature/ssr_all/test/ssr_ck/connie_dev2_fsh_117716_A.w"

    parser = xml.sax.make_parser()

    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler_w = ChunkHandler.ChunkHandler_w()

    parser.setContentHandler(handler_w)

    parser.parse(filePath_w)

#  Instance a handler_m object for processing .m file, transfer origDict before destroy the handler_w object.
    handler_m = ChunkHandler.ChunkHandler_m(handler_w.origDict)
    del handler_w

    parser.setContentHandler(handler_m)

    parser.parse(filePath_m)

    # print(handler_m.line1[18])
    # print(handler_m.line2[18])
    # print(handler_m.line3[18])
    # print(handler_m.line4[18])

    return [handler_m.line1, handler_m.line2, handler_m.line3, handler_m.line4, handler_m.line5]
