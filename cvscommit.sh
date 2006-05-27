#!/bin/sh
find -name ChangeLog | xargs cvs diff | grep "^\+" | sed -e "s/^\+//; s/^\+\+ .\//++ test\//" > .cvslog.tmp
cvs commit -F .cvslog.tmp $1 $2 $3 $4 $5 $6 $7 $8 $9 
rm .cvslog.tmp

## $Date: 2006/05/27 08:32:17 $
## License: Public Domain
