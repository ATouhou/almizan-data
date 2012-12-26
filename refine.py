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
		#print line,
		line = ''

	if line.startswith('# '):
		print line,

	# refine characters
	line = line.replace(u'ي', u'ی').replace(u'ك', u'ک').replace(u'ـ', '')

	# refine punctuations
	line = re.sub(ur' ([:،؟!\.\)])', r'\1', line)
	

	# refine translations
	if len(re.findall(r'(\([0-9]{1,3}\))', line)) > 1:
		if not(u'آیه: (' in line or u'آیه (' in line or u'اصحاح' in line):

			if line.startswith('>'):
				line = re.sub(r'(\([0-9]+\))', r' \1\n\n>', line)
			else:
				line = re.sub(r'(\([0-9]+\))', r' \1\n\n', line)
	
			line = line.strip()
			if line.endswith('\n>'):
				line = line[:-1]
				
			line = line.replace('\n.', '\n').replace('\n ', '\n')
	
			line = line.strip() + '\n'

			#print line
			
	if line.strip():
		refined.write(line)
