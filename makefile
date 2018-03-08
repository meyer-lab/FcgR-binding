NPROCS := 8

fdir = ./Manuscript/Figures
tdir = ./Manuscript/Templates
pan_common = -F pandoc-crossref -F pandoc-citeproc --filter=$(tdir)/figure-filter.py -f markdown ./Manuscript/Text/*.md

.PHONY: clean upload test profile testcover open rebuild sample sampleprofile

all: Manuscript/index.html Manuscript/Manuscript.pdf Manuscript/Manuscript.docx Manuscript/CoverLetter.docx Manuscript/ReviewResponse.docx Manuscript/ReviewResponse.pdf

$(fdir)/Figure%.svg: genFigures.py recepmod/recepmod.so
	mkdir -p ./Manuscript/Figures
	python3 genFigures.py $*

$(fdir)/Figure%pdf: $(fdir)/Figure%svg
	rsvg-convert --background-color=white -f pdf $< -o $@

$(fdir)/Figure%eps: $(fdir)/Figure%svg
	rsvg-convert --background-color=white -f eps $< -o $@

recepmod/recepmod.so: recepmod/solverC.cpp
	g++ -std=c++11 -mavx -march=native $< -O3 --shared -fPIC -lm -o $@

Manuscript/Manuscript.pdf: Manuscript/Manuscript.tex $(fdir)/Figure1.pdf $(fdir)/Figure2.pdf $(fdir)/Figure3.pdf $(fdir)/Figure4.pdf $(fdir)/FigureS2.pdf $(fdir)/FigureAA.pdf
	(cd ./Manuscript && latexmk -xelatex -f -quiet)
	rm -f ./Manuscript/Manuscript.b* ./Manuscript/Manuscript.aux ./Manuscript/Manuscript.fls

Manuscript/index.html: Manuscript/Text/*.md $(fdir)/Figure1.svg $(fdir)/Figure2.svg $(fdir)/Figure3.svg $(fdir)/Figure4.svg $(fdir)/FigureS2.svg $(fdir)/FigureAA.svg Manuscript/Text/07_ModelData.md
	pandoc -s $(pan_common) -t html5 --mathjax -c ./Templates/kultiad.css --template=$(tdir)/html.template -o $@

Manuscript/Manuscript.docx: Manuscript/Text/*.md $(fdir)/Figure1.eps $(fdir)/Figure2.eps $(fdir)/Figure3.eps $(fdir)/Figure4.eps $(fdir)/FigureS2.eps $(fdir)/FigureAA.eps Manuscript/Text/07_ModelData.md
	cp -R $(fdir) ./
	pandoc -s $(pan_common) -o $@
	rm -r ./Figures

Manuscript/Text/07_ModelData.md: recepmod/recepmod.so
	python3 -c "from recepmod.StoneModMouse import StoneModelMouse; StoneModelMouse().writeModelData('./Manuscript/Text/07_ModelData.md')"

Manuscript/ReviewResponse.docx: Manuscript/ReviewResponse.md
	pandoc -s -f markdown $< -o $@

Manuscript/ReviewResponse.pdf: Manuscript/ReviewResponse.md
	pandoc -s --pdf-engine=xelatex -f markdown $< -o $@

Manuscript/Manuscript.tex: Manuscript/Text/*.md Manuscript/Text/07_ModelData.md
	pandoc -s $(pan_common) --template=$(tdir)/default.latex --pdf-engine=xelatex -o $@

Manuscript/CoverLetter.docx: Manuscript/CoverLetter.md
	pandoc -f markdown $< -o $@

Manuscript/CoverLetter.pdf: Manuscript/CoverLetter.md
	pandoc --pdf-engine=xelatex --template=/Users/asm/.pandoc/letter-templ.tex $< -o $@

clean:
	rm -f ./Manuscript/Manuscript.* ./Manuscript/index.html Manuscript/CoverLetter.docx Manuscript/CoverLetter.pdf
	rm -f $(fdir)/Figure* recepmod/recepmod.so Manuscript/Text/07_ModelData.md profile.p* stats.dat .coverage nosetests.xml
	rm -f Manuscript/ReviewResponse.docx Manuscript/ReviewResponse.pdf

open: Manuscript/index.html
	open ./Manuscript/index.html

test: recepmod/recepmod.so
	nosetests3 -s --with-timer --timer-top-n 5

profile: recepmod/recepmod.so
	nosetests3 -s --with-timer --timer-top-n 5 --with-cprofile
	snakeviz stats.dat

testcover: recepmod/recepmod.so
	nosetests3 --with-xunit --with-xcoverage --cover-package=recepmod -s --with-timer --timer-top-n 5

sample: recepmod/recepmod.so
	python3 -c "from recepmod.fitFuncs import runSampler; runSampler()"

sampleprofile: recepmod/recepmod.so
	python3 -c "from recepmod.fitFuncs import runSampler; import cProfile; cProfile.run('runSampler(niters=200, npar=1)', 'stats.dat')"
	snakeviz stats.dat