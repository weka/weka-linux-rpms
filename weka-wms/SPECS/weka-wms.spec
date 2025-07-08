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
Recommends:       weka-ansible-install
Recommends:       wekahome
Recommends:       weka-tools
Recommends:       weka-mon
#Requires:	NetworkManager

%description
Weka Management Station (WMS)

%build
echo Good

%install

%files


%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
