%define name	nvidia-cuda-toolkit
%define version 2.2
%define release %mkrel 1

%define driver_ver 185.18.14

Summary:	NVIDIA CUDA Toolkit libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	cudatoolkit_2.2_linux_32_rhel5.3.run
Source1:	cudatoolkit_2.2_linux_64_rhel5.3.run
Source2:	nvidia
License:	Freeware
Group:		System/Libraries
Url:		http://www.nvidia.com/cuda
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Suggests:	nvidia >= %{driver_ver}

%description
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the libraries and attendant files needed to run
programs that make use of CUDA.

%package devel
Summary:	NVIDIA CUDA Toolkit development files
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Suggests:	nvidia-devel >= %{driver_ver}

%description devel
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the development files needed to build programs
that make use of CUDA.

%package -n nvidia-cuda-profiler
Summary:	NVIDIA CUDA Visual Profiler
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Suggests:	nvidia-devel >= %{driver_ver}

%description -n nvidia-cuda-profiler
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the CUDA Visual Profiler.

%prep
%setup -q -T -c %{name}-%{version}

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_usr}

%ifarch %ix86
bash %SOURCE0 --tar xf -C %{buildroot}%{_usr}
%else
bash %SOURCE1 --tar xf -C %{buildroot}%{_usr}
%__mv %{buildroot}/usr/lib %{buildroot}/usr/lib64
%__sed -ie 's/lib/lib64/g' %{buildroot}%{_bindir}/nvcc.profile
%endif

%__mv %{buildroot}%{_usr}/doc ./
%__install -d -m 755 %{buildroot}%{_datadir}
%__mv %{buildroot}%{_usr}/man %{buildroot}%{_mandir}

%__mv %{buildroot}%{_usr}/cudaprof/bin/cudaprof %{buildroot}%{_bindir}/
%__mkdir cudaprofdoc
%__mv %{buildroot}%{_usr}/cudaprof/*.txt cudaprofdoc/
%__mv %{buildroot}%{_usr}/cudaprof/doc/* cudaprofdoc/
%__mv %{buildroot}%{_usr}/cudaprof/projects cudaprofdoc/
%__rm -rf %{buildroot}%{_usr}/cudaprof

%__install -D -m 755 %SOURCE2 %{buildroot}%{_sysconfdir}/init.d/nvidia

%clean
%__rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%_libdir/*.so.*
%_sysconfdir/init.d/*
%exclude %_usr/src
%exclude %_usr/install-linux.pl

%files devel
%defattr(-,root,root)
%doc doc/*
%_bindir/*
%_libdir/*.so
%_includedir/*
%_mandir/*
%_usr/open64/*
%exclude %_usr/src
%exclude %_usr/install-linux.pl

%files -n nvidia-cuda-profiler
%defattr(-,root,root)
%doc cudaprofdoc/*
%_bindir/cudaprof
