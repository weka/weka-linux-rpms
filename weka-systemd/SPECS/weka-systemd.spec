Name:		weka-systemd
Version:	1.0
Release:	1%{?dist}
Summary:	WEKA Linux Systemd Customizations
BuildArch:	noarch

License:	GPL
URL:		https://weka.io

Requires:	systemd
#Recommends:	avahi
Requires:	coreutils
Requires:	sed

Source101:	weka-firstboot.service
Source102:	weka-everyboot.service
Source103:	weka-avahi-config.service
Source104:	weka-avahi-config.timer

Source201:	weka-firstboot
Source202:	weka-everyboot
Source203:	weka-avahi-config

Source301:	avahi-boilerplate.service


%description
Systemd Customizations to WEKA Rocky Linux 8.10

%build
echo Good

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE102} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE103} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE104} %{buildroot}%{_unitdir}

install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 %{SOURCE201} %{buildroot}%{_bindir}
install -m 0755 %{SOURCE202} %{buildroot}%{_bindir}
install -m 0755 %{SOURCE203} %{buildroot}%{_bindir}

install -d -m 0755 %{buildroot}/etc/avahi
install -m 0644 %{SOURCE301} %{buildroot}/etc/avahi

%pre
# edit the nsswitch.conf so we'll use Avahi for name resolution
cp /etc/nsswitch.conf /etc/nsswitch.conf.last
sed -i '/^hosts:/s/files dns myhostname/files mdns_minimal [NOTFOUND=return] dns myhostname/' /etc/nsswitch.conf

%post
%systemd_post weka-firstboot.service weka-everyboot.service weka-avahi-config.timer

%preun
%systemd_preun weka-firstboot.service weka-everyboot.service weka-avahi-config.timer

%postun
%{?ldconfig}
%systemd_postun_with_restart weka-firstboot.service weka-everyboot.service weka-avahi-config.timer

%files
%{_unitdir}/*
%{_bindir}/*
/etc/avahi/avahi-boilerplate.service


%changelog
* Sat Aug 31 2024 Vince Fleming <vince@weka.io>
-- 
