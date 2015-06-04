# coding:utf-8
__author__ = 'Casey'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
import re
import jieba
import jieba.analyse
import jft
import urllib
import chardet



from optparse import OptionParser

USAGE = "usage:    python extract_tags_stop_words.py [file name] -f [function]"

parser = OptionParser(USAGE)
parser.add_option("-f", dest="function")
parser.add_option("-k", dest="topK")

opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]
func = ''
if opt.function is None:
	print "plz input function name"
	sys.exit(1)
else:
	func = opt.function

if opt.topK is None:
	topK = 10
else:
	topK = int(opt.topK)



# detect url in text
def removeurl():
	file = open(file_name, 'rb')
	output = open('noURLText.txt', 'w+')
	urlNum = open('urlNum.txt', 'w+')
	urlFile = open('urlFile.txt', 'w+')
	for content in file.readlines():
		match = re.findall(r'http://[\w\d]+.\w+/[\d\w]+/[\d\w]+|http://[\w\d]+.[\w\d]+/[\w\d]+', content)
		tmp = str(content)
		count = 0
		urlFile.write(' '.join(match) + "\n")
		if match:
			for url in match:
				tmp = tmp.replace(url, '')
				count += 1
		output.write(tmp)
		urlNum.write(str(count) + "\n")
	output.close()
	urlNum.close()

# detect @ in text
def removeUselessAt():
	file = open(file_name, 'rb')
	output = open('noUselessAt.txt', 'w+')
	for content in file.readlines():
		match = re.findall(r'@\s+', content)
		tmp = str(content)
		if match:
			for at in match:
				tmp = tmp.replace(at, 'At')
		output.write(tmp)
	output.close()


def textTopK():
	file = open(file_name, 'rb')
	output = open('Step4textTopKwithemo.txt', 'w+')
	jieba.analyse.set_stop_words("../jieba/extra_dict/stop_words.txt")
	jieba.analyse.set_idf_path("../jieba/extra_dict/idf.txt.big")
	for content in file.readlines():
		topK_list = jieba.analyse.extract_tags(content, topK=topK)
		s = " ".join(re.sub("[\[\]#\s+\.\!\/_,$%^*(+\"\')]+|[《》【】：＝＋－～＃$％＊“‘’”+——！，。？、~@#￥%……&*（）；｀]+".decode("utf-8"), "".decode("utf-8"),topK) for topK in topK_list).encode("utf-8")
		output.write(s + '\n')

def textCut():
	file = open(file_name, 'rb')
	output = open('Step4textCut.txt', 'w+')
	for content in file.readlines():
		seg_list = jieba.cut(content, cut_all=False)
		output.write(" ".join(re.sub("[\[\]#\s+\.\!\/_,$%^*(+\"\')]+|[《》【】：＝＋－～＃$％＊“‘’”+——！，。？、~@#￥%……&*（）；｀]+".decode("utf-8"), "".decode("utf-8"), seg.decode("utf-8")) for seg in seg_list).encode("utf-8") + '\n')


def getEmotion():
	file = open(file_name, 'rb')
	fileEmotion = open('./Reference/emotionPhrase.txt', 'r')
	hash = {}# build hash on official emotion
	for emotion in fileEmotion.readlines():
		hash[emotion.strip()] = 1
	output = open('Step3RemoveNotEmo.txt', 'w+')
	emotionlist = open('Step3Emotion.txt', 'w+')
	for content in file.readlines():
		match = re.findall(r'\[[^\[^\\S]+\]', content)
		tmp = str(content)
		emo_list = []
		for emo in match:
			if hash.has_key(emo.encode('utf-8')):
				emo_list.append(emo)
				tmp = tmp.replace(emo, '')
			else:
				tmp = tmp.replace(emo, '')
		output.write(tmp)
		emotionlist.write(" ".join(emo_list) + '\n')

def readEmotion():
	file = open(file_name, 'rb')
	output = open('emotionValue.txt', 'w+')
	for content in file.readlines():
		tmp = content.split('\t')
		output.write(tmp[1].replace('Phrase:','') + '\n')
	output.close()

def removeAt():
	file = open(file_name, 'rb')
	output = open('Step4RemoveAt.txt', 'w+')
	atListOutput = open('Step4AtList.txt','w+')

	for content in file.readlines():
		atList = []
		match = re.findall(r'@\S+', content)
		tmp = str(content)
		if match:
			for at in match:
				atList.append(at)
				tmp = tmp.replace(at, '')
		atListOutput.write(" ".join(atList) + '\n')
		output.write(tmp)
	output.close()

def givelabel():
	file = open(file_name, 'rb')
	output = open('./data/threeLabel.txt', 'w+')
	threelabelText = open('./data/Step5ThreeLabelText.txt', 'w+')
	i = 1
	for content in file.readlines():

		questionable = 0
		leng = len(str(content))
		if leng <= 50:
			questionable = 0.5
			threelabelText.write(content)
		elif i <= 2346:
			questionable = 1
		else:
			questionable = 0
		output.write(str(questionable) + '\n')
		i += 1
	output.close()
	threelabelText.close()






if opt.function == 'removeUselessAt':
	removeUselessAt()
elif opt.function == 'removeurl':
	removeurl()
elif opt.function == 'textTopK':
	textTopK()
elif opt.function == 'getEmotion':
	getEmotion()
elif opt.function == 'readEmotion':
	readEmotion()
elif opt.function == 'textCut':
	textCut()
elif opt.function == 'removeAt':
	removeAt()
elif opt.function == 'givelabel':
	givelabel()
