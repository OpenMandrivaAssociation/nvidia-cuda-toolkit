%define name	nvidia-cuda-toolkit
%define version 4.1.28
%define release %mkrel 2

%define driver_ver 285.05

%define noautoreq_regex libcuda.so.*\\|libcudart.so.*\\|devel\(libcuda.*\)\\|devel\(libcudart.*\)\\|python\(abi\)
%if %{_use_internal_dependency_generator}
%define __noautoreq %{noautoreq_regex}
%else
%define _requires_exceptions %{noautoreq_regex}
%endif

Summary:	NVIDIA CUDA Toolkit libraries
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	cudatoolkit_%{version}_linux_32_ubuntu11.04.run
Source1:	cudatoolkit_%{version}_linux_64_ubuntu11.04.run
Source2:	nvidia
Source10:	nvvp.desktop
License:	Freeware
Group:		System/Libraries
Url:		http://www.nvidia.com/cuda/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post):	/sbin/ldconfig
Requires(postun): /sbin/ldconfig
Suggests:	nvidia >= %{driver_ver}

# We don't require installation of the NVIDIA graphics drivers so that 
# folks can do CUDA development on systems without NVIDIA hardware.

# A library, libcudainj.so, was introduced in CUDA 4.1, which depends
# on libcuda.so. It is not needed to compile CUDA programs, though.

%description
NVIDIA(R) CUDA(TM) is a general purpose parallel computing architecture
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
Suggests:	gcc-c++

%description devel
NVIDIA(R) CUDA(TM) is a general purpose parallel computing architecture
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

%package -n nvidia-compute-profiler
Summary:	NVIDIA Compute Visual Profiler
Group:		Development/Other
Requires:	java
Obsoletes:	nvidia-cuda-profiler, nvidia-opencl-profiler
Suggests:	nvidia-devel >= %{driver_ver}
Suggests:	%{name} = %{version}-%{release}
BuildRequires:	imagemagick

# We don't strictly require NVIDIA CUDA Toolkit, because the profiler
# could be used to analyze CSV profile logs obtained elsewhere.

%description -n nvidia-compute-profiler
NVIDIA(R) CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the Compute Visual Profiler for CUDA and OpenCL.

%prep
%setup -q -T -c %{name}-%{version}

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_usr}
%__install -d -m 755 %{buildroot}%{_datadir}/%{name}
%__install -d -m 755 %{buildroot}/%{_docdir}/%{name}-devel
%__install -d -m755 %{buildroot}%{_datadir}/applications

%ifarch %ix86
bash %SOURCE0 --tar xf -C %{buildroot}%{_usr}
%else
bash %SOURCE1 --tar xf -C %{buildroot}%{_usr}
%__rm -rf %{buildroot}/usr/lib 
%__sed -i 's/lib/lib64/g' %{buildroot}%{_bindir}/nvcc.profile
%endif

%__mv %{buildroot}%{_usr}/doc %{buildroot}/%{_docdir}/%{name}-devel/
%__rm -rf %{buildroot}%{_usr}/install-linux.pl
%__mv %{buildroot}%{_usr}/{extras,src,tools} %{buildroot}/%{_datadir}/%{name}
%__rm -rf %{buildroot}/%{_usr}/libnvvp/jre
%__ln_s %{_usr}/libnvvp/nvvp %{buildroot}/%{_bindir}


for S in 16 24 32 48 64 128 192 256; do
 %__install -d -m755 %{buildroot}%{_iconsdir}/hicolor/$S\x$S/apps
 convert -scale $S\x$S %{buildroot}/%{_usr}/libnvvp/icon.xpm %{buildroot}%{_iconsdir}/hicolor/$S\x$S/apps/nvvp.png
done

%__install -D -m 755 %SOURCE2 %{buildroot}%{_sysconfdir}/init.d/nvidia
%__install -m644 %{SOURCE10} %{buildroot}%{_datadir}/applications/

%clean
%__rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%_libdir/*.so.*
%_sysconfdir/init.d/*

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}-devel/*
%_bindir/*
%exclude %_bindir/nvvp
%_libdir/*.so
%_includedir/*
%_usr/open64/*
%_usr/nvvm/*
%_datadir/%{name}/*

%files -n nvidia-compute-profiler
%defattr(-,root,root)
%_bindir/nvvp
%_usr/libnvvp/.eclipseproduct
%_usr/libnvvp/*
%_datadir/applications/nvvp.desktop
%_iconsdir/hicolor/*

