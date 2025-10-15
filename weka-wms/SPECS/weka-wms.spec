# this rpm just ensures that all the other required rpms get installed
Name:		weka-wms
Version:	2.0
Release:	1%{?dist}
Summary:	WEKA Management Station
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

Requires:	weka-release
Requires:       weka-cockpit-branding
Requires:       weka-systemd
Recommends:       weka-wms-gui
Recommends:       wekahome
#Recommends:       weka-tools
Recommends:       weka-mon

Source0:	podman.sh
Source1:        95-weka-podman.preset

Source105:      netissue.service
Source205:      netissue.sh

%description
Weka Management Station (WMS)

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}/etc/profile.d
install -m 0644 %{SOURCE0} %{buildroot}/etc/profile.d/

install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/

install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE105} %{buildroot}%{_unitdir}

install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 %{SOURCE205} %{buildroot}%{_bindir}

%post
%systemd_post netissue.service

%preun
%systemd_preun netissue.service

%postun
%{?ldconfig}
%systemd_postun_with_restart netissue.service

%files
/etc/*
%{_prefix}/lib/systemd/system-preset/*
%{_unitdir}/*
%{_bindir}/*

%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
