
all: download extract analyze

download:
	mkdir -p pdfs
	curl -o pdfs/gruene.pdf http://www.gruene.de/fileadmin/user_upload/Dokumente/Gruenes-Bundestagswahlprogramm-2013.pdf
	curl -o pdfs/linke.pdf http://www.die-linke.de/fileadmin/download/wahlen2013/bundestagswahlprogramm/bundestagswahlprogramm2013.pdf
	curl -o pdfs/fdp.pdf http://www.fdp.de/files/565/B_rgerprogramm_A5_Online-Fassung.pdf
	curl -o pdfs/spd.pdf http://www.spd.de/linkableblob/96686/data/20130415_regierungsprogramm_2013_2017.pdf 
	curl -o pdfs/cdu.pdf http://www.cdu.de/sites/default/files/media/dokumente/cdu_regierungsprogramm_2013-2017.pdf

extract:
	mkdir -p html
	mkdir -p markdown

	pdftohtml -noframes -f 4 pdfs/cdu.pdf html/cdu.html
	python cdu_to_text.py

	pdftohtml -noframes -c -f 4 -l 118 pdfs/spd.pdf html/spd.html
	rm html/spd*.png
	python spd_to_text.py

	pdftohtml -noframes -c -f 7 -l 93 pdfs/fdp.pdf html/fdp.html
	rm html/fdp*.png
	python fdp_to_text.py

	pdftohtml -noframes -c -f 5 -l 86 pdfs/linke.pdf html/linke.html
	rm html/linke*.png
	python linke_to_text.py

	pdftohtml -noframes -c -f 7 -l 319 pdfs/gruene.pdf html/gruene.html
	rm html/gruene*.png
	python gruene_to_text.py

analyze:
	python sections.py
	python section_titles.py
	python topics.py
	python to_html.py
	python political_values.py