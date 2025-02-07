Name:		weka-wsa
Version:	1.0
Release:	3%{?dist}
Summary:	WEKA Linux WSA scripts
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

Source101:	set_ip_from_ipmiip.sh  
Source102:	wmsip.txt
Source103:	wekaips.csv  

Source201:	i2c_i801.conf

Source301:	dns.conf
Source302:	dnsmasq.conf

Source401:	99-weka.conf

Source501:	remove_ofed
Source502:	fix_net_interfaces

#Source501:	Weka810.repo

Recommends:	weka-release
Requires:	weka-repos
Recommends:	weka-cockpit-branding
Recommends:	weka-systemd

# fix/remove OFED
Obsoletes:	openmpi
Obsoletes:	kmod-kernel-mft-mlnx
Obsoletes:	kmod-iser
Obsoletes:	kmod-isert
Obsoletes:	kmod-knmem
Obsoletes:	kmod-mlnx-ofa_kernel
Obsoletes:	kmod-srp
Obsoletes:	libxpmem
Obsoletes:	libxpmem-devel
Obsoletes:	mlnx-ofa_kernel
Obsoletes:	mlnx-ofa_kernel-devel
Obsoletes:	mpi-selector
Obsoletes:	dump_pr
Obsoletes:	hcoll
Obsoletes:	kmod-knem
#Requires:	kernel-mft
#Requires:	mft
Requires:	libibverbs <= 58mlnx43-1
Requires:	perftest <= 25
Requires:	rdma-core <= 58mlnx43-1



Requires(pre):	coreutils
Requires(pre):	bash
Requires(post):	jq
Requires(post):	sed

%define workdir	/opt/wekabits
%define netmandir	%{_sysconfdir}/NetworkManager/


%description
Weka Linux WSA scripts

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}%{workdir}/
install -m 0755 %{SOURCE101} %{buildroot}%{workdir}/
install -m 0644 %{SOURCE102} %{buildroot}%{workdir}/
install -m 0644 %{SOURCE103} %{buildroot}%{workdir}/

install -d -m 0755 %{buildroot}%{_sysconfdir}/modprobe.d
install -m 0644 %{SOURCE201} %{buildroot}%{_sysconfdir}/modprobe.d

install -d -m 0755 %{buildroot}%{netmandir}/conf.d
install -d -m 0755 %{buildroot}%{netmandir}/dnsmasq.d
install -m 0644 %{SOURCE301} %{buildroot}%{netmandir}/conf.d
install -m 0644 %{SOURCE302} %{buildroot}%{netmandir}/dnsmasq.d

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d/
install -m 0644 %{SOURCE401} %{buildroot}%{_sysconfdir}/sysctl.d/

install -d -m 0555 %{buildroot}%{_bindir}
install -p -m 0755 %{SOURCE501} %{buildroot}%{_bindir}
install -p -m 0755 %{SOURCE502} %{buildroot}%{_bindir}

%files
%{workdir}/set_ip_from_ipmiip.sh
%config(noreplace) %{workdir}/wmsip.txt
%config(noreplace) %{workdir}/wekaips.csv

%{_sysconfdir}/modprobe.d/*
%{_sysconfdir}/sysctl.d/*

%{netmandir}/conf.d/*
%{netmandir}/dnsmasq.d/*
%{_bindir}

%pre
# for upgrades, if the installed WEKA version is too old to run on Weka Linux 8.10, fail the installation.
if [ -x /usr/bin/weka ]; then
	WEKA_VERS=$(/usr/bin/weka --version | cut '-d ' -f 4)
	WEKA_MAJ=$(echo ${WEKA_VERS} | cut '-d.' -f 1)
	WEKA_MIN=$(echo ${WEKA_VERS} | cut '-d.' -f 2)
	WEKA_DOT=$(echo ${WEKA_VERS} | cut '-d.' -f 3)
	CANCEL="false"
	if [ ${WEKA_MAJ} -lt "4" ]; then
		CANCEL="true"
	elif [ ${WEKA_MIN} -lt "3" ]; then
		CANCEL="true"
	elif [ ${WEKA_DOT} -lt "1" ]; then
		CANCEL="true"
	fi
	if [ ${CANCEL} == "true" ]; then
		echo "******************************************"
		echo
		echo "ERROR: Cannot install %{name} - WEKA version ${WEKA_VERS} is too old.  Update Weka version and try again."
		echo
		echo "******************************************"
		exit 1
	fi
else
	echo "WEKA is not installed on this system"
fi
exit 0

%post
if [ ! -x /usr/bin/weka ]; then
	echo Weka is not installed on this system
	exit 0
fi

# so this next part only runs if WEKA is installed - ie: it's not a fresh OS installation, it's upgrading the OS...
echo "Reconfiguring network interfaces"
echo

get_nic_name() {
	weka local resources --container $1 -J|jq .net_devices[$2].name | tr -d '"'
}

NUM_CONTAINERS=$(weka local ps -J | jq '. | length')
if [ $NUM_CONTAINERS -gt 0 ]; then 
	WEKA_PS=$(weka local ps -J)
	CONTAINER_NAME=$(echo $WEKA_PS | jq .[0].name | tr -d '"')
	CONTAINER_STATE=$(echo $WEKA_PS | jq .[0].internalStatus.display_status | tr -d '"')
else
	echo "******************************************"
	echo
	echo "ERROR: cannot reconfigure network because there are no containers"
	echo "However, we can still proceed - you will have to manually configure the networks"
	echo
	echo "******************************************"
	exit 0
fi

if [ $CONTAINER_STATE == "STEM" ]; then
	echo "******************************************"
	echo
	echo "ERROR: WEKA is in STEM mode"
	echo "However, we can still proceed - you will have to manually configure the networks"
	echo
	echo "******************************************"
	exit 0
fi

# start by looking at the nics defined in weka - make a list of them in use:
for INDEX in 0 1 2 3
do
	NICNAME=$(get_nic_name $CONTAINER_NAME $INDEX)
	if [ NICNAME == "" ]; then
		break
	fi
	# only ETH interfaces change names
	if [ ${NICNAME:0:2} != "ib" ]; then
		NICS[$INDEX]=$NICNAME
		unset NICNAME
	fi
done

SCRIPTDIR=/etc/sysconfig/network-scripts

# now, for each nic, re-swizzle the network config
for NIC in $NICS
do
	NEW=${NIC%np1}
	echo NIC is $NIC - new is $NEW
	source $SCRIPTDIR/ifcfg-$NEW
	if [ "${IPADDR}x" == "x" ]; then
		echo $NEW does not have an ip.  Copying IP settings from $NIC
		sed '/DEVICE/s/np1//' $SCRIPTDIR/ifcfg-$NIC > $SCRIPTDIR/ifcfg-${NEW}
	else
		echo $NEW already has an IP, ignoring
	fi
	unset IPADDR
done

echo "Network reconfiguration complete"; echo

echo "Don't forget to dnf update after this and reboot to activate"


%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
