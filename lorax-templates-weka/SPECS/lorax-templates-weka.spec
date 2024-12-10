Name:             lorax-templates-weka
Version:          8.10
Release:          3%{?dist}
Summary:          Rocky Linux 8 build templates for lorax and livemedia-creator

License:          GPLv2+
URL:              https://github.com/weldr/lorax
BuildArch:        noarch
Source0:          lorax-templates-weka-8.10.tgz

# Required for the template branding support
Requires:         lorax > 28.14.68
Provides:         lorax-templates-weka = %{version}-%{release}
Obsoletes:        lorax-templates-rhel < %{version}-%{release}

# Where are these supposed to end up?
%define templatedir %{_datadir}/lorax/templates.d/80-weka

%description
EL-specific Lorax templates for creating the boot.iso and live isos are
placed in %{templatedir}

%prep
%setup -n lorax-templates-weka-%{version}

%build
# nothing to build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{templatedir}
cp -a 80-weka/* $RPM_BUILD_ROOT/%{templatedir}

%files
%dir %{templatedir}
%{templatedir}/*

%changelog
* Mon Feb 12 2024 Louis Abel <label@resf.org> - 8.10-3
- Reduce requires for lorax

* Wed Feb 07 2024 Louis Abel <label@resf.org> - 8.10-2
- Update to upstream: 8.10

* Tue Feb 06 2024 Louis Abel <label@rockylinux.org> - 8.7-4
- Update to upstream: Remove libreport bugzilla plugins

* Tue Jan 23 2024 Louis Abel <label@resf.org> - 8.7-3
- Initial build of lorax-templates-rocky, based on rhel
