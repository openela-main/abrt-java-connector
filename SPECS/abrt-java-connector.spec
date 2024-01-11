%global commit 230b72697c7c43db747b2644b17cb2685d1539de
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		abrt-java-connector
Version:	1.1.0
Release:	16%{?dist}
Summary:	JNI Agent library converting Java exceptions to ABRT problems

Group:		System Environment/Libraries
License:	GPLv2+
URL:		https://github.com/jfilak/abrt-java-connector
Source0:	https://github.com/jfilak/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:	cmake
BuildRequires:	satyr-devel
BuildRequires:	libreport-devel >= 2.4.0
BuildRequires:	abrt-devel
BuildRequires:	java-devel
BuildRequires:	systemd-devel
BuildRequires:	gettext
BuildRequires:	check-devel
BuildRequires:	rpm-devel
BuildRequires:	git

Requires:	abrt

# git format-patch 416db946329b043a58acf557f0525361a97e1da1 -N
Patch0001: 0001-Decrease-the-tested-memory-limits-because-of-failure.patch
Patch0002: 0002-Adapt-the-arm-test-outputs-to-java-1.8.patch
Patch0003: 0003-Add-java-1.8-test-outputs-for-aarch-ppc-and-s390.patch
Patch0004: 0004-Update-Linux-aarch64-test-outputs.patch
Patch0005: 0005-Update-the-test-results.patch
Patch0006: 0006-Make-the-dependency-on-systemd-optional.patch
Patch0007: 0007-Update-README.patch
Patch0008: 0008-Remove-function-malloc_readlink.patch
Patch0009: 0009-Makefile-Adds-srpm-target.patch
Patch0010: 0010-Update-the-test-results.patch
Patch0011: 0011-Clearly-state-that-tests-cannot-be-run-under-root.patch
Patch0012: 0012-Disable-ClassNotFoundException-test-again.patch
Patch0013: 0013-Correct-includes-for-ABRT.patch
Patch0014: 0014-Drop-pedantic-from-CFLAGS.patch
Patch0015: 0015-Rename-log-to-log_warning.patch
Patch0016: 0016-Update-the-test-results.patch
Patch0017: 0017-build-update-pkg-modules-for-systemd.patch
Patch0018: 0018-abrt-checker-Fix-preprocessor-check.patch

%description
JNI library providing an agent capable to process both caught and uncaught
exceptions and transform them to ABRT problems


%prep
# http://www.rpm.org/wiki/PackagerDocs/Autosetup
# Default '__scm_apply_git' is 'git apply && git commit' but this workflow
# doesn't allow us to create a new file within a patch, so we have to use
# 'git am' (see /usr/lib/rpm/macros for more details)
%define __scm_apply_git(qp:m:) %{__git} am
%autosetup -n %{name}-%{commit} -S git


%build
%cmake -DCMAKE_BUILD_TYPE=Release
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%files
%doc LICENSE README AUTHORS
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_java.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_java.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/java_event.conf
%config(noreplace) %{_sysconfdir}/abrt/plugins/java.conf
%{_bindir}/abrt-action-analyze-java
%{_mandir}/man1/abrt-action-analyze-java.1*
%{_mandir}/man5/java_event.conf.5*
%{_mandir}/man5/bugzilla_format_java.conf.5*
%{_mandir}/man5/bugzilla_formatdup_java.conf.5*
%{_datadir}/abrt/conf.d/plugins/java.conf

# Applications may use a single subdirectory under/usr/lib.
# http://www.pathname.com/fhs/pub/fhs-2.3.html#PURPOSE22
#
# Java does not support multilib.
# https://fedorahosted.org/fesco/ticket/961
%{_prefix}/lib/abrt-java-connector


%check
make test || {
    cat Testing/Temporary/LastTest.log
    exit 1
}


%changelog
* Fri Jul 19 2019 Ernestas Kulik <ekulik@redhat.com> - 1.1.0-16
- Add patch for #1721393
- Add patch for https://github.com/abrt/abrt-java-connector/commit/ae2144f1674f163517f0aa18b5f1b4784c143572

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Matej Habrnal <mhabrnal@redhat.com> - 1.1.0-14
- turn on unit testing and fix test outputs

* Mon Aug 28 2017 Matej Habrnal <mhabrnal@redhat.com> - 1.1.0-13
- Rename log() to log_warning()
- Update the test results
- Resolves: #1484585

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.0-12
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 15 2016 Jakub Filak <jfilak@redhat.com> - 1.1.0-8
- Drop '-pedantic' from CFLAGS
- Correct includes for ABRT
- Resolves: #1307305

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Jakub Filak <jfilak@redhat.com> - 1.1.0-6
- Rebuilt for new rpmlib : https://lists.fedoraproject.org/pipermail/devel/2015-July/212672.html

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Matej Habrnal <mhabrnal@redhat.com> - 1.1.0-4
- Make the dependency on systemd optional
- Update the test results
- Resolves: #1185626

* Tue Nov 04 2014 Jakub Filak <jfilak@redhat.com> - 1.1.0-3
- Update the test results for armv7l

* Tue Nov 04 2014 Jakub Filak <jfilak@redhat.com> - 1.1.0-2
- Update the test results for aarch64

* Wed Oct 29 2014 Jakub Filak <jfilak@redhat.com> - 1.1.0-1
- Support java-1.8-openjdk
- Install the library to /usr/lib/abrt-java-connector on all arches

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Jakub Filak <jfilak@redhat.com> - 1.0.10-2
- Add test results for Linux-ppc64le
- Related: #981682

* Fri Apr 4 2014 Jakub Filak <jfilak@redhat.com> - 1.0.10-1
- Temporarily ignore failures of reporter-ureport until ABRT start using FAF2
- Prevent users from reporting low quality stack traces

* Tue Mar 18 2014 Jakub Filak <jfilak@redhat.com> - 1.0.9-1
- Make the agent configurable via a configuration file
- Include custom debug info in bug reports
- Make the detection of 'executable' working with JAR files

* Tue Feb 04 2014 Jakub Filak <jfilak@redhat.com> - 1.0.8-3
- Return the correct value from Agent_OnLoad
- Add test for multiple calls of Agent_On*

* Tue Feb 04 2014 Jakub Filak <jfilak@redhat.com> - 1.0.8-2
- Make sure that agent_onload and agent_onunload are processed only once
- Fix a pair of defects uncovered by coverity

* Wed Jan 22 2014 Jakub Filak <jfilak@redhat.com> - 1.0.8-1
- Do not report exceptions caught in a native method
- Mark stack traces with 3rd party classes as not-reportable
- Calculate 'duphash' & 'uuid' in satyr
- Use the main class URL for 'executable'
- Do not ship own reporting workflow definitions
- Code optimizations

* Fri Jan 10 2014 Jakub Filak <jfilak@redhat.com> - 1.0.7-1
- Use the last frame class path for executable
- Gracefully handle JVMTI errors
- Add an abstract to README
- Add support for journald and syslog
- Make log output disabled by default
- Add support for changing log directory
- Fix a race condition causing a crash of JVM

* Tue Oct 01 2013 Jakub Filak <jfilak@redhat.com> - 1.0.6-1
- Fix a deadlock in GC start callback
- Disable experimental features in production releases

* Tue Jul 30 2013 Jakub Filak <jfilak@redhat.com> - 1.0.5-1
- Provide a proper configuration for libreport

* Thu Jul 18 2013 Jakub Filak <jfilak@redhat.com> - 1.0.4-1
- Stop creating an empty log file

* Tue Jul 16 2013 Jakub Filak <jfilak@redhat.com> - 1.0.3-1
- Fix tests on arm

* Tue Jul 09 2013 Jakub Filak <jfilak@redhat.com> - 1.0.2-1
- Do not crash on empty command line options

* Mon Jul 08 2013 Jakub Filak <jfilak@redhat.com> - 1.0.1-1
- Fix tests on ppc and s390 on both 32 and 64 bit

* Thu Jun 27 2013 Jakub Filak <jfilak@redhat.com> - 1.0.0-1
- Publicly releasable version

* Mon Jun 03 2013 Jakub Filak <jfilak@redhat.com> - 0.1.2-1
- Start versioning library
- Drop build dependency on abrt-devel

* Mon Jun 03 2013 Jakub Filak <jfilak@redhat.com> - 0.1.1-2
- Provide ABRT configuration

* Mon Jun 03 2013 Jakub Filak <jfilak@redhat.com> - 0.1.1-1
- New release

* Fri May 31 2013 Jakub Filak <jfilak@redhat.com> - 0.1.0-3
- Build with the library name same as the package name

* Fri May 31 2013 Jakub Filak <jfilak@redhat.com> - 0.1.0-2
- Build with ABRT enabled

* Fri May 31 2013 Jakub Filak <jfilak@redhat.com> - 0.1.0-1
- Initial version
