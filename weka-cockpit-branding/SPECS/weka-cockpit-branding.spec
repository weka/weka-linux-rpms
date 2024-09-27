Name:		weka-cockpit-branding
Version:	1.0
Release:	1%{?dist}
Summary:	WEKA Linux Customizations
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

Requires:	coreutils
Requires:	tar
Requires:	findutils

# These all get installed in /usr/share/cockpit/branding/weka/
Source0:	weka-cockpit-branding.tgz

%description
Cockpit customizations to WEKA Rocky Linux

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}%{_datadir}/cockpit/branding/weka/
tar xvf %{SOURCE0} -C %{buildroot}%{_datadir}/cockpit/branding/weka/

find %{buildroot}

%files
%{_datadir}/cockpit/branding/weka/*

%changelog
* Tue Aug 27 2024 Vince Fleming <vince@weka.io>
-- 
