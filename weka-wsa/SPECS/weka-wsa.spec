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

Requires:	weka-rocky-release
Requires:       weka-cockpit-branding
Requires:       weka-systemd
Requires:	NetworkManager

%define workdir	/opt/wekabits
%define netmandir	%{_sysconfdir}/NetworkManager/


%description
Weka Rocky Linux WSA scripts

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}%{workdir}/
install -m 0644 %{SOURCE101} %{buildroot}%{workdir}/
install -m 0644 %{SOURCE102} %{buildroot}%{workdir}/
install -m 0644 %{SOURCE103} %{buildroot}%{workdir}/

install -d -m 0755 %{buildroot}%{_sysconfdir}/modprobe.d
install -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/modprobe.d

install -d -m 0755 %{buildroot}%{netmandir}/conf.d
install -d -m 0755 %{buildroot}%{netmandir}/dnsmasq.d
install -m 0644 %{SOURCE301} %{buildroot}%{netmandir}/conf.d
install -m 0644 %{SOURCE302} %{buildroot}%{netmandir}/dnsmasq.d

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d/
install -m 0644 %{SOURCE401} %{buildroot}%{_sysconfdir}/sysctl.d/

%files
%{workdir}/set_ip_from_ipmiip.sh
%config(noreplace) %{workdir}/wmsip.txt
%config(noreplace) %{workdir}/wekaips.csv

%{_sysconfdir}/modprobe.d/*

%{netmandir}/conf.d/*
%{netmandir}/dnsmasq.d/*

%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
