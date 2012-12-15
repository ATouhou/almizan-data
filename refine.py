# coding=utf8

import codecs, re

refined = codecs.open('data/almizan.md', 'w', encoding='utf8')

# convert raw.md -> almizan.md
for line in codecs.open('data/raw.md', encoding='utf8'):
	if line and not line.startswith('>'):
		line = re.sub(r'\*([^\*]+)\*', r' *\1* ', line) +'\n'

	if line.startswith('>'):
		line = line + '\n'
		if len(line) < 5: line = ''

	if line.find(u'تفسیر المیزان') >= 0:
		print line,
		line = ''

	if line.startswith('# '):
		print line,

	# refine characters
	line = line.replace(u'ي', u'ی').replace(u'ك', u'ک').replace(u'ـ', '')

	# refine punctuations
	line = re.sub(ur' ([:،؟!\.\)])', r'\1', line)

	if line.strip():
		refined.write(line)
