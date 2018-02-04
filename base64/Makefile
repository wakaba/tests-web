all: clean update

update: update-wpt update-generated

clean: clean-wpt clean-generated

update-generated: decode-generated.json encode-generated.json
clean-generated:
	rm -fr decode-generated.json encode-generated.json

decode-generated.json: generate-decode.pl
	../perl $< > $@
encode-generated.json: generate-encode.pl
	../perl $< > $@

update-wpt: LICENSE.wpt decode-wpt.json
clean-wpt:
	rm -fr LICENSE.wpt decode-wpt.json

LICENSE.wpt:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/LICENSE.md
decode-wpt.json:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/fetch/data-urls/resources/base64.json

## License: Public Domain.
