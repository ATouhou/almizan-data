""" starts with convert.py output """

import codecs, sys, re
from pyquery import PyQuery as pq
import tashaphyne.normalize as norm
import Levenshtein

almizan = codecs.open('data/almizan.html', encoding='utf-8').read()
quran = codecs.open('data/quran.txt', encoding='utf-8').readlines()
errors = open('data/errors.txt','w')

d = pq(almizan)
for i, aya in enumerate(d('blockquote p')):
	aya = pq(aya)
	s, a, max, c = 0, 0, 0, 0
	for ayah in quran:
		ayah = norm.normalize_searchtext(ayah)
		aya1 = norm.normalize_searchtext(aya[0].text)
		if max < Levenshtein.ratio(ayah,aya1):
			max = Levenshtein.ratio(ayah,aya1)
		if Levenshtein.ratio(ayah, aya1) > 0.75:
			match = re.search(r'\d+', ayah)
			s = int(match.group(0))
			match = re.search(r'\|\d+', ayah)
			a = int(match.group(0)[1:])
			for err in quran[:c]:
				errors.write(err.encode('utf-8'))
			del quran[:c+1]
			break
		c += 1
	if max <= 0.75:
		ayah = quran[0]
		match = re.search(r'\d+', ayah)
		s = int(match.group(0))
		match = re.search(r'\|\d+', ayah)
		a = int(match.group(0)[1:])
		del quran[0]

	aya.addClass('aya')
	aya.attr('rel', '%s-%s' % (s, a))

	if i % 100 == 0: sys.stdout.write('.'); sys.stdout.flush()

d.root.write('data/output.html', encoding='utf-8')

print ' aya tags added'
