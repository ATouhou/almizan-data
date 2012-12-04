import codecs, sys, re
import tashaphyne.normalize as norm
from pyquery import PyQuery as pq
import Levenshtein

almizan = codecs.open('data/almizan.html', encoding='utf-8').read()
quran = codecs.open('data/quran.txt', encoding='utf-8').readlines()
d = pq(almizan)
i = 0
for aye in d('blockquote p'):
	aye = pq(aye)
	# aye.text()
	s, a, max, c = 0, 0, 0, 0
	for ayeh in quran:
		ayeh = norm.normalize_searchtext(ayeh)
		aye1 = norm.normalize_searchtext(aye[0].text)
		if max < Levenshtein.ratio(ayeh,aye1):
			max = Levenshtein.ratio(ayeh,aye1)
		if Levenshtein.ratio(ayeh, aye1) > 0.75:
			match = re.search(r'\d+', ayeh)
			s = int(match.group(0))
			match = re.search(r'\|\d+', ayeh)
			a = int(match.group(0)[1:])
			del quran[:c+1]
			break
		c += 1
	if max <= 0.75:
		ayeh = quran[0]
		match = re.search(r'\d+', ayeh)
		s = int(match.group(0))
		match = re.search(r'\|\d+', ayeh)
		a = int(match.group(0)[1:])
		del quran[0]

	aye.addClass('aye')
	aye.attr('rel', '%s-%s' % (s, a))

	i += 1
	if i % 100 == 0:
		sys.stdout.write('.')
		sys.stdout.flush()

d.root.write('data/output.html', encoding='utf-8')

print ' Aye tags added'
