%{?_javapackages_macros:%_javapackages_macros}
%bcond_without itext
%bcond_without markdown

Name:           maven-doxia
Version:        1.6
Release:        1.3
Epoch:          0
Summary:        Content generation framework
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/doxia/

Source0:        http://repo2.maven.org/maven2/org/apache/maven/doxia/doxia/%{version}/doxia-%{version}-source-release.zip

# Class used only by dependent packages that was moved to doxia-sitetools in
# previous release. But doxia-sitetools doesn't have 1.5 release so putting it
# back otherwise it would break all doxia dependent packages.
# Please remove it as soon as new doxia-sitetools containing this class is
# released
Source1:        RenderingContext.java


# Build against iText 2.x
# http://jira.codehaus.org/browse/DOXIA-53
Patch2:         0004-Fix-itext-dependency.patch

# Forwarded upstream: DOXIA-504
Patch3:         0001-Update-to-Plexus-Container-1.5.5.patch

# Forwarded upstream: DOXIA-505
Patch4:         0001-Update-to-Commons-Collections-1.10.patch

# Don't run bad tests which rely on ordering in set (they fail with Java 8)
Patch5:         0001-Disable-tests-which-rely-on-ordering-in-set.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-configuration:commons-configuration)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
#BuildRequires:  mvn(org.apache.maven.doxia:doxia-core::tests:)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-logging-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-apt)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-modules:pom:)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-module-xhtml)
BuildRequires:  mvn(org.apache.maven.doxia:doxia:pom:)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-test-docs)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.xmlgraphics:fop)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(xerces:xercesImpl)
BuildRequires:  mvn(xmlunit:xmlunit)
BuildRequires:	mvn(org.bouncycastle:bcmail-jdk16)

%if %{with itext}
BuildRequires:  mvn(com.lowagie:itext)
%endif
%if %{with markdown}
BuildRequires:  mvn(org.pegdown:pegdown)
%endif

Obsoletes:      maven-doxia-book < %{epoch}:%{version}-%{release}
Obsoletes:      maven-doxia-maven-plugin < %{epoch}:%{version}-%{release}


%description
Doxia is a content generation framework which aims to provide its
users with powerful techniques for generating static and dynamic
content. Doxia can be used to generate static sites in addition to
being incorporated into dynamic content generation systems like blogs,
wikis and content management systems.


%package core
Summary: Core module for %{name}

%description core
This package provides %{summary}.

%package logging-api
Summary: Logging-api module for %{name}

%description logging-api
This package provides %{summary}.

%package module-apt
Summary: APT module for %{name}

%description module-apt
This package provides %{summary}.

%package module-confluence
Summary: Confluence module for %{name}

%description module-confluence
This package provides %{summary}.

%package module-docbook-simple
Summary: Simplified DocBook module for %{name}

%description module-docbook-simple
This package provides %{summary}.

%package module-fml
Summary: FML module for %{name}

%description module-fml
This package provides %{summary}.

%package module-fo
Summary: FO module for %{name}

%description module-fo
This package provides %{summary}.

%if %{with itext}
%package module-itext
Summary: iText module for %{name}

%description module-itext
This package provides %{summary}.
%endif

%if %{with markdown}
%package module-markdown
Summary: Markdown module for %{name}

%description module-markdown
This package provides %{summary}.
%endif

%package module-latex
Summary: Latex module for %{name}

%description module-latex
This package provides %{summary}.

%package module-rtf
Summary: RTF module for %{name}

%description module-rtf
This package provides %{summary}.

%package modules
Summary: Doxia modules for several markup languages

%description modules
This package provides %{summary}.

%package module-twiki
Summary: TWiki module for %{name}

%description module-twiki
This package provides %{summary}.

%package module-xdoc
Summary: XDoc module for %{name}

%description module-xdoc
This package provides %{summary}.

%package module-xhtml
Summary: XHTML module for %{name}

%description module-xhtml
This package provides %{summary}.

%package sink-api
Summary: Sink-api module for %{name}

%description sink-api
This package provides %{summary}.

%package tests
Summary: Tests for %{name}

%description tests
This package provides %{summary}.

%package test-docs
Summary: Test-docs module for %{name}

%description test-docs
This package provides %{summary}.

%package javadoc
Summary: Javadoc for %{name}
Group:   Documentation

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n doxia-%{version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

mkdir doxia-core/src/main/java/org/apache/maven/doxia/sink/render
cp -p %SOURCE1 doxia-core/src/main/java/org/apache/maven/doxia/sink/render/

# we don't have clirr-maven-plugin
%pom_remove_plugin org.codehaus.mojo:clirr-maven-plugin pom.xml

# use java 5 generics in modello plugin
%pom_xpath_inject "pom:plugin[pom:artifactId[text()='modello-maven-plugin']]"\
"/pom:executions/pom:execution/pom:configuration" \
"<useJava5>true</useJava5>" doxia-modules/doxia-module-fml/pom.xml

%mvn_package :::tests: tests

%if %{without itext}
%pom_disable_module doxia-module-itext doxia-modules
%endif
%if %{without markdown}
%pom_disable_module doxia-module-markdown doxia-modules
%endif

%build
%mvn_build -s

%install
%mvn_install


%files -f .mfiles-doxia
%dir %{_javadir}/%{name}
%doc LICENSE NOTICE
%files core -f .mfiles-doxia-core
%files logging-api -f .mfiles-doxia-logging-api
%doc LICENSE NOTICE
%files module-apt -f .mfiles-doxia-module-apt
%files module-confluence -f .mfiles-doxia-module-confluence
%files module-docbook-simple -f .mfiles-doxia-module-docbook-simple
%files module-fml -f .mfiles-doxia-module-fml
%files module-fo -f .mfiles-doxia-module-fo
%if %{with itext}
%files module-itext -f .mfiles-doxia-module-itext
%endif
%if %{with markdown}
%files module-markdown -f .mfiles-doxia-module-markdown
%endif
%files module-latex -f .mfiles-doxia-module-latex
%files module-rtf -f .mfiles-doxia-module-rtf
%files modules -f .mfiles-doxia-modules
%files module-twiki -f .mfiles-doxia-module-twiki
%files module-xdoc -f .mfiles-doxia-module-xdoc
%files module-xhtml -f .mfiles-doxia-module-xhtml
%files sink-api -f .mfiles-doxia-sink-api
%files test-docs -f .mfiles-doxia-test-docs
%files tests -f .mfiles-tests
%doc LICENSE NOTICE
%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Thu Jul 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6-1
- Update to upstream version 1.6

* Wed Jun 11 2014 Michael Simacek <msimacek@redhat.com> - 0:1.5-7
- Change BR classworlds to plexus-classworlds

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-5
- Build-require pegdown >= 1.4.2-2

* Wed Mar 26 2014 Michal Srb <msrb@redhat.com> - 0:1.5-4
- Disable bad tests which rely on ordering in set

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.5-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-2
- Fix unowned directory

* Tue Dec 10 2013 Michael Simacek <msimacek@redhat.com> - 0:1.5-1
- Update to upstream version 1.5
- Move back RenderingContext.java that was moved to doxia-sitetools which
  doesn't have a release yet

* Thu Dec  5 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-6
- BuildRequire plexus-containers-container-default 1.5.5-14
- Resolves: rhbz#1036584

* Mon Nov 25 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-5
- Rebuild after itext versioned jar fixed

* Thu Nov  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-4
- Port to Commons Collections 1.10

* Wed Nov  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-3
- Enable tests

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Michal Srb <msrb@redhat.com> - 0:1.4-1
- Update to upstream version 1.4
- Enable markdown module
- Remove unneeded patch

* Tue Apr 23 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.3-3
- Remove ant-nodeps BuildRequires

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-2
- Conditionally disable itext module

* Tue Mar 19 2013 Michal Srb <msrb@redhat.com> - 0:1.3-1
- Update to upstream version 1.3
- Remove temporary dependencies on subpackages

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-9
- Remove runtime requirement on POM: httpcomponents-project

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.2-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Dec 20 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-8
- Add httpcomponents-project to doxia-core requires

* Thu Dec 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-7
- Temporarly require all subpackages in the main package

* Wed Dec 19 2012 Michal Srb <msrb@redhat.com>
- Splitted into multiple subpackages (Resolves: #888710)

* Mon Dec 10 2012 Michal Srb <msrb@redhat.com> - 0:1.2-5
- Migrated to plexus-components-component-default (Resolves: #878553)
- Removed custom depmap and its occurrence in spec file
- Fixed various rpmlint warnings

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-3
- Remove plexus-xmlrpc from BR
- Update patches to work without plexus-maven-plugin

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-2
- Add forgotten missing requires

* Fri May  6 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-1
- Update to latest upstream (1.2)
- Use maven 3 to build
- Remove version limits on BR/R (not valid anymore anyway)
- Remove "assert" patch (no explanation for it's existence)

* Tue Feb 22 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.4-3
- Change oro to jakarta-oro in BR/R

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.4-1
- Update to 1.1.4
- Migrate from tomca5 to tomca6
- Versionless jars and javadocs
- Remove old skip-plugin patch
- Replace add-default-role-hint patch with remove-plexus-component patch
- Rename few jakarta BRs/Rs to apache names

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.3-1
- New bugfix version
- Fix javadoc generation error
- Use %%{_mavenpomdir} macro
- Update BRs to latest maven plugin names
- Use new plexus-containers components
- Remove/update old patches

* Tue May 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.2-3
- Update for transitional maven state.
- Install doxia-modules pom.

* Wed May  5 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-2
- Add BuildRequirement on fop

* Fri Feb 12 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.1.2-1
- Update to 1.1.2
- Add update_maven_depmap to post and postun
- Temporarily disable javadoc until maven2-plugin-javadoc is rebuilt against
  the new doxia

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.4
- BR maven2-plugin-plugin.

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.3
- BR maven2-plugin-assembly.

* Mon Dec 21 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.8.a10.2
- BR maven-surefire-provider-junit.

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.8.a10.1
- Add tomcat5 BR

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.8.a10
- Add tomcat5-servlet-2.4-api BR

* Tue Sep 01 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.7.a10
- Fix plexus-cli BR version

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.6.a10
- Add itext and plexus-cli BRs

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.5.a10
- Update to 1.0 alpha 10 courtesy of Deepak Bhole
- Remove gcj support
- Add patch to build against iText 2.x (with back-ported XML classes)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.4.a7.2.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a7.2.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2.10
- Fix broken release tag

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2.9
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7.2.8
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-0.2.a7.2jpp.7
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.2.a7.2jpp.6
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a7.3jpp.5
- Build with maven
- ExcludeArch ppc64

* Sat Sep 01 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.4
- Rebuild without maven (fpr initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.3
- Added switch to ignore failures for the time being

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.0-0.1.a7.3jpp.2
- Build with maven

* Tue Feb 27 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a7.3jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed %%post and %%postun sections for javadoc.
- Fixed instructios on how to generate source drop.
- Fixed %%Summary.
- Added gcj support option.
- Marked configuration file as %%config(noreplace) in %%files section.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a7.3jpp
- Update for maven2 9jpp

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a7.2jpp
- Fix versions in the depmap

* Wed Mar 15 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a7.1jpp
- Initial build
