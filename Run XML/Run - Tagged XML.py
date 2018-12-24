import spacy
import re

nlp = spacy.load(r'C:\Users\zl0\Desktop\Testing NLP\T_Model\nl_model-0.0.0\nl_model\nl_model-0.0.0')

txt = open(r"C:\Users\zl0\Desktop\Training Model\Annonimize\Done\01\02\ASAG05\ASAG0501.txt", "r", encoding='utf-8')
XML = open(r"Tagged-xml.xml","a")
dict = {}
for line in txt.readlines():
	doc_file = nlp(line)
	# print(doc_file)
	for word in doc_file.ents:
		wlbl = word.label_
		wtxt = word.text
		dict[(wtxt)] = wlbl
		print("label : "+wlbl,"Text: "+wtxt)
		lineR = line.replace(wtxt,"<ano as=\"" + wlbl + "\">" + wtxt + "</ano>")
		XML.write(lineR)
	XML.write(line)



# print(dict.items())
# for line in txt.readlines():
# 	for w in line:
# 	find = re.findall(dict.keys(),line,re.M|re.I)
#
# 	if find:
# 		for match in find:
#
# 			XML.write("<ano as=\"" + dict.values() + ">" + find + "</ano>")
# 	else:
# 		XML.write(find)