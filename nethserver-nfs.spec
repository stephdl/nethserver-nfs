Summary: nethserver - configure nfs server
%define name nethserver-nfs
Name: %{name}
%define version 0.0.1
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-samba
Requires: nethserver-ibays
Requires: nfs-utils
Requires: nfs4-acl-tools
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure nfs server

%changelog

* Mon Apr 03 2017 stephane de Labrusse <stephdl@de-labrusse.fr> - 0.0.1.ns6
- initial release for ns6

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
chkconfig rpcbind on
chkconfig nfs     on
chkconfig nfslock on

#start
service rpcbind start
service nfs     start
service nfslock start

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING
