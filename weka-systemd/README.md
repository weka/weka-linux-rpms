# weka-systemd
An RPM to add WEKA-specific systemd units


## Prerequisites
This RPM is intended to be installed on/with a base Rocky 8.10.  It may not work and has not been tested on any other RHEL derivitive or Rocky release.

## Provides
This repo will provide the following RPMS:

weka-systemd-1.0-1.el8.noarch.rpm

## How to modify
The contents are in the SOURCES directory.

Edit the files as needed, and build the RPM.

## function
This RPM adds some special units.
firstboot - run only the first time the server boots (after installation)
everyboot - run every time the server boots
netissue.sh - run anytime the ip configuration of the server changes
avahi - configures Avahi (bonjour/zerconf) so we can leverage some auto-discovery features
