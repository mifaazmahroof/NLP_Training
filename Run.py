import spacy

nlp = spacy.load(r'C:\Users\zl0\Desktop\Testing NLP\T_Model\nl_model-0.0.0\nl_model\nl_model-0.0.0')

txt = open(r"C:\Users\zl0\Desktop\Training Model\Annonimize\Done\01\02\ASAG05\ASAG0501.txt", "r", encoding='utf-8')

for line in txt.readlines():
	doc_file = nlp(line)
	# print(doc_file)
	for word in doc_file.ents:
		print('word:', word.label_, '+', word.text)
