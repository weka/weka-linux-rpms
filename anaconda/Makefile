
.PHONY: all clean Makefile 

SOURCES=$(wildcard SOURCES/*)
SPECS=$(wildcard SPECS/*)

TARG=RPMS/x86_64/anaconda-33.16.10.5-50.el8.weka.0.2.x86_64.rpm

${TARG}: ${SPECS} ${SOURCES}
	rpmbuild --define "_topdir ${CURDIR}" -ba $<

clean:
	rm -rf ${TARG} BUILD BUILDROOT RPMS SRPMS
