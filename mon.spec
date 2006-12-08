%include	/usr/lib/rpm/macros.perl
%define	_rc	pre1
Summary:	A general-purpose resource monitoring system
Summary(es):	Verificaci�n de recursos
Summary(pl):	System monitorowania zasob�w og�lnego przeznaczenia
Summary(pt_BR):	Monitora��o de recursos
Summary(ru):	"mon" - ���������� ��� ����������� ����������� ��������
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

%description -l es
Verificaci�n de recursos.

%description -l pl
mon jest systemem monitorowania zasob�w og�lnego przeznaczenia. Mo�e
by� u�ywany do monitorowania dost�pno�ci sieci, problem�w z serwerem,
warunk�w �rodowiska (np. temperatury) i innych. Mo�e by� u�ywany do
sprawdzania warunk�w i/lub uruchamiania jakiej� akcji po wykryciu
awarii. Akcje te s� podejmowane przez uruchamianie oddzielnych
program�w.

mon jest rozszerzalny. Monitory i alarmy nie s� cz�ci� mona, ale
dystrybucja zawiera pewien ich zestaw na pocz�tek. To znaczy, �e
je�eli nowa us�uga potrzebuje monitorowania lub potrzebny jest nowy
alarm, serwer mon nie musi by� zmieniany.

%description -l pt_BR
Mon � um sistema de prop�sito geral para monitora��o de recursos, o
qual pode ser usado para monitorar a disponibilidade de servi�os de
uma rede, problemas em servidores, condi��es ambientais, etc

A monitora��o de recursos pode ser vista como duas tarefas separadas:
o teste de uma condi��o e a a��o a ser tomada em caso de falha. O mon
foi projetado para fazer estas duas duas tarefas separadas usando
programas independentes, e foi implementado como um escalonador que
executa os monitores (que testam uma condi��o), e chama os alertas
apropriados se o monitor falhar.

Monitores e alertas n�o fazem parte do mon, apesar de que uma s�rie
deles vem neste pacote, sendo �teis para come�ar a us�-lo. Isto
significa que se um novo servi�o necessita de monitora��o, ou se um
novo alerta � requerido, o servidor mon n�o precisa ser alterado. Isto
faz o mon ser facilmente estendido.

%description -l ru
"mon" - ���������� ��� ����������� ����������� ��������. ������� �����
���� ��������, ���������� ���������, ��� ��� ������ �������, ��� �����
�������������� ����������. �� ����������� ������� ��� ���������
���������������, �� �� �������������� �������������� ������ ���. ��
���������� ��� �������� ������� ���������� �� �������, �������� ������
������������ �������� �� ����������� � �������� ��������� ���������,
����� ���-�� �� ��������. ��� ���������� ����� "mon" ���������� ���
���������, ������� ��������� ���������, ������� ���������
������������, � ��������� ��������� ��������������, ����� �������
������������ ����. �� ���� �� �������� �� �������������� ����������
"mon"'��. ��� ������� �������������� ���������������� �����������.

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
