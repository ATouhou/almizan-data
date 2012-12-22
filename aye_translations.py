# coding=utf8

import codecs, re
from pyquery import PyQuery as pq
import Levenshtein
from idlelib.IOBinding import encoding

almizan = codecs.open('data/output-sections.html',encoding='utf-8').read()
errors = open('data/trans_errors.txt','w')
d = pq(almizan)
header = u'ترجمه آیات'.encode('utf8')
for aye in d('h2'):
	aye = pq(aye)
	if Levenshtein.ratio(header, (aye[0].text).encode('utf8')) < 0.8:
		continue
	sec = aye.parent().attr('rel')
	if sec == None:
		continue
	#print(sec)
	match = re.search(r'\d+', sec)
	sura = int(match.group(0))
	match = re.search(r'\-\d+',sec )
	aya_begin = int(match.group(0)[1:])
	match = re.search(r'\:\d+', sec)
	aya_end = int(match.group(0)[1:])
	trans = aye.next()
	while aya_begin <= aya_end:
		trans.addClass('trans')
		trans.attr('rel', '%s-%s' % (sura, aya_begin))
		print('%s-%s' % (sura, aya_begin))
		if trans.length == 0 or trans[0].text == None:
			errors.write('[%s-%s]\n' % (sura, aya_begin))
		else:	
			match = re.search(r'\d+', trans[0].text)
			if match != None:
				c = int(match.group(0))
				if  c!=aya_begin:
					errors.write('[%s-%s]\n' % (sura, aya_begin))
		aya_begin += 1
		trans = trans.next()

d.root.write('data/output-trans.html', encoding='utf-8')
print('aya translations tagged!\n')
		
	
	
	

