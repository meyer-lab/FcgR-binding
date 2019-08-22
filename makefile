fdir = ./Manuscript/Figures
tdir = ./Manuscript/Templates
pan_common = -F pandoc-crossref -F pandoc-citeproc --filter=$(tdir)/figure-filter.py -f markdown ./Manuscript/Text/*.md

.PHONY: clean upload test testcover open sample

all: Manuscript/index.html Manuscript/Manuscript.pdf Manuscript/Manuscript.docx Manuscript/CoverLetter.docx Manuscript/ReviewResponse.docx Manuscript/ReviewResponse.pdf

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --system-site-packages venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/bin/activate

$(fdir)/Figure%.svg: genFigures.py venv recepmod/recepmod.so
	mkdir -p ./Manuscript/Figures
	. venv/bin/activate && python3 genFigures.py $*

$(fdir)/Figure%pdf: $(fdir)/Figure%svg
	rsvg-convert -f pdf $< -o $@

$(fdir)/Figure%eps: $(fdir)/Figure%svg
	rsvg-convert -f eps $< -o $@

recepmod/recepmod.so: recepmod/solverC.cpp
	g++ -std=c++11 -mavx -march=native $< -O3 --shared -fPIC -lm -o $@

Manuscript/Manuscript.pdf: Manuscript/Manuscript.tex $(fdir)/Figure1.pdf $(fdir)/Figure2.pdf $(fdir)/Figure3.pdf $(fdir)/Figure4.pdf $(fdir)/FigureS2.pdf $(fdir)/FigureAA.pdf
	(cd ./Manuscript && latexmk -xelatex -f -quiet)
	rm -f ./Manuscript/Manuscript.b* ./Manuscript/Manuscript.aux ./Manuscript/Manuscript.fls

Manuscript/index.html: Manuscript/Text/*.md $(fdir)/Figure1.svg $(fdir)/Figure2.svg $(fdir)/Figure3.svg $(fdir)/Figure4.svg $(fdir)/FigureS2.svg $(fdir)/FigureAA.svg
	pandoc -s $(pan_common) -t html5 --mathjax -c ./Templates/kultiad.css --template=$(tdir)/html.template -o $@

Manuscript/Manuscript.docx: Manuscript/Text/*.md $(fdir)/Figure1.eps $(fdir)/Figure2.eps $(fdir)/Figure3.eps $(fdir)/Figure4.eps $(fdir)/FigureS2.eps $(fdir)/FigureAA.eps
	cp -R $(fdir) ./
	pandoc -s $(pan_common) -o $@
	rm -r ./Figures

ModelData.md: venv recepmod/recepmod.so
	. venv/bin/activate && python3 -c "from recepmod.StoneModMouse import StoneModelMouse; StoneModelMouse().writeModelData('ModelData.md')"

Manuscript/ReviewResponse.docx: Manuscript/ReviewResponse.md
	pandoc -s -f markdown $< -o $@

Manuscript/ReviewResponse.pdf: Manuscript/ReviewResponse.md
	pandoc -s --pdf-engine=xelatex -f markdown $< -o $@

Manuscript/Manuscript.tex: Manuscript/Text/*.md
	pandoc -s $(pan_common) --template=$(tdir)/default.latex --pdf-engine=xelatex -o $@

Manuscript/CoverLetter.docx: Manuscript/CoverLetter.md
	pandoc -f markdown $< -o $@

Manuscript/CoverLetter.pdf: Manuscript/CoverLetter.md
	pandoc --pdf-engine=xelatex --template=/Users/asm/.pandoc/letter-templ.tex $< -o $@

Manuscript/CoverLetterResponse.pdf: Manuscript/CoverLetterResponse.md
	pandoc --pdf-engine=xelatex --template=/Users/asm/.pandoc/letter-templ.tex $< -o $@

clean:
	rm -f ./Manuscript/Manuscript.* ./Manuscript/index.html Manuscript/CoverLetter.docx Manuscript/CoverLetter.pdf
	rm -f $(fdir)/Figure* recepmod/recepmod.so ModelData.md profile.p* stats.dat .coverage nosetests.xml
	rm -f Manuscript/ReviewResponse.docx Manuscript/ReviewResponse.pdf

open: Manuscript/index.html
	open ./Manuscript/index.html

test: venv recepmod/recepmod.so
	. venv/bin/activate && pytest

testcover: venv recepmod/recepmod.so
	. venv/bin/activate && pytest --cov=./recepmod

sample: venv recepmod/recepmod.so
	. venv/bin/activate && python3 -c "from recepmod.fitFuncs import runSampler; runSampler()"
