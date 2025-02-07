
.PHONY: all clean Makefile 

SOURCES=$(wildcard SOURCES/*)
SPECS=$(wildcard SPECS/*)

TARG=RPMS/x86_64/iperf3-3.18-11.el8.x86_64.rpm

${TARG}: ${SPECS} ${SOURCES}
	rpmbuild --define "_topdir ${CURDIR}" -ba $<

clean:
	rm -rf ${TARG} BUILD BUILDROOT RPMS SRPMS
