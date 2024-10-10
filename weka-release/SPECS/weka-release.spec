# Note to packagers/builders:
#
# If you wish to build the LookAhead or Beta variant of this package, make sure
# that you are setting --with=rlbeta or --with=rllookahead on your mock
# command. See the README for more information.

%bcond_with rlbeta
%bcond_with rllookahead
%bcond_with rloverride

%define debug_package %{nil}

# Product information
%define product_family WEKA Linux
%define variant_titlecase Server
%define variant_lowercase server

# Distribution Name and Version
%define distro_name  Weka Linux
%define distro       %{distro_name}
%define distro_code  Fledgeling
%define major        8
%define minor        10
%define rocky_rel    1%{?rllh:.%{rllh}}%{!?rllh:.9}
%define upstream_rel %{major}.%{minor}-0.2
%define rpm_license  BSD-3-Clause
%define dist         .el%{major}
%define home_url     https://weka.io/
%define bug_url      https://support.weka.io
%define debug_url    https://support.weka.io
%define dist_vendor  RESF

%define contentdir   pub/weka
%define sigcontent   pub/sig
%define rlosid       weka

%define os_bug_name  Weka-Linux-%{major}

################################################################################
# Weka LookAhead Section
#
# Reset defines for LookAhead variant. Default is stable if 0 or undefined.
%if %{with rllookahead}
%define minor        8
%define contentdir   pub/weka-lh
%define rltype       -lookahead
%define rlstatement  LookAhead
%endif
# End Weka LookAhead Section
################################################################################

################################################################################
# Weka Beta Section
#
# Reset defines for Beta variant. Default is stable if 0 or undefined.
# We do NOT override the minor version number here.
%if %{with rlbeta}
%define contentdir   pub/weka-beta
%define rltype       -beta
%define rlstatement  Beta
%endif
# End Weka Beta Section
################################################################################

################################################################################
# Weka Override Section
#
# Resets only the dist tag for the override package. All this does is ensure
# that only the rhel macros and settings are provided - This is useful in the
# case of a build that cannot be properly debranded (eg dotnet).
%if %{with rloverride}
%define dist         .el%{major}.override
%define rlosid       rhel
%endif
# End Weka Override Section
################################################################################

%define base_release_version %{major}
%define dist_release_version %{major}
%define full_release_version %{major}.%{minor}

%ifarch ppc64le
%define tuned_profile :server
%endif

# Avoids a weird anaconda problem
%global __requires_exclude_from %{_libexecdir}

# conditional section for future use

Name:           weka-release%{?rltype}
Version:        8.10
Release:        50.2%{?dist}
Summary:        %{distro_name} release files
Group:          System Environment/Base
License:        %{rpm_license}
URL:            https://weka.io
BuildArch:      noarch

# What do we provide? Some of these needs are a necesity (think comps and
# groups) and things like EPEL need it.
Provides:       weka-release = %{version}-%{release}
Provides:       weka-release(upstream) = %{full_release_version}
Provides:       rocky-release = %{version}-%{release}
Provides:       rocky-release(upstream) = %{full_release_version}
Provides:       redhat-release = %{upstream_rel}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{major}
Provides:       centos-release = %{version}-%{release}
Provides:       centos-release(upstream) = %{full_release_version}

## Required by libdnf
Provides:       base-module(platform:el%{major})

## This makes lorax/pungi/anaconda happy
Provides:       weka-release-eula  = %{version}-%{release}
Provides:       rocky-release-eula  = %{version}-%{release}
Provides:       redhat-release-eula = %{upstream_rel}
Provides:       centos-release-eula = %{version}-%{release}

# What are our requirements?
Requires:       weka-repos(%{major})
Requires:	sed
#Requires:       weka-cockpit-branding
#Requires:       weka-systemd

Obsoletes:	weka-rocky-lts86-release
Obsoletes:	ciq-lts86-rocky-release
Obsoletes:	rocky-release

# GPG Keys (100-199)
Source101:      RPM-GPG-KEY-rockyofficial
Source102:      RPM-GPG-KEY-rockytesting

# Release Sources (200-499)
Source200:      EULA
Source201:      LICENSE
Source202:      Contributors
Source203:      COMMUNITY-CHARTER

# !! Stable !!
Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      99-default-disable.preset
Source303:      95-weka.preset


# Repo Sources
Source1200:     Weka-BaseOS.repo
Source1201:     Weka-AppStream.repo
Source1202:     Rocky-PowerTools.repo
Source1203:     Rocky-Extras.repo
Source1204:     Weka.repo
Source1205:     Ofed.repo

# Rocky Add-ons
Source1210:     Rocky-HighAvailability.repo
Source1211:     Rocky-ResilientStorage.repo
Source1212:     Rocky-RT.repo
Source1213:     Rocky-NFV.repo

# Rocky Special Stuff
Source1220:     Rocky-Media.repo
Source1221:     Rocky-Debuginfo.repo
Source1222:     Rocky-Sources.repo
Source1223:     Rocky-Devel.repo
Source1226:     Rocky-Plus.repo
Source1300:     weka.1.gz

# 1400 is the root
# 1401-1420 are dedicated to the kernel
# 1421-1440 is dedicated to x86_64
# 1441-1460 is dedicated to aarch64
Source1400:     rocky-root-ca.der
Source1401:     rockydup1.x509
Source1402:     rockykpatch1.x509
Source1403:     rockydup1-aarch64.x509
Source1404:     rockykpatch1-aarch64.x509
# x86_64
Source1421:     rocky-fwupd.cer
Source1422:     rocky-grub2.cer
Source1423:     rocky-kernel.cer
Source1424:     rocky-shim.cer
# aarch64
Source1441:     rocky-fwupd-aarch64.cer
Source1442:     rocky-grub2-aarch64.cer
Source1443:     rocky-kernel-aarch64.cer
Source1444:     rocky-shim-aarch64.cer

%description
%{distro_name} release files.

%package     -n weka-repos%{?rltype}
Summary:        %{distro_name} Package Repositories
License:        %{rpm_license}
Provides:       system-repos = %{version}-%{release}
# vince - added new provides
Provides:       rocky-repos(%{major}) = %{full_release_version}
Provides:       weka-repos(%{major}) = %{full_release_version}
Requires:       system-release = %{version}-%{release}
Requires:       rocky-gpg-keys%{?rltype}
Conflicts:      %{name} < 8.0
#Conflicts:      rocky-repos
Obsoletes:      rocky-repos
Obsoletes:	weka-rocky-lts86-repos
Obsoletes:	ciq-lts86-rocky-repos

%description   -n weka-repos%{?rltype}
This package provide repo definitions for WEKA Linux 8.10

%package     -n rocky-gpg-keys%{?rltype}
Summary:        Rocky RPM GPG Keys
Conflicts:      %{name} < 8.0

%description -n rocky-gpg-keys%{?rltype}
This package provides the RPM signature keys for Rocky.

%package     -n rocky-sb-certs%{?rltype}
Summary:        %{distro_name} public secureboot certificates
Group:          System Environment/Base
Provides:       system-sb-certs = %{version}-%{release}

%description -n rocky-sb-certs%{?rltype}
This package contains the %{distro_name} secureboot public certificates.

%prep
%if %{with rllookahead} && %{with rlbeta}
echo "!! WARNING !!"
echo "Both LookAhead and Beta were enabled. This is not supported."
echo "As a result: BUILD FAILED."
exit 1
%endif
echo Good.

%build
echo Good.

%post
# remove the previous directive to exclude kernel updates 
sed -i '/^exclude=/d' /etc/dnf/dnf.conf

%install
# copy license and contributors doc here for %%license and %%doc macros
cp %{SOURCE201} %{SOURCE202} %{SOURCE203} .

################################################################################
# system-release data
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro_name} release %{full_release_version}%{?rlstatement: %{rlstatement}} (%{distro_code})" > %{buildroot}%{_sysconfdir}/weka-release
echo "Derived from Rocky Linux %{full_release_version}" > %{buildroot}%{_sysconfdir}/weka-release-upstream
ln -s weka-release %{buildroot}%{_sysconfdir}/system-release
ln -s weka-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s weka-release %{buildroot}%{_sysconfdir}/centos-release
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE1300} %{buildroot}%{_mandir}/man1/

# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{distro_name}"
VERSION="%{full_release_version} (%{distro_code})"
ID="%{rlosid}"
ID_LIKE="rocky rhel centos fedora"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{major}"
PRETTY_NAME="%{distro_name} %{full_release_version}%{?rlstatement: %{rlstatement}} (%{distro_code})"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:weka:weka:%{major}:GA"
HOME_URL="%{home_url}"
BUG_REPORT_URL="%{bug_url}"
SUPPORT_END="2029-05-31"
ROCKY_SUPPORT_PRODUCT="%{os_bug_name}"
ROCKY_SUPPORT_PRODUCT_VERSION="%{full_release_version}%{?rlstatement:-%{rlstatement}}"
REDHAT_SUPPORT_PRODUCT="%{distro_name}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{full_release_version}%{?rlstatement: %{rlstatement}}"
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:weka:weka:%{major}:GA" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%weka_ver %{major}
%%weka %{major}
%%rocky_ver %{major}
%%rocky %{major}
%%centos_ver %{major}
%%centos %{major}
%%rhel %{major}
%%distcore .el%{major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?distsuffix}%%{?with_bootstrap:%{__bootstrap}}
%%el%{major} 1

%%dist_vendor         %{dist_vendor}
%%dist_name           %{distro}
%%dist_home_url       %{home_url}
%%dist_bug_report_url %{bug_url}
%%dist_debuginfod_url %{debug_url}
EOF

# Data directory
install -d -m 0755 %{buildroot}%{_datadir}/weka-release
ln -s weka-release %{buildroot}%{_datadir}/redhat-release
ln -s weka-release %{buildroot}%{_datadir}/rocky-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/weka-release/

# end system-release data
################################################################################

################################################################################
# systemd section
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE300} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE301} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE302} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE303} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
# systemd section
################################################################################

################################################################################
# start secureboot section
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Backported certs for now
install -m 0644 %{SOURCE1400} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1401} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1402} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1403} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1404} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1421} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1422} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1423} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1424} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1441} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1442} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1443} %{buildroot}%{_datadir}/pki/sb-certs/
install -m 0644 %{SOURCE1444} %{buildroot}%{_datadir}/pki/sb-certs/


# Placeholders
# x86_64
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-x86_64.cer

# aarch64
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel-aarch64.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2-aarch64.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd-aarch64.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim-aarch64.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-aarch64.cer

# ppc64le
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-ppc64le.cer

# armhfp
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-root-ca.der %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-kernel.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-grub2.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-fwupd.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-armhfp.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/rocky-shim.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-shim-armhfp.cer

# symlinks for everybody
for x in $(ls %{buildroot}%{_datadir}/pki/sb-certs); do
  ln -sr %{buildroot}%{_datadir}/pki/sb-certs/${x} %{buildroot}%{_sysconfdir}/pki/sb-certs/${x}
done

# end secureboot section
################################################################################

################################################################################
# dnf repo section
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE1200} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1201} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1202} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1203} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1204} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1205} %{buildroot}%{_sysconfdir}/yum.repos.d/

install -p -m 0644 %{SOURCE1210} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1211} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1212} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1213} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1220} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1221} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1222} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1223} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1226} %{buildroot}%{_sysconfdir}/yum.repos.d/

# dnf stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "%{contentdir}" > %{buildroot}%{_sysconfdir}/dnf/vars/contentdir
echo "%{sigcontent}" > %{buildroot}%{_sysconfdir}/dnf/vars/sigcontentdir
echo "%{?rltype}" > %{buildroot}%{_sysconfdir}/dnf/vars/rltype
echo "%{major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# Copy out GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
install -p -m 0644 %{SOURCE102} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

# symlink 8 key
ln -sr %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial \
  %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-Rocky-8

ln -sr %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rockytesting \
  %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-Rocky-8-Testing
# end dnf repo section
################################################################################

%files
%license LICENSE
%doc Contributors COMMUNITY-CHARTER
%{_sysconfdir}/redhat-release
%{_sysconfdir}/centos-release
%{_sysconfdir}/system-release
%{_sysconfdir}/weka-release
%{_sysconfdir}/weka-release
%{_sysconfdir}/weka-release-upstream
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%{_rpmmacrodir}/macros.dist
%{_datadir}/redhat-release
%{_datadir}/weka-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_mandir}/man1/weka.1.gz

%files -n weka-repos%{?rltype}
%license LICENSE
# vince - not sure we want noreplace on these..
%config(noreplace) %{_sysconfdir}/yum.repos.d/*

%config(noreplace) %{_sysconfdir}/dnf/vars/contentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/sigcontentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/rltype
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n rocky-gpg-keys%{?rltype}
%{_sysconfdir}/pki/rpm-gpg/

%files -n rocky-sb-certs%{?rltype}
# care: resetting symlinks is intended
%dir %{_sysconfdir}/pki/sb-certs
%dir %{_datadir}/pki/sb-certs
%{_sysconfdir}/pki/sb-certs/*
%{_datadir}/pki/sb-certs/*

%changelog
* Wed Sep 4 2024 Vince Fleming <vince@weka.io> - 8.10-50.2
- Weka customizations

* Fri Jun 14 2024 Vince Fleming <vince@weka.io> - 8.10-50.1
- Weka customizations

* Fri Jun 07 2024 Louis Abel <label@rockylinux.org> - 8.10-1.9
- Backport distcore macro from 9 and 10

* Mon May 27 2024 Louis Abel <label@rockylinux.org> - 8.10-1.8
- Backport distcore macro from 9 and 10

* Wed Apr 03 2024 Louis Abel <label@rockylinux.org> - 8.10-1.7
- Update SB certs

* Fri Feb 09 2024 Louis Abel <label@rockylinux.org> - 8.10-1.6
- Symlink rockyofficial and rockytesting keys

* Fri Dec 22 2023 Louis Abel <label@rockylinux.org> - 8.10-1.5
- Fix debuginfo repo names

* Wed Nov 29 2023 Louis Abel <label@rockylinux.org> - 8.10-1.4
- Update contributors

* Sun Nov 19 2023 Louis Abel <label@rockylinux.org> - 8.10-1.3
- Adjust comments in sources repo

* Thu Nov 02 2023 Louis Abel <label@rockylinux.org> - 8.10-1.2
- Add aarch64 secure boot certificates

* Thu Sep 07 2023 Louis Abel <label@rockylinux.org> - 8.10-1.1
- Bump to 8.10 for lookahead development

* Sat Jun 10 2023 Louis Abel <label@rockylinux.org> - 8.9-1.5
- Define the distro macro

* Tue May 16 2023 Louis Abel <label@rockylinux.org> - 8.9-1.4
- Update gz

* Tue Apr 25 2023 Louis Abel <label@rockylinux.org> - 8.9-1.3
- Update secure boot certificates

* Wed Mar 29 2023 Louis Abel <label@rockylinux.org> - 8.9-1.1
- Bump to 8.9 for lookahead development

* Fri Mar 17 2023 Louis Abel <label@rockylinux.org> - 8.8-1.5
- Backport rocky-sb-certs to Rocky Linux 8

* Sun Jan 01 2023 Louis Abel <label@rockylinux.org> - 8.8-1.3
- Move macros to a proper location

* Thu Dec 22 2022 Louis Abel <label@rockylinux.org> - 8.8-1.2
- Add SUPPORT_END to absolute EOL

* Tue Oct 18 2022 Louis Abel <label@rockylinux.org> - 8.8-1.1
- Bump to 8.8 for lookahead development

* Wed Sep 07 2022 Louis Abel <label@rockylinux.org> - 8.7-1.1
- Branch off and make system-release version use X.Y-A.B
  format in attempt to match upstream.
- Add stream dnf var

* Fri May 20 2022 Louis Abel <label@rockylinux.org> - 8.6-3
- Add pub/sig var for dnf

* Tue Mar 29 2022 Louis Abel <label@rockylinux.org> - 8.6-2
- 8.6 prepatory release
- Add REDHAT_SUPPORT_PRODUCT to /etc/os-release

* Mon Feb 14 2022 Louis Abel <label@rockylinux.org> - 8.5-4
- Add bootstrap to macros to match EL9

* Tue Dec 21 2021 Louis Abel <label@rockylinux.org> - 8.5-3
- Add countme=1 to base repositories

* Sat Dec 11 2021 Louis Abel <label@rockylinux.org> - 8.5-2
- Fix CPE to match upstreamed Rocky data

* Tue Oct 05 2021 Louis Abel <label@rockylinux.org> - 8.5-1
- 8.5 prepatory release

* Mon Sep 13 2021 Louis Abel <label@rockylinux.org> - 8.4-35
- Add missing CentOS provides and symlinks
- Add centos macros for some builds to complete successfully without relying
  on random patching

* Thu Sep 09 2021 Louis Abel <label@rockylinux.org> - 8.4-33
- Add centos as an id_like to allow current and future SIGs that rely on CentOS
  to work properly.

* Wed Jul 07 2021 Louis Abel <label@rockylinux.org> - 8.4-32
- Fix URLs for Plus and NFV
- Use a macro for the license across sub packages
- Fix bogus date in changelog

* Mon Jul 05 2021 Louis Abel <label@rockylinux.org> - 8.4-30
- Fix URLs for debuginfo

* Tue Jun 29 2021 Louis Abel <label@rockylinux.org> - 8.4-29
- Fix URLs
- Added debuginfo
- Added NFV (future state)

* Wed Jun 16 2021 Louis Abel <label@rockylinux.org> - 8.4-25
- Fix up outstanding issues

* Sat Jun 05 2021 Louis Abel <label@rockylinux.org> - 8.4-24
- Change all mirrorlist urls to https

* Tue May 25 2021 Louis Abel <label@rockylinux.org> - 8.4-23
- Add a version codename to satisfy vendors
- Change license
- Fix up /etc/os-release and CPE
- Remove unused infra var
- Change base_release_version to major

* Wed May 19 2021 Louis Abel <label@rockylinux.org> - 8.4-16
- Remove annoying /etc/issue banner

* Sat May 08 2021 Louis Abel <label@rockylinux.org> - 8.4-15
- Release for 8.4

* Wed May 05 2021 Louis Abel <label@rockylinux.org> - 8.3-14
- Add RT, Plus, and NFV repo files

* Mon May 03 2021 Louis Abel <label@rockylinux.org> - 8.3-13
- Add minor version to /etc/os-release to resolve issues
  with products that provide the "full version"

* Sat May 01 2021 Louis Abel <label@rockylinux.org> - 8.3-12
- Add resilient storage varient
- Fix vars

* Wed Apr 28 2021 Louis Abel <label@rockylinux.org> - 8.3-11
- Fix repo URL's where needed
- Change contentdir var

* Sun Apr 25 2021 Louis Abel <label@rockylinux.org> - 8.3-9
- Remove and add os-release references

* Sun Apr 18 2021 Louis Abel <label@rockylinux.org> - 8.3-8
- Emphasize that this is not a production ready release
- rpmlint

* Wed Apr 14 2021 Louis Abel <label@rockylinux.org> - 8.3-7
- Fix mantis links

* Thu Apr 08 2021 Louis Abel <label@rockylinux.org> - 8.3-5
- Combine release, repos, and keys together to simplify

* Mon Feb 01 2021 Louis Abel <label@rockylinux.org> - 8.3-4
- Initial Rocky Release 8.3 based on CentOS 8.3
- Keep centos rpm macro to reduce package modification burden
- Update /etc/issue
