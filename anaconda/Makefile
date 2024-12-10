
.PHONY: all clean Makefile 

SOURCES=$(wildcard SOURCES/*)
SPECS=$(wildcard SPECS/*)

TARG=weka-release/RPMS/noarch/weka-release-8.10-50.2.el8.noarch.rpm

${TARG}: ${SPECS} ${SOURCES}
	rpmbuild --define "_topdir ${CURDIR}" -ba $<

clean:
	rm -rf ${TARG} BUILD BUILDROOT RPMS SRPMS
