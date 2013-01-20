# coding=utf8

import codecs, re
from pyquery import PyQuery as pq
import Levenshtein
from idlelib.IOBinding import encoding
import tashaphyne.normalize as norm


almizan = codecs.open('data/output-trans.html',encoding='utf-8').read()
errors = open('data/parts_errors.txt','w')
quran = codecs.open('data/quran.txt', encoding='utf-8').readlines()
tags = codecs.open('data/part-tags.html','w',encoding='utf-8')
d = pq(almizan)

for sec in d("div"):
		"""find section ayas"""
		sec = pq(sec)
		sec_str = sec.attr('rel')
		if sec_str == None:
			continue
		print sec_str
		match = re.search(r'\d+', sec_str)
		sura = int(match.group(0))
		match = re.search(r'\-\d+',sec_str )
		aya_begin = int(match.group(0)[1:])
		match = re.search(r'\:\d+', sec_str)
		aya_end = int(match.group(0)[1:])
		sec_ayas = []
		i = aya_begin
		while(i <= aya_end):
			aya_num = str(sura) +'|'+ str(i)
			for c in range(len(quran)):
				q_aya = quran[c]
				if(q_aya.startswith(aya_num)):
					sec_ayas.append(q_aya)
					quran = quran[c+1:]
					break
			i += 1	
		#omit parts with null or <=2 length
		counter = 1
		for part in sec.find("em"):
			success = 0
			part = pq(part)
			try:
				part_text = norm.normalize_searchtext(part[0].text)
				part_text = part_text
			except:
				part_text = part[0].text
				errors.write(part.outerHtml())
			print counter
			counter += 1
			if part == None or part[0].text == None:
				continue
			if  len(part[0].text)<=2:
				continue
			
			for aya in sec_ayas:
				aya = norm.normalize_searchtext(aya)
				aya = aya.replace(u'ي', u'ی').replace(u'ك', u'ک')				
				aya_tokens = re.split("[ |\r\n]",aya[:-2])
				aya_tokens = aya_tokens[2:]
				part_tokens = re.split(" ",part_text)
				partlen = len(part_tokens)
				if partlen<1:
					continue
				for i in range(len(aya_tokens)-partlen):
					start = i
					end = start + partlen						
					current = start
					threshold = 0.5
					while current<end:
						try:
							if Levenshtein.ratio(aya_tokens[current], part_tokens[current-i]) > threshold:
								current += 1
								continue
						except:
							pass
						break
					if current >= end:
						success = 1	
						break
					
				if success != 1 :	
					continue
				
				match = re.search(r'\d+', aya)
				sura_num = int(match.group(0))
				match = re.search(r'\|\d+', aya)
				aya_num = int(match.group(0)[1:])
				part.attr('rel','%s-%s/%s-%s' % (sura_num, aya_num, start, end))
				break
d.root.write('data/output-parts.html', encoding='utf-8')	
for tag in d('em'):
	try:
		tag = pq(tag)
		tags.write(tag.outerHtml())
		tags.write('\n')
	except:
		pass
tags.close()
print('aya parts tagged!\n')	
			