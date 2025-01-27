Name:		weka-wsa
Version:	1.0
Release:	1%{?dist}
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

#Source501:	Weka810.repo

Recommends:	weka-release
Recommends:	weka-repos
Recommends:	weka-cockpit-branding
Recommends:	weka-systemd
#Requires:	NetworkManager
Requires(pre):	coreutils
Requires(pre):	bash

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

#install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
#install -p -m 0644 %{SOURCE501} %{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%{workdir}/set_ip_from_ipmiip.sh
%config(noreplace) %{workdir}/wmsip.txt
%config(noreplace) %{workdir}/wekaips.csv

%{_sysconfdir}/modprobe.d/*
%{_sysconfdir}/sysctl.d/*

%{netmandir}/conf.d/*
%{netmandir}/dnsmasq.d/*
#%config %{_sysconfdir}/yum.repos.d/*

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


%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
