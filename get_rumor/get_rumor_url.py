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
	filename = "ridlist" + str(j) + ".txt"
	exists = os.path.exists(filename)
fileout = codecs.open(filename,'w','utf-8')
errorfile = strftime("%Y%d%m_%H%M%S_error", gmtime()) + ".log"
lastpage = False
er_ct = 0
error = False
i = 1
while True:
	try:
		targetno = int(raw_input('Enter the target number of tweets: '))
		break
	except ValueError:
		print "Oops!  That was no valid number.  Try again..."
pageno = 1
cookies = {'SUB': '_2A254TC4CDeTxGedG7VUX9SrLzjuIHXVbOBjKrDV8PUNbuNBuLUP8kW8KZCWyP_PlH8Vd2mDoD_2J3bm6CA..'}
while (i-1) <= targetno:
	url = "http://service.account.weibo.com/?type=5&status=4" + "&page=" + str(pageno)
	#print url
	pageno += 1
	response = requests.get(url,cookies=cookies)
	if response.status_code == 200:	#if success
		st = "Succeeded"
		data = response.text
		data = data.replace("\\n", "\n")
		data = data.replace("\\r", "\r")
		data = data.replace("\\t", "\t")
		data = data.replace("\\\"", "\\")
		data = data.replace("\\/", "/")
		data = data.decode("unicode-escape")
		try:
			data = data.split("\"html\":\"")[5]
		except:
			print data
			er_ct += 1
			with open('errorpage.html','w') as outputf:
				outputf.write(data)
			break
		data = data.split("\"})</script>")[0]
		rid = data.split("show?rid=")
		count = 1
		for count in range(1,len(rid)):
			rid[count] = rid[count].split("\\")[0]
			output = rid[count] + "\n"
			count += 1
			fileout.write(output)
			i += 1
	else:
		if not error:
			errorlog = open(errorfile,'w')
			errorlog.write("Following pages failed to be crawled:\n")
			error = True
		else:
			errorlog = open(errorfile, 'a')
		st = "Failed"
		er_ct += 1
		line = " Error code:"
		line += str(response.status_code)
		line += "\n"
		errorlog.write(line)
		errorlog.close()
	print ("Query Page %d %s" % (pageno-1,st))
if er_ct == 0:
	print ("Congrats! Finished %d pieces with no error!" % (i-1))
else:
	print ("%d finished with %d errors." % (i-1, er_ct))
fileout.close()