#!/bin/bash

#
# set ip of first active ethernet connection via $IPFILE
# also set gateway, dns, hostname from the file
# $IPFILE is searched for local IPMI IP for above info
#
# usage: ./set_ip_from_ipmi_ip.sh [<ipfile>]
#    <ipfile> is optional, default is 'wekaips.csv'
#
cwd="$PWD"
sdir=$(dirname $(realpath "$0"))
WMSIPF="$sdir/wmsip.txt"
IPFILE="$sdir/wekaips.csv"

if [[ -n "$1" ]]; then
    IPFILE=$(realpath "$1")
fi
echo "IP file is '$IPFILE'"
wekaips="$(cat ${IPFILE})"

ipmiip=$(ipmitool lan print | sed -n -r "s/IP Address\s*:\s*//p")
my_new_net=$(echo "$wekaips" | grep "$ipmiip")

if [[ "$?" == 0 && -n "$my_new_net" ]]; then
    ar=(${my_new_net//,/ })
    ip_and_nm=${ar[1]}
    new_gw=${ar[2]}
    new_dns=${ar[3]}
    new_name=${ar[4]}
    ethcon=$(nmcli --terse con show --active | grep -m 1 -o "[^:]*" | head -1)
    echo "Modifying $ethcon: hostname=$new_name, ip/nm=$ip_and_nm, gw=$new_gw, dns=$new_dns"
    nmcli con mod "$ethcon" ipv4.method manual ipv4.addresses "$ip_and_nm"
    nmcli con mod "$ethcon" ipv4.gateway "$new_gw"
    nmcli con mod "$ethcon" ipv4.dns "$new_dns"
    nmcli gen hostname "$new_name"
    nmcli con down "$ethcon" ; nmcli con up "$ethcon"
else
    if [[ ! -f "$IPFILE" ]]; then
        echo "Error: File '$IPFILE' not found"
    else
        echo "Error: IPMI ip '$ipmiip' not found in file '$IPFILE'"
    fi
fi

