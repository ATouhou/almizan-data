# coding=utf8

import codecs
from pyquery import PyQuery as pq
from nltk import stem

isri = stem.ISRIStemmer()
almizan = codecs.open('data/output-trans.html', encoding='utf-8').read()
quran = codecs.open('data/quran.txt', encoding='utf-8').readlines()
errors = codecs.open('data/errors-phrases.txt', 'w', encoding='utf-8')
tags = codecs.open('data/tags-phrases.txt', 'w', encoding='utf-8')
d = pq(almizan)


def normalize(text):
	text = text.strip().replace(u'ي', u'ی').replace(u'ك', u'ک').replace(u'،', u'').replace(u'؟', u'').replace(u'أ', u'ا').replace(u'إ', u'ا').replace(u'ه', u'ة').replace(u'ّ', u'').replace(u'اء', u'ا').replace('...', '')
	return [isri.stem(word) for word in text.split(' ')]


def findPhrase(phrase, aya):
	p, a = '-'.join(phrase), '-'.join(aya)
	index = a.find(p)
	if index >= 0:
		index = a[:index].count('-')
		return index, index + len(phrase)

	return None


ayas = {}
for line in quran:
	line = line.split('|')
	if len(line) == 3:
		ayas[int(line[0]), int(line[1])] = normalize(line[2])

for sec in d("div"):
	"""find section ayas"""
	section = pq(sec)
	section_rel = section.attr('rel')
	if section_rel == None:
		continue

	# find aya range
	sura, aya_range = section_rel.split('-')
	aya_from, aya_to = aya_range.split(':')
	sura, aya_from, aya_to = int(sura), int(aya_from), int(aya_to)

	# iteratoe over all phrases
	for em in section.find('em'):
		em = pq(em)
		phrase = normalize(em.text())
		if len(phrase) > 5:
			continue

		for aya in range(aya_from, aya_to+1):

			# match query and aya
			result = findPhrase(phrase, ayas[sura, aya])
			if result:
				em.attr('rel', '%s-%s/%s-%s' % (sura, aya, result[0], result[1]))
				break

		if not em.attr('rel'):
			errors.write('%s\t%s\n' % (section_rel, em.outerHtml()))
		else:
			tags.write('%s\t%s\n' % (section_rel, em.outerHtml()))

d.root.write('data/output-phrases.html', encoding='utf-8')
print 'aya parts tagged!'
