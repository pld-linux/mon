Summary:	A general-purpose resource monitoring system
Summary(es):	VerificaciСn de recursos
Summary(pl):	System monitorowania zasobСw ogСlnego przeznaczenia
Summary(pt_BR):	MonitoraГЦo de recursos
Summary(ru):	"mon" - инструмент для мониторинга доступности сервисов
Name:		mon
Version:	0.99.2
Release:	4
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/software/admin/mon/%{name}-%{version}.tar.bz2
# Source0-md5:	61dbaed4ab89e952650339a55dd9f1dc
Source1:	%{name}-%{name}.cf
Source2:	%{name}-%{name}.cgi
Source3:	%{name}.init
Source4:	%{name}.sysconfig
URL:		http://www.kernel.org/software/mon/
BuildRequires:	ed
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-Mon
Requires:	perl-Time-Period
Requires:	perl-TimeDate
Requires:	perl-Time-HiRes
Requires:	perl-Convert-BER
Requires:	perl-Net-Telnet
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

%description -l es
VerificaciСn de recursos.

%description -l pl
mon jest systemem monitorowania zasobСw ogСlnego przeznaczenia. Mo©e
byФ u©ywany do monitorowania dostЙpno╤ci sieci, problemСw z serwerem,
warunkСw ╤rodowiska (np. temperatury) i innych. Mo©e byФ u©ywany do
sprawdzania warunkСw i/lub uruchamiania jakiej╤ akcji po wykryciu
awarii. Akcje te s╠ podejmowane przez uruchamianie oddzielnych
programСw.

mon jest rozszerzalny. Monitory i alarmy nie s╠ czЙ╤ci╠ mona, ale
dystrybucja zawiera pewien ich zestaw na pocz╠tek. To znaczy, ©e
je©eli nowa usЁuga potrzebuje monitorowania lub potrzebny jest nowy
alarm, serwer mon nie musi byФ zmieniany.

%description -l pt_BR
Mon И um sistema de propСsito geral para monitoraГЦo de recursos, o
qual pode ser usado para monitorar a disponibilidade de serviГos de
uma rede, problemas em servidores, condiГУes ambientais, etc

A monitoraГЦo de recursos pode ser vista como duas tarefas separadas:
o teste de uma condiГЦo e a aГЦo a ser tomada em caso de falha. O mon
foi projetado para fazer estas duas duas tarefas separadas usando
programas independentes, e foi implementado como um escalonador que
executa os monitores (que testam uma condiГЦo), e chama os alertas
apropriados se o monitor falhar.

Monitores e alertas nЦo fazem parte do mon, apesar de que uma sИrie
deles vem neste pacote, sendo Зteis para comeГar a usА-lo. Isto
significa que se um novo serviГo necessita de monitoraГЦo, ou se um
novo alerta И requerido, o servidor mon nЦo precisa ser alterado. Isto
faz o mon ser facilmente estendido.

%description -l ru
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
%setup -q

%build
# change hardcoded paths in scripts, etc.
for i in mon doc/mon.8 mon.d/{file_change,http_t*,traceroute,up_rtt}.monitor clients/skymon/skymon clients/monshow ; do
ed $i <<EOF
,s:/usr/local/:/usr/:g
wq
EOF
done

RPM_OPT_FLAGS="%{rpmcflags} -DUSE_VENDOR_CF_PATH=1"; export RPM_OPT_FLAGS

%{__make} all -C mon.d

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
install alert.d/* 	$RPM_BUILD_ROOT%{_libdir}/mon/alert.d
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
%doc [A-Z]* doc/[A-Z]* skymon.tar.gz etc.tar.gz
%dir %{_sysconfdir}/mon
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mon/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/mon
%attr(754,root,root) /etc/rc.d/init.d/mon
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mon
%dir %{_libdir}/mon/*.d
%attr(755,root,root) %{_libdir}/mon/*.d/*
%dir /var/lib/mon
%dir /var/lib/mon/state.d
%dir /var/lib/mon/log.d
%{_mandir}/man?/*
