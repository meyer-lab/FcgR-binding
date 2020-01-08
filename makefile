fdir = ./Manuscript/Figures
tdir = ./Manuscript/Templates
pan_common = -F pandoc-crossref -F pandoc-citeproc --filter=$(tdir)/figure-filter.py -f markdown ./Manuscript/Text/*.md

.PHONY: clean upload test testcover open sample

all: Manuscript/Manuscript.pdf Manuscript/CoverLetter.docx Manuscript/ReviewResponse.docx pylint.log

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --system-site-packages venv
	tlmgr install cslreferences
	. venv/bin/activate && pip install -Uqr requirements.txt
	touch venv/bin/activate

$(fdir)/Figure%.svg: genFigures.py venv
	mkdir -p ./Manuscript/Figures
	. venv/bin/activate && python3 genFigures.py $*

$(fdir)/Figure%pdf: $(fdir)/Figure%svg
	rsvg-convert -f pdf $< -o $@

Manuscript/Manuscript.pdf: Manuscript/Manuscript.tex $(fdir)/Figure1.pdf $(fdir)/Figure2.pdf $(fdir)/Figure3.pdf $(fdir)/Figure4.pdf $(fdir)/FigureS2.pdf $(fdir)/FigureAA.pdf
	(cd ./Manuscript && latexmk -xelatex -f -quiet)
	rm -f ./Manuscript/Manuscript.b* ./Manuscript/Manuscript.aux ./Manuscript/Manuscript.fls

ModelData.md: venv
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
	rm -f ./Manuscript/Manuscript.* Manuscript/CoverLetter.docx Manuscript/CoverLetter.pdf
	rm -f $(fdir)/Figure* ModelData.md profile.p* stats.dat .coverage nosetests.xml
	rm -f Manuscript/ReviewResponse.docx Manuscript/ReviewResponse.pdf
	rm -rf venv

open: Manuscript/index.html
	open ./Manuscript/index.html

pylint.log: venv .pylintrc
	. venv/bin/activate && (pylint --rcfile=.pylintrc recepmod > pylint.log || echo "pylint3 exited with $?")

test: venv
	. venv/bin/activate && pytest

testcover: venv
	. venv/bin/activate && pytest --junitxml=junit.xml --cov-branch --cov=recepmod --cov-report xml:coverage.xml

sample: venv
	. venv/bin/activate && python3 -c "from recepmod.fitFuncs import runSampler; runSampler()"
