Name:		weka-wms
Version:	1.0
Release:	1%{?dist}
Summary:	WEKA Management Station
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

Source101:	hosts

Requires:	weka-release
Requires:       weka-cockpit-branding
Requires:       weka-systemd
Requires:       weka-wms-gui
Requires:       weka-ansible-install
Requires:	NetworkManager

#%define workdir	/opt/wekabits
#%define netmandir	%{_sysconfdir}/NetworkManager/


%description
Weka Management Station (WMS)

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}%{_sysconfdir}
install -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}

#install -d -m 0755 %{buildroot}%{netmandir}/conf.d
#install -d -m 0755 %{buildroot}%{netmandir}/dnsmasq.d
#install -m 0644 %{SOURCE301} %{buildroot}%{netmandir}/conf.d
#install -m 0644 %{SOURCE302} %{buildroot}%{netmandir}/dnsmasq.d

#install -d -m 0755 %{buildroot}%{_sysconfdir}/sysctl.d/
#install -m 0644 %{SOURCE401} %{buildroot}%{_sysconfdir}/sysctl.d/

%files
#%{workdir}/set_ip_from_ipmiip.sh
#%config(noreplace) %{workdir}/wmsip.txt
#%config(noreplace) %{workdir}/wekaips.csv

%{_sysconfdir}/*
#%{_sysconfdir}/sysctl.d/*

#%{netmandir}/conf.d/*
#%{netmandir}/dnsmasq.d/*



%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
