""" starts with aya.py output """

import codecs, sys
from pyquery import PyQuery as pq

almizan = codecs.open('data/output-aya.html', encoding='utf-8').read()
errors = open('data/errors.txt', 'w')

d = pq(almizan)
for i, div in enumerate(d('div')):
	div = pq(div)
	ayas = div.find('.aya')
	if ayas:
		rels = [pq(p).attr('rel') for p in ayas]
	else:
		errors.write('empty div\n')
		continue

	sura, aya = [], []
	for rel in rels:
		s, a = rel.split('-')
		sura.append(int(s))
		aya.append(int(a))

	mi, ma = min(aya), max(aya)

	if len(set(sura)) != 1 or aya != range(mi, ma+1):
		errors.write(str(rels) + '\n')
		continue

	sura = sura.pop()
	div.attr('rel', '%d-%d:%d' % (sura, mi, ma))

	if i % 50 == 0: sys.stdout.write('.'); sys.stdout.flush()

d.root.write('data/output-sections.html', encoding='utf-8')

print ' Section tags added'
