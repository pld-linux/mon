Summary:	A general-purpose resource monitoring system.
Name:		mon 
Version:	0.99.2
Release:	1 
Source0:	ftp://ftp.kernel.org/pub/software/admin/mon/%{name}-%{version}.tar.bz2
Source1:	%{name}-%{name}.cf
Source2:	%{name}-%{name}.cgi
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Url:		http://www.kernel.org/software/mon/
License:	GPL
Group:		Applications/System	
Requires:	perl-Mon                  
Requires:	perl-Time-Period	
Requires:	perl-TimeDate           
Requires:	perl-Time-HiRes        
Requires:	perl-Convert-BER      
Requires:	perl-Net-Telnet       
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mon is a general-purpose resource monitoring system. It can be used to
monitor network service availability, server problems, environmental
conditions (i.e., the temperature in a room) or other things. Mon can
be used to test the condition and/or to trigger an action upon failure
of the condition. Mon keeps the testing and action-taking tasks as
separate, stand-alone programs.

Mon is very extensible. Monitors and alerts are not a part of mon, but
the distribution comes with a handful of them to get you started. This
means that if a new service needs monitoring, or if a new alert is
required, the mon server will not need to be changed.

%prep
%setup0 -q 

%build
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1"

%{__make} all -C mon.d

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name},rc.d/init.d,sysconfig,mon}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/{man1,man8},%{_libdir}/mon/{alert.d,mon.d}}
install -d $RPM_BUILD_ROOT/var/lib/mon/{state.d,log.d}

install mon 		$RPM_BUILD_ROOT%{_bindir}
install clients/moncmd 	$RPM_BUILD_ROOT%{_bindir}
install clients/monshow $RPM_BUILD_ROOT%{_bindir}
install clients/skymon/skymon $RPM_BUILD_ROOT%{_bindir}
install doc/*.1 	$RPM_BUILD_ROOT%{_mandir}/man1 
install doc/*.8 	$RPM_BUILD_ROOT%{_mandir}/man8 
install alert.d/* 	$RPM_BUILD_ROOT%{_libdir}/mon/alert.d
install mon.d/*.monitor	$RPM_BUILD_ROOT%{_libdir}/mon/mon.d
install etc/auth.cf 	$RPM_BUILD_ROOT%{_sysconfdir}/mon/auth.cf
touch 			$RPM_BUILD_ROOT%{_sysconfdir}/mon/userfile

#install -d $RPM_BUILD_ROOT/var/www/cgi-bin/
#install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/var/www/cgi-bin/

install %{SOURCE1} 	$RPM_BUILD_ROOT%{_sysconfdir}/mon/mon.cf
install %{SOURCE3} 	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE4} 	$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

gzip -9nf [A-Z]* doc/[A-Z]* mon.lsm
tar czf skymon.tar.gz clients/skymon
tar czf etc.tar.gz etc/[a-z]*

%clean
rm -rf $RPM_BUILD_ROOT

%post

/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/mon ]; then
        /etc/rc.d/init.d/mon reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/mon start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/mon ]; then
                /etc/rc.d/init.d/mon stop >&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mon/* 
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/mon
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/mon
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/mon/*/*
%dir /var/lib/mon/state.d
%dir /var/lib/mon/log.d
%{_mandir}/man?/*
