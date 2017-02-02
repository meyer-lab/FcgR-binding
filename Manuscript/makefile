pan_common = --filter pandoc-citeproc -f markdown ./Text/*.md

all: Manuscript.html

./Figures/Figure%.png: ./Figures/Figure%.pdf
	convert -density 450 ./Figures/Figure$*.pdf -quality 90 ./Figures/Figure$*.png

Manuscript.pdf: ./Text/*.md ./Figures/Figure*.pdf
	pandoc $(pan_common) --template=default.latex --latex-engine=xelatex  -o Manuscript.pdf

Manuscript.html: ./Text/*.md ./Figures/Figure*.pdf ./Figures/Figure1.png
	pandoc -s $(pan_common) -t html5 --mathml -c ./Templates/kultiad.css --template=./Templates/html.template -o Manuscript.html

Manuscript.docx: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) -o Manuscript.docx

Manuscript.tex: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) --template=default.latex --latex-engine=xelatex -o Manuscript.tex

clean:
	rm -f Manuscript.pdf Manuscript.docx Manuscript.html Manuscript.tex
	rm -f ./Figures/Figure*.png
