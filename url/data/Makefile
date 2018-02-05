all: clean update

update: update-wpt
clean: clean-wpt

update-wpt: LICENSE.wpt parse-wpt.json
clean-wpt:
	rm -fr LICENSE.wpt parse-wpt.json

LICENSE.wpt:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/LICENSE.md
parse-wpt.json:
	wget -O $@ https://raw.githubusercontent.com/w3c/web-platform-tests/master/fetch/data-urls/resources/data-urls.json

## License: Public Domain.
