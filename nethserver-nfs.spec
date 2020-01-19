Summary: nethserver - configure nfs server
%define name nethserver-nfs
Name: %{name}
%define version 1.0.0
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
# Build Source1 by executing prep-sources
Source1: %{name}-ui.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-samba
Requires: nfs-utils
Requires: nfs4-acl-tools
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure nfs server



%prep
%setup

%build
%{makedocs}
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
  --file /usr/libexec/nethserver/getentGroupNfs 'attr(0755,root,root)' \
> %{name}-%{version}-%{release}-filelist

%post
#enable
systemctl enable rpcbind
systemctl enable nfs-server
systemctl enable rpc-statd

#start
systemctl start rpcbind
systemctl start nfs-server
systemctl start rpc-statd

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING

%changelog
* Sun Jan 19 2020 stephane de labrusse <stephane@de-labrusse.fr> - 1.0.0
- Cockpit panels

* Fri Oct 12 2018 stephane de labrusse <stephane@de-labrusse.fr> - 0.1.4
- Subscribe to the nethserver-sssd-save event

* Sat Nov 11 2017 stephane de Labrusse <stephdl@de-labrusse.fr> - 0.1.3
- return the bad IP in the nethgui message error
 
* Mon Jun 5 2017 stephane de Labrusse <stephdl@de-labrusse.fr> - 0.1.2
- test if isAd is valid before to display specific AD settings

* Sat Apr 1 2017 stephane de Labrusse <stephdl@de-labrusse.fr> - 0.1.0
- nfs service renamed to nfs-server
- nfs-lock service renamed to rpc-statd

* Sat Mar 04 2017 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial