all: html5lib-tests htmlparser-data-manakai.diff

html5lib-tests:
	git clone git://github.com/html5lib/html5lib-tests.git tmp/html5lib-tests || \
	(cd tmp/html5lib-tests && git pull)
	cp tmp/html5lib-tests/tokenizer/*.test html-tokenizer/
	cp tmp/html5lib-tests/tree-construction/*.dat html-tree/
	cp tmp/html5lib-tests/LICENSE html-tokenizer/
	cp tmp/html5lib-tests/LICENSE html-tree/
	patch -p4 < htmlparser-data-manakai.diff

htmlparser-data-manakai.diff: html-tokenizer html-tree
	git diff --text 4d425bc -- html-tokenizer html-tree > $@
