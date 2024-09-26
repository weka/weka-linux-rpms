# weka-linux-rpms
Several RPMs that customize Rocky Linux into WEKA Linux


## Prerequisites
Be sure to install these packages:
rpmlint
rpm-libs
rpm-build-libs
rpm-plugin-selinux
rpm-build
rpm
rpm-plugin-systemd-inhibit
rpm-sign
rpmdevtools

This build env could probably be run on any RHEL-derivitive (version 8.x), but has only been tested with Rocky 8.10.

## Build Procedure
We intend to provide a Makefile someday, but until then, run the provided `build_all` shell script.  This will re-create ALL of the RPMs (it's quick).

The `copy_to_62` script will copy the .src.rpm and .rpm files to another server - in this case, #62.  Change this as needed. ;)
