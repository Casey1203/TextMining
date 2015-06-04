#encoding: utf8
import urllib2
import urllib
import cookielib
import os
import re
import codecs
import os.path
import requests
from time import gmtime, strftime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
j=0
exists = True
while exists:
	j+=1
	filename = "wbid" + str(j) + ".txt"
	exists = os.path.exists(filename)
fileout = codecs.open(filename,'w','utf-8')
fileout.write("Weibo URL as follows:\n")
fileout.close()
errorfile = strftime("%Y%d%m_%H%M%S_error", gmtime()) + ".log"
er_ct = 0
error = False
i = 1
while True:
	try:
		inputfile = str(raw_input('Enter the input file of rid: '))
		ridfile = open(inputfile,'r')
		break
	except IOError:
		print "Oops! No file found with that name! Try again..."
cookies = {'SUB': '_2A254TC4CDeTxGedG7VUX9SrLzjuIHXVbOBjKrDV8PUNbuNBuLUP8kW8KZCWyP_PlH8Vd2mDoD_2J3bm6CA..'}
for rid in ridfile:
	url = "http://service.account.weibo.com/show?rid=" + rid
	#print url
	
	response = requests.get(url,cookies=cookies)
	if response.status_code == 200:	#if success
		st = "Succeeded"
		data = response.text
		data = data.replace("\\n", "\n")
		data = data.replace("\\r", "\r")
		data = data.replace("\\t", "\t")
		data = data.replace("\\\"", "\\")
		data = data.replace("\\/", "/")
		try:
			data = data.split("value=original_text")[1]
			data = data.split("\'>")[0]
			data = data.split("http://weibo.com/")[1]
			data = data + "\n"
			fileout = codecs.open(filename,'a','utf-8')
			fileout.write(data)
			fileout.close()
		except IndexError:
			if not error:
				errorlog = open(errorfile,'w')
				errorlog.write("Following item failed to be crawled:\n")
				error = True
			else:
				errorlog = open(errorfile, 'a')
			st = "Failed"
			er_ct += 1
			line = "RID: " + rid.replace("\n","") + "\n"
			errorlog.write(line)
			errorlog.close()
	else:
		if not error:
			errorlog = open(errorfile,'w')
			errorlog.write("Following item failed to be crawled:\n")
		else:
			errorlog = open(errorfile, 'a')
		st = "Failed"
		er_ct += 1
		line = "RID: " + rid + " Error code:"
		line += str(response.status_code)
		line += "\n"
		errorlog.write(line)
		errorlog.close()
	print ("Query No. %d %s" % (i,st))
	i += 1
if er_ct == 0:
	print ("Congrats! Finished %d pieces with no error!" % (i-1))
else:
	print ("%d finished with %d errors." % (i-1, er_ct))
fileout.close()