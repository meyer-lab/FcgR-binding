all: Manuscript.pdf Manuscript.html

Manuscript.pdf:
	pandoc --template=default.latex --latex-engine=xelatex --filter pandoc-citeproc -o Manuscript.pdf ./Text/*.md

Manuscript.html:
	pandoc -s -t html5 --mathml -c ./Templates/html-style.css --filter pandoc-citeproc -o Manuscript.html ./Text/*.md

Manuscript.docx:
	pandoc -s --filter pandoc-citeproc -o Manuscript.docx ./Text/*.md

Manuscript.tex:
	pandoc -s --template=default.latex --latex-engine=xelatex --filter pandoc-citeproc -o Manuscript.tex ./Text/*.md

clean:
	rm -f Manuscript.pdf Manuscript.docx Manuscript.html Manuscript.tex
