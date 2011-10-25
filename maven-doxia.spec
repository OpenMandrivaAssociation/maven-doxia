# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           maven-doxia
Version:        1.1.4
Release:        2
Summary:        Content generation framework
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/doxia/

# svn export http://svn.apache.org/repos/asf/maven/doxia/doxia/tags/doxia-1.1.4 maven-doxia-1.1.4
# tar czf maven-doxia-1.1.4.tar.gz maven-doxia-1.1.4/
Source0:        %{name}-%{version}.tar.gz

# Point it at the correct plexus-container-default
Source1:        %{name}-depmap.xml


# TODO: push upstream
Patch0:         0001-Use-plexus-component-metadata.patch
# TODO: push upstream
# abstract class should not be annotated as component because maven
# will pick it up and try to instantiate
Patch1:         0002-doxia-core-remove-plexus-component-annotation.patch

Patch2:         0003-remove-clirr.patch
Patch3:         0004-Comment-out-assert.patch
# Build against iText 2.x
# http://jira.codehaus.org/browse/DOXIA-53
Patch4:         0005-Fix-itext-dependency.patch


BuildArch:      noarch

BuildRequires:  java >= 0:1.6.0
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant, ant-nodeps
BuildRequires:  itext >= 2.1.7-4
BuildRequires:  plexus-cli >= 1.2-8
BuildRequires:  maven2 >= 0:2.0.4-9
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-doxia-tools
BuildRequires:  plexus-maven-plugin >= 0:1.2-2
BuildRequires:  modello-maven-plugin >= 0:1.0-0.a8.3
BuildRequires:  plexus-xmlrpc >= 0:1.0-0.b4.3
BuildRequires:  servlet25
BuildRequires:  classworlds
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-validator
BuildRequires:  apache-commons-configuration
BuildRequires:  junit
BuildRequires:  oro
BuildRequires:  plexus-i18n
BuildRequires:  plexus-utils >= 1.5.7
BuildRequires:  plexus-velocity
BuildRequires:  plexus-build-api
BuildRequires:  velocity
BuildRequires:	fop
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  plexus-containers-component-javadoc
BuildRequires:  plexus-containers-container-default
BuildRequires:  httpcomponents-client
BuildRequires:  httpcomponents-project

Requires:       classworlds
Requires:       apache-commons-collections
Requires:       apache-commons-logging
Requires:       apache-commons-validator
Requires:       junit
Requires:       oro
Requires:       plexus-container-default
Requires:       plexus-i18n
Requires:       plexus-utils >= 1.5.7
Requires:       plexus-velocity
Requires:       velocity
Requires:	fop
Requires:       httpcomponents-client
Requires:       httpcomponents-project

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils >= 0:1.7.2
Requires(postun): jpackage-utils >= 0:1.7.2

%description
Doxia is a content generation framework which aims to provide its
users with powerful techniques for generating static and dynamic
content. Doxia can be used to generate static sites in addition to
being incorporated into dynamic content generation systems like blogs,
wikis and content management systems.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

#rm -fr doxia-maven-plugin

# use new plexus-javadoc taglet replacement
sed -i 's:plexus-javadoc:plexus-component-javadoc:' pom.xml


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
	-e \
	-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
	-Dmaven2.jpp.depmap.file=%{SOURCE1} \
	-Dmaven.test.skip=true \
	install javadoc:aggregate

%install
# jars/poms
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for targetdir in `find -type d -name target`; do

    targetdir=`echo $targetdir | sed -e s:^\./::g`

    modulename=`echo $targetdir | awk -F / '{print $(NF-1)}'`
    strippedmodulename=`echo $modulename | sed -e s:^doxia-::g`

    # Does the module have a jar?
    if [ -f $targetdir/$modulename-%{version}.jar ]; then
        cp -p $targetdir/$modulename-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/%{name}/$strippedmodulename.jar
    fi


    # Skip parent pom
    if [ ! -z $strippedmodulename ]; then
        cp -p $targetdir/../pom.xml \
                $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-$strippedmodulename.pom

        %add_to_maven_depmap org.apache.maven.doxia $modulename %{version} JPP/maven-doxia $strippedmodulename
    fi

done

# Install parent pom
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-doxia-doxia.pom
%add_to_maven_depmap org.apache.maven.doxia doxia %{version} JPP/maven-doxia doxia
install -pm 644 doxia-modules/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.maven-doxia-modules.pom
%add_to_maven_depmap org.apache.maven.doxia doxia-modules %{version} JPP/maven-doxia modules
install -d -m 0755 %{buildroot}/%{_datadir}/maven2/lib
ln -s %{_javadir}/maven-doxia/logging-api.jar $RPM_BUILD_ROOT/%{_datadir}/maven2/lib/maven-doxia_logging-api.jar

# javadoc (all javadocs are contained in the main module docs dir used below)
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_datadir}/maven2/lib/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

