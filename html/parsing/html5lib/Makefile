all: html5lib-tests htmlparser-data-manakai-2.diff

html5lib-tests:
	git clone git://github.com/html5lib/html5lib-tests.git tmp/html5lib-tests || \
	(cd tmp/html5lib-tests && git pull)
	cp tmp/html5lib-tests/tokenizer/*.test html-tokenizer/
	cp tmp/html5lib-tests/tree-construction/*.dat html-tree/
	cp tmp/html5lib-tests/LICENSE html-tokenizer/
	cp tmp/html5lib-tests/LICENSE html-tree/
	#patch -p3 < htmlparser-data-manakai.diff
	#patch -p4 < htmlparser-data-manakai-2.diff

htmlparser-data-manakai-2.diff: html-tokenizer html-tree
	git diff 8cd5c6ce266cdfa96bb7a1c6eb2f723b27c4628d -- html-tokenizer html-tree > $@
