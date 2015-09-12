%define driver_ver 295.40

%if %{_use_internal_dependency_generator}
%define __noautoreq 'libcuda.so.*|libcudart.so.*|devel\\(libcuda.*\\)|devel\\(libcudart.*\\)|python\\(abi\\)|libnvcuvid\\.so\\.(.*)'
%define __noautoprovfiles /usr/libnvvp
%define __noautoreqfiles /usr/libnvvp
%define __noautoprov 'libcairo\\.so\\.2(.*)'
%else
%define _requires_exceptions libcuda.so.*\\|libcudart.so.*\\|devel(libcuda.*)\\|devel(libcudart.*)\\|python(abi)\\|libnvcuvid.so.*
%endif

Summary:	NVIDIA CUDA Toolkit libraries

Name:		nvidia-cuda-toolkit
Version:	5.5.22
Release:	3
Source0:	http://developer.download.nvidia.com/compute/cuda/5_5/rel/installers/cuda_%{version}_linux_32.run
Source1:	http://developer.download.nvidia.com/compute/cuda/5_5/rel/installers/cuda_%{version}_linux_64.run
Source2:	nvidia
Source10:	nvvp.desktop
Source11:	nsight.desktop
Source100:	nvidia-cuda-toolkit.rpmlintrc
License:	Freeware
Group:		System/Libraries
Url:		http://www.nvidia.com/cuda/
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

%package -n nvidia-nsight
Summary:	NVIDIA Nsight IDE

Group:		Development/Other
Requires:	java
Suggests:	nvidia-devel >= %{driver_ver}

# We don't strictly require NVIDIA CUDA Toolkit, because Nsight IDE
# could be used to develop CUDA programs on a remote node.

%description -n nvidia-nsight
NVIDIAÂ® CUDAâ„¢ is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDAâ„¢ architecture, developers can, today,
use C++, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDAâ„¢ enabled
processor. Support for other languages, like FORTRAN, Python or Java,
is available from third parties.

This package contains Nsight Eclipse Edition, a full-featured CUDA IDE.

%prep
%setup -q -T -c %{name}-%{version}

%install

install -d -m 755 %{buildroot}%{_usr}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}/%{_docdir}/%{name}-devel
install -d -m755 %{buildroot}%{_datadir}/applications

%ifarch %ix86
bash %{SOURCE0} --tar xf -C .
./run_files/cuda-linux-rel-%{version}-16488124.run --tar xf -C %{buildroot}%{_usr}
%else
bash %{SOURCE1} --tar xf -C . 
./run_files/cuda-linux64-rel-%{version}-16488124.run --tar xf -C %{buildroot}%{_usr}
rm -rf %{buildroot}/usr/lib 
sed -i 's/lib/lib64/g' %{buildroot}%{_bindir}/nvcc.profile
# (tmb) restore libdevice
sed -i 's/lib64device/libdevice/g' %{buildroot}%{_bindir}/nvcc.profile
%endif

mv %{buildroot}%{_usr}/doc %{buildroot}/%{_docdir}/%{name}-devel/
rm -rf %{buildroot}%{_usr}/install-linux.pl
mv %{buildroot}%{_usr}/{extras,src,tools} %{buildroot}/%{_datadir}/%{name}
rm -rf %{buildroot}/%{_usr}/jre

rm -rf %{buildroot}%{_usr}/InstallUtils.pm
mv %{buildroot}%{_usr}/EULA.txt %{buildroot}%{_docdir}/%{name}-devel/

for S in 16 24 32 48 64 128 192 256; do
 install -d -m755 %{buildroot}%{_iconsdir}/hicolor/$S\x$S/apps
 convert -scale $S\x$S %{buildroot}/%{_usr}/libnvvp/icon.xpm %{buildroot}%{_iconsdir}/hicolor/$S\x$S/apps/nvvp.png
 convert -scale $S\x$S %{buildroot}/%{_usr}/libnsight/icon.xpm %{buildroot}%{_iconsdir}/hicolor/$S\x$S/apps/nsight.png
done

install -d -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/nvidia
install -m644 %{SOURCE10} %{buildroot}%{_datadir}/applications/
install -m644 %{SOURCE11} %{buildroot}%{_datadir}/applications/

%files
%{_libdir}/*.so.*
%{_sysconfdir}/init.d/*

%files devel
%doc %{_docdir}/%{name}-devel/*
%{_bindir}/*
%exclude %{_bindir}/nvvp
%exclude %{_bindir}/nsight
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_usr}/open64/*
%{_usr}/nvvm/*
%{_datadir}/%{name}/*

%files -n nvidia-compute-profiler
%{_bindir}/nvvp
%{_usr}/libnvvp/.eclipseproduct
%{_usr}/libnvvp/*
%{_datadir}/applications/nvvp.desktop
%{_iconsdir}/hicolor/*/apps/nvvp.png

%files -n nvidia-nsight
%{_bindir}/nsight
%{_usr}/libnsight/.eclipseproduct
%{_usr}/libnsight/*
%{_datadir}/applications/nsight.desktop
%{_iconsdir}/hicolor/*/apps/nsight.png
