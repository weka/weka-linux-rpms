
.PHONY: all clean Makefile 

SOURCES=$(wildcard SOURCES/*)
SPECS=$(wildcard SPECS/*)

TARG=./RPMS/noarch/weka-wsa-1.0-1.el8.noarch.rpm

${TARG}: ${SPECS} ${SOURCES}
	rpmbuild --define "_topdir ${CURDIR}" -ba $<

clean:
	rm -rf ${TARG} BUILD BUILDROOT RPMS SRPMS
