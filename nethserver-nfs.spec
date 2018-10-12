Summary: nethserver - configure nfs server
%define name nethserver-nfs
Name: %{name}
%define version 0.1.4
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-samba
Requires: nfs-utils
Requires: nfs4-acl-tools
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure nfs server

%changelog
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

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
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
