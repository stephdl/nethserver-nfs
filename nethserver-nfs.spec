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
Requires: nfs-utils
Requires: nfs4-acl-tools
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
configure nfs server

%changelog
* Sat Mar 04 2017 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial

%prep
%setup

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
    > %{name}-%{version}-%{release}-filelist
#echo "%doc COPYING" >> %{name}-%{version}-%{release}-filelist

%post
#enable
/usr/bin/systemctl enable rpcbind
/usr/bin/systemctl enable nfs
/usr/bin/systemctl enable nfs-lock

#start
/usr/bin/systemctl start rpcbind
/usr/bin/systemctl start nfs
/usr/bin/systemctl start nfs-lock

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
