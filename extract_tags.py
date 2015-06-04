# coding:utf-8
__author__ = 'Casey'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

USAGE = "usage:    python extract_tags_stop_words.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

file = open(file_name, 'rb')
output = open('tags.txt','wb')


jieba.analyse.set_stop_words("../jieba/extra_dict/stop_words.txt")
jieba.analyse.set_idf_path("../jieba/extra_dict/idf.txt.big")
for content in file.readlines():
	tags = jieba.analyse.extract_tags(content, topK=topK)
	if len(tags) <= 3:
		output.write(",".join(tags).encode('utf-8')+ "," + 'repost' + '\n')
	else:
		output.write(",".join(tags).encode('utf-8')+ "," + 'original' + '\n')

