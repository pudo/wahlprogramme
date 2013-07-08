#!/bin/bash

mkdir -p pdfs
curl -o pdfs/gruene.pdf http://www.gruene.de/fileadmin/user_upload/Dokumente/Gruenes-Bundestagswahlprogramm-2013.pdf
curl -o pdfs/linke.pdf http://www.die-linke.de/fileadmin/download/wahlen2013/bundestagswahlprogramm/bundestagswahlprogramm2013.pdf
curl -o pdfs/fdp.pdf http://www.fdp.de/files/565/B_rgerprogramm_A5_Online-Fassung.pdf
curl -o pdfs/spd.pdf http://www.spd.de/linkableblob/96686/data/20130415_regierungsprogramm_2013_2017.pdf 
curl -o pdfs/cdu.pdf http://www.cdu.de/sites/default/files/media/dokumente/cdu_regierungsprogramm_2013-2017.pdf 




