Name:		weka-cockpit-branding
Version:	1.0
Release:	1%{?dist}
Summary:	WEKA Linux Customizations
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

# These all get installed in /usr/share/cockpit/branding/rocky/
Source0:	weka-cockpit-branding.tgz

%description
Cockpit customizations to WEKA Rocky Linux

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}
tar xvf %{SOURCE0} -C %{buildroot}

find %{buildroot}

%files
%{_datadir}/cockpit/branding/rocky/*

%changelog
* Tue Aug 27 2024 Vince Fleming <vince@weka.io>
-- 
