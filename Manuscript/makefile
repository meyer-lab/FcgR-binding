pan_common = --filter pandoc-crossref --filter pandoc-citeproc -f markdown ./Text/*.md

all: Manuscript.html

Manuscript.pdf: ./Text/*.md ./Figures/Figure*.pdf
	pandoc $(pan_common) --template=default.latex --latex-engine=xelatex  -o Manuscript.pdf

Manuscript.html: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) -t html5 --mathml -c ./Templates/kultiad.css --template=./Templates/html.template -o Manuscript.html

Manuscript.docx: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) -o Manuscript.docx

Manuscript.tex: ./Text/*.md ./Figures/Figure*.pdf
	pandoc -s $(pan_common) --template=default.latex --latex-engine=xelatex -o Manuscript.tex

clean:
	rm -f Manuscript.pdf Manuscript.docx Manuscript.html Manuscript.tex
