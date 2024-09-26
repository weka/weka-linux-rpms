# weka-rocky-release
An RPM to WEKA-brand the OS


## Prerequisites
This RPM is intended to be installed on/with a base Rocky 8.10.  It may not work and has not been tested on any other RHEL derivitive or Rocky release.

## Provides
This repo will provide the following RPMS:

rocky-gpg-keys-8.10-50.2.el8.noarch.rpm - GPG keys used by Rocky (We're not using GPG yet on our (ie: these) RPMs
rocky-sb-certs-8.10-50.2.el8.noarch.rpm	- certs provided by the base code (blatently stolen from Rocky 8.10)
weka-rocky-release-8.10-50.2.el8.noarch.rpm - release specific stuff like building the /etc/os-release file
weka-rocky-repos-8.10-50.2.el8.noarch.rpm  - repo definitions that point to OUR repos instead of Rocky's repos.

## How to modify
The contents are in the SOURCES directory.

Edit the files as needed, and build the RPM.

