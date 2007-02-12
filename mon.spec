%include	/usr/lib/rpm/macros.perl
%define	_rc	pre1
Summary:	A general-purpose resource monitoring system
Summary(es.UTF-8):   Verificación de recursos
Summary(pl.UTF-8):   System monitorowania zasobów ogólnego przeznaczenia
Summary(pt_BR.UTF-8):   Monitoração de recursos
Summary(ru.UTF-8):   "mon" - инструмент для мониторинга доступности сервисов
Name:		mon
Version:	1.1.0
Release:	0.%{_rc}.5
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/software/admin/mon/devel/%{name}-%{version}%{_rc}.tar.bz2
# Source0-md5:	cec4079e8bcb8461e6c876c89cf2a01f
Source1:	%{name}-%{name}.cf
Source2:	%{name}-%{name}.cgi
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}-jabber.alert
Source6:	%{name}-clamd.monitor
Source7:	%{name}-spamd.monitor
Patch0:		%{name}-ftp.patch
Patch1:		%{name}-msql-mysql-timeout.patch
URL:		http://www.kernel.org/software/mon/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l es.UTF-8
Verificación de recursos.

%description -l pl.UTF-8
mon jest systemem monitorowania zasobów ogólnego przeznaczenia. Może
być używany do monitorowania dostępności sieci, problemów z serwerem,
warunków środowiska (np. temperatury) i innych. Może być używany do
sprawdzania warunków i/lub uruchamiania jakiejś akcji po wykryciu
awarii. Akcje te są podejmowane przez uruchamianie oddzielnych
programów.

mon jest rozszerzalny. Monitory i alarmy nie są częścią mona, ale
dystrybucja zawiera pewien ich zestaw na początek. To znaczy, że
jeżeli nowa usługa potrzebuje monitorowania lub potrzebny jest nowy
alarm, serwer mon nie musi być zmieniany.

%description -l pt_BR.UTF-8
Mon é um sistema de propósito geral para monitoração de recursos, o
qual pode ser usado para monitorar a disponibilidade de serviços de
uma rede, problemas em servidores, condições ambientais, etc

A monitoração de recursos pode ser vista como duas tarefas separadas:
o teste de uma condição e a ação a ser tomada em caso de falha. O mon
foi projetado para fazer estas duas duas tarefas separadas usando
programas independentes, e foi implementado como um escalonador que
executa os monitores (que testam uma condição), e chama os alertas
apropriados se o monitor falhar.

Monitores e alertas não fazem parte do mon, apesar de que uma série
deles vem neste pacote, sendo úteis para começar a usá-lo. Isto
significa que se um novo serviço necessita de monitoração, ou se um
novo alerta é requerido, o servidor mon não precisa ser alterado. Isto
faz o mon ser facilmente estendido.

%description -l ru.UTF-8
"mon" - инструмент для мониторинга доступности сервисов. Сервисы могут
быть сетевыми, состоянием окружения, или чем угодно похожим, что можно
протестировать программно. Он чрезвычайно полезен для системных
администраторов, но не ограничивается использованием только ими. Он
разработан как основная система оповещения об авариях, разделяя задачи
тестирования сервисов на доступность и отправку тревожных сообщений,
когда что-то не работает. Для достижения этого "mon" реализован как
диспетчер, который запускает программы, которые выполняют
тестирование, и запускает программы предупреждения, когда скрипты
обнаруживают сбои. Ни один из сервисов не обрабатывается собственно
"mon"'ом. Эти функции обрабатываются соответствующими программами.

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p1
%patch1 -p1

find -name CVS -type d | xargs rm -rf

%build
# change hardcoded paths in scripts, etc.
for i in mon doc/mon.8 mon.d/{file_change,http_t*,traceroute,up_rtt}.monitor clients/skymon/skymon clients/monshow ; do
	sed -i -e 's#/usr/local/#%{_prefix}/#g' $i
done

RPM_OPT_FLAGS="%{rpmcflags} -DUSE_VENDOR_CF_PATH=1"; export RPM_OPT_FLAGS

%{__make} all \
	-C mon.d \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/{rc.d/init.d,sysconfig,mon}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,8},%{_libdir}/mon/{alert.d,mon.d}} \
	$RPM_BUILD_ROOT/var/lib/mon/{state.d,log.d}

install mon 		$RPM_BUILD_ROOT%{_bindir}
install clients/moncmd 	$RPM_BUILD_ROOT%{_bindir}
install clients/monshow $RPM_BUILD_ROOT%{_bindir}
install clients/skymon/skymon $RPM_BUILD_ROOT%{_bindir}
install doc/*.1 	$RPM_BUILD_ROOT%{_mandir}/man1
install doc/*.8 	$RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE5}	$RPM_BUILD_ROOT%{_libdir}/mon/alert.d/jabber.alert
install alert.d/* 	$RPM_BUILD_ROOT%{_libdir}/mon/alert.d
install %{SOURCE6}	$RPM_BUILD_ROOT%{_libdir}/mon/mon.d/clamd.monitor
install %{SOURCE7}      $RPM_BUILD_ROOT%{_libdir}/mon/mon.d/spamd.monitor
install mon.d/*.monitor	$RPM_BUILD_ROOT%{_libdir}/mon/mon.d
install etc/auth.cf 	$RPM_BUILD_ROOT%{_sysconfdir}/mon/auth.cf
touch 			$RPM_BUILD_ROOT%{_sysconfdir}/mon/userfile

#install -d $RPM_BUILD_ROOT/var/www/cgi-bin/
#install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/var/www/cgi-bin/

install %{SOURCE1} 	$RPM_BUILD_ROOT%{_sysconfdir}/mon/mon.cf
install %{SOURCE3} 	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE4} 	$RPM_BUILD_ROOT/etc/sysconfig/%{name}

tar czf skymon.tar.gz clients/skymon
tar czf etc.tar.gz etc/[a-z]*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service mon restart

%preun
if [ "$1" = "0" ]; then
	%service mon stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc [A-Z]* doc/[A-Z]* skymon.tar.gz etc.tar.gz
%dir %{_sysconfdir}/mon
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mon/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mon
%attr(754,root,root) /etc/rc.d/init.d/mon
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mon
%dir %{_libdir}/mon/*.d
%attr(755,root,root) %{_libdir}/mon/*.d/*
%dir /var/lib/mon
%dir /var/lib/mon/state.d
%dir /var/lib/mon/log.d
%{_mandir}/man?/*
