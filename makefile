NPROCS := 8

pan_common = --filter pandoc-citeproc -f markdown ./Manuscript/Text/*.md
fdir = ./Manuscript/Figures

.PHONY: clean upload test
.PRECIOUS: Manuscript/Figures/Figure1.pdf

all: index.html

$(fdir)/Figure%.png: $(fdir)/Figure%.pdf
	convert -density 450 $(fdir)/Figure$*.pdf -quality 90 $(fdir)/Figure$*.png

$(fdir)/Figure1%pdf $(fdir)/Figure2%pdf: genFigures.py
	python3 genFigures.py

Manuscript.pdf: ./Manuscript/Text/*.md
	pandoc $(pan_common) --template=default.latex --latex-engine=xelatex  -o ./Manuscript/Manuscript.pdf

index.html: ./Manuscript/Text/*.md $(fdir)/Figure1.png $(fdir)/Figure2.png
	pandoc -s $(pan_common) -t html5 --mathml -c ./Manuscript/Templates/kultiad.css --template=./Manuscript/Templates/html.template -o ./Manuscript/index.html

Manuscript.docx: ./Manuscript/Text/*.md
	pandoc -s $(pan_common) -o ./Manuscript/Manuscript.docx

Manuscript.tex: ./Manuscript/Text/*.md
	pandoc -s $(pan_common) --template=default.latex --latex-engine=xelatex -o ./Manuscript/Manuscript.tex

clean:
	rm -f ./Manuscript/Manuscript.* ./Manuscript/index.html
	rm -f $(fdir)/Figure*

test:
	python3 -m unittest discover

upload:
	lftp -c "set ftp:list-options -a; open athena; cd ./www/fcgr-paper/; lcd ./Manuscript/; mirror --reverse --delete --ignore-time --verbose"
