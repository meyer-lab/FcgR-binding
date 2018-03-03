NPROCS := 8

fdir = ./Manuscript/Figures
tdir = ./Manuscript/Templates
pan_common = -F pandoc-crossref -F pandoc-citeproc --filter=$(tdir)/figure-filter.py -f markdown ./Manuscript/Text/*.md

.PHONY: clean upload test profile testcover open rebuild sample sampleprofile

all: Manuscript/index.html Manuscript/Manuscript.pdf Manuscript/Manuscript.docx Manuscript/CoverLetter.docx

$(fdir)/Figure%.svg: genFigures.py
	mkdir -p ./Manuscript/Figures
	python3 genFigures.py $*

$(fdir)/Figure%pdf: $(fdir)/Figure%svg
	rsvg-convert -f pdf $< -o $@

$(fdir)/Figure%eps: $(fdir)/Figure%svg
	rsvg-convert -f eps $< -o $@

Manuscript/Manuscript.pdf: Manuscript/Manuscript.tex $(fdir)/Figure1.pdf $(fdir)/Figure2.pdf $(fdir)/Figure3.pdf $(fdir)/Figure4.pdf $(fdir)/FigureS2.pdf $(fdir)/FigureAA.pdf
	(cd ./Manuscript && latexmk -xelatex -f -quiet)
	rm -f ./Manuscript/Manuscript.b* ./Manuscript/Manuscript.aux ./Manuscript/Manuscript.fls

Manuscript/index.html: Manuscript/Text/*.md $(fdir)/Figure1.svg $(fdir)/Figure2.svg $(fdir)/Figure3.svg $(fdir)/Figure4.svg $(fdir)/FigureS2.svg $(fdir)/FigureAA.svg
	pandoc -s $(pan_common) -t html5 --mathjax -c ./Templates/kultiad.css --template=$(tdir)/html.template -o $@

Manuscript/Manuscript.docx: Manuscript/Text/*.md $(fdir)/Figure1.eps $(fdir)/Figure2.eps $(fdir)/Figure3.eps $(fdir)/Figure4.eps $(fdir)/FigureS2.eps $(fdir)/FigureAA.eps
	cp -R $(fdir) ./
	pandoc -s $(pan_common) -o $@
	rm -r ./Figures

Manuscript/Manuscript.tex: Manuscript/Text/*.md Manuscript/index.html
	pandoc -s $(pan_common) --template=$(tdir)/default.latex --latex-engine=xelatex -o $@

Manuscript/CoverLetter.docx: Manuscript/CoverLetter.md
	pandoc -f markdown $< -o $@

Manuscript/CoverLetter.pdf: Manuscript/CoverLetter.md
	pandoc --latex-engine=xelatex --template=/Users/asm/.pandoc/letter-templ.tex $< -o $@

clean:
	rm -f ./Manuscript/Manuscript.* ./Manuscript/index.html Manuscript/Figures/ModelData.md Manuscript/CoverLetter.docx Manuscript/CoverLetter.pdf
	rm -f $(fdir)/Figure*
	rm -f Manuscript/Text/07_ModelData.md
	rm -f profile.p* stats.dat .coverage nosetests.xml

open: Manuscript/index.html
	open ./Manuscript/index.html

test:
	nosetests3 -s --with-timer --timer-top-n 5

profile:
	nosetests3 -s --with-timer --timer-top-n 5 --with-cprofile
	snakeviz stats.dat

testcover:
	nosetests3 --with-xunit --with-xcoverage --cover-package=recepmod -s --with-timer --timer-top-n 5

sample:
	python3 -c "from recepmod.fitFuncs import runSampler; runSampler()"

sampleprofile:
	python3 -c "from recepmod.fitFuncs import runSampler; import cProfile; cProfile.run('runSampler(niters=200, npar=1)', 'stats.dat')"
	snakeviz stats.dat