import sys, codecs, markdown

converted = codecs.open('data/almizan.html', 'w', encoding='utf8')

converted.write('<html>')

# convert almizan.md -> almizan.html
section, i = '', 0
for line in codecs.open('data/almizan.md', encoding='utf8'):
	if line.startswith('# '):
		if section:
			html = markdown.markdown(section)
			converted.write('<div>\n%s\n</div>\n' % html)

		section = ''

		# show progress
		i += 1
		if i % 20 == 0:
			sys.stdout.write('.')
			sys.stdout.flush()

	section += line

converted.write('</html>')

print ' HTML generated'
