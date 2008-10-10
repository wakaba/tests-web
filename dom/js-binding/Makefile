WTTJS_PL = /home/httpd/html/www/webidl2tests/bin/wttjs.pl

all: webdomcore html xhr

webdomcore:
	perl $(WTTJS_PL) --idl-file-name idls/webdomcore-20081008.idl \
	    --instances-file-name idls/webdomcore.json \
	    --test-dir-name tests/ \
	    --testset-id webdomcore-20081008

html:
	perl $(WTTJS_PL) --idl-file-name idls/html5-r2321.idl \
	    --instances-file-name idls/html.json \
	    --test-dir-name tests/ \
	    --testset-id html5-r2321

xhr:
	perl $(WTTJS_PL) --idl-file-name idls/xhr2-20081006.idl \
	    --instances-file-name idls/xhr.json \
	    --test-dir-name tests/ \
	    --testset-id xhr2-20081006
