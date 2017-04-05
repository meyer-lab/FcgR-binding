NPROCS := 8

pan_common = -F pandoc-crossref -F pandoc-citeproc -f markdown ./Manuscript/Text/*.md
fdir = ./Manuscript/Figures
tdir = ./Manuscript/Templates

.PHONY: clean upload test profile

all: Manuscript/index.html Manuscript/Manuscript.pdf

$(fdir)/Figure1%pdf $(fdir)/Figure2%pdf $(fdir)/Figure3%pdf $(fdir)/Figure1%svg $(fdir)/Figure2%svg $(fdir)/Figure3%svg: genFigures.py
	mkdir -p ./Manuscript/Figures
	python3 genFigures.py

Manuscript/Manuscript.pdf: Manuscript/Manuscript.tex
	(cd ./Manuscript && latexmk -xelatex -f -quiet)
	rm -f ./Manuscript/Manuscript.b* ./Manuscript/Manuscript.aux ./Manuscript/Manuscript.fls

Manuscript/index.html: Manuscript/Text/*.md $(fdir)/Figure1.svg $(fdir)/Figure2.svg $(fdir)/Figure3.svg
	pandoc -s $(pan_common) -t html5 --mathjax -c ./Templates/kultiad.css --template=$(tdir)/html.template -o ./Manuscript/index.html

Manuscript/Manuscript.docx: Manuscript/Text/*.md
	pandoc -s $(pan_common) -o ./Manuscript/Manuscript.docx

Manuscript/Manuscript.tex: Manuscript/Text/*.md
	pandoc -s $(pan_common) --filter=$(tdir)/figure-filter.py --template=$(tdir)/default.latex --latex-engine=xelatex -o ./Manuscript/Manuscript.tex

clean:
	rm -f ./Manuscript/Manuscript.* ./Manuscript/index.html
	rm -f $(fdir)/Figure*
	rm -f profile.p*

test:
	python3 -m unittest discover

profile:
	python3 -m cProfile -o profile.pstats genFigures.py
	python3 -m gprof2dot -n 2.0 -f pstats profile.pstats | dot -Tpng -o profile.png

upload:
	lftp -c "set ftp:list-options -a; open athena; cd ./www/fcgr-paper/; lcd ./Manuscript/; mirror --reverse --delete --ignore-time --verbose"
