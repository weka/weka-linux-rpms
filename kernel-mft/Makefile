
.PHONY: all clean Makefile 

SOURCES=$(wildcard SOURCES/*)
SPECS=$(wildcard SPECS/*)

TARG=RPMS/x86_64/kernel-mft-4.30.1-4.18.0_553.36.1.el8_10.x86_64.x86_64.rpm

${TARG}: ${SPECS} ${SOURCES}
	rpmbuild --define "_topdir ${CURDIR}" -ba $<

clean:
	rm -rf ${TARG} BUILD BUILDROOT RPMS SRPMS
