pan_common = --filter pandoc-citeproc -f markdown ./Text/*.md

.PHONY: clean upload

all: index.html Manuscript.pdf

./Figures/Figure%.png: ./Figures/Figure%.pdf
	convert -density 450 ./Figures/Figure$*.pdf -quality 90 ./Figures/Figure$*.png

Manuscript.pdf: ./Text/*.md ./Figures/Figure*.pdf
	pandoc $(pan_common) --template=default.latex --latex-engine=xelatex  -o Manuscript.pdf

index.html: ./Text/*.md ./Figures/Figure*.pdf ./Figures/Figure1.png
	pandoc -s $(pan_common) -t html5 --mathml -c ./Templates/kultiad.css --template=./Templates/html.template -o index.html

Manuscript.docx: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) -o Manuscript.docx

Manuscript.tex: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) --template=default.latex --latex-engine=xelatex -o Manuscript.tex

clean:
	rm -f Manuscript.pdf Manuscript.docx index.html Manuscript.tex
	rm -f ./Figures/Figure*.png

upload:
	lftp -c "set ftp:list-options -a; open athena; cd ./www/fcgr-paper/; lcd ./; mirror --reverse --delete --ignore-time --verbose"
