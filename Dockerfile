FROM ubuntu:18.04
# FROM continuumio/anaconda3:latest

LABEL maintainer="zhaoying@comp.nus.edu.sg"

RUN apt-get update \
        && apt-get install  -y g++ software-properties-common \
        && add-apt-repository ppa:ubuntu-toolchain-r/test \
        && apt update \
        && apt install -y make g++-7 clang-10 llvm-10 build-essential cmake git\
        && apt-get install -y libstdc++6 curl wget htop python3.8 python3-pip gcc-multilib g++-multilib vim graphviz \
	&& pip3 install  numpy tqdm pyyaml \
	&& update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
	&& update-alternatives --install /usr/bin/clang clang /usr/bin/clang-10 100 \
	&& update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-10 100 \
	&& update-alternatives --install /usr/bin/llc llc /usr/bin/llc-10 100 \
	&& update-alternatives --install /usr/bin/llvm-link llvm-link /usr/bin/llvm-link-10 100	\
	&& update-alternatives --install /usr/bin/opt opt /usr/bin/opt-10 100 \
	&& git clone --recurse-submodules https://github.com/ecolab-nus/morpher.git /home/hpca/morpher
