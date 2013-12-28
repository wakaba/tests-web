HG = hg

all: htmlparser-data htmlparser-data-manakai-2.diff

htmlparser-data:
	mkdir -p tmp html-tokenizer html-tree
	$(HG) clone https://code.google.com/p/html5lib/ tmp/html5lib || \
	    (cd tmp/html5lib && $(HG) pull -u)
	cp -R tmp/html5lib/testdata/tokenizer/* html-tokenizer/
	cp tmp/html5lib/LICENSE html-tokenizer/
	cp -R tmp/html5lib/testdata/tree-construction/* html-tree/
	cp tmp/html5lib/LICENSE html-tree/
	patch -p3 < htmlparser-data-manakai.diff
	patch -p4 < htmlparser-data-manakai-2.diff

htmlparser-data-manakai-2.diff: html-tokenizer html-tree
	git diff 8cd5c6ce266cdfa96bb7a1c6eb2f723b27c4628d -- html-tokenizer html-tree > $@
