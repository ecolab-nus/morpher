# Morpher

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Build%20and%20Test/badge.svg)](https://github.com/ecolab-nus/morpher/actions)

Morpher is a powerful, integrated compilation and simulation framework for CGRA, that fills this gap
with a flexible approach enabling easy specification of complex architectural features and automated
modeling of these features in efficient compiler, simulator.

clone first:  `git clone --recurse-submodules  https://github.com/ecolab-nus/Morpher.git` \
pull the latest change of submodule.:  `git submodule update --remote`

## Build dependencies:

This version requires LLVM 10.0.0 and JSON libraries. 

### LLVM, clang, polly (for DFG Generator):

Read https://llvm.org/docs/GettingStarted.html
follow https://github.com/llvm/llvm-project

    git clone https://github.com/llvm/llvm-project.git
    git checkout <correct version> (llvm10.0.0)
    cd llvm-project
    mkdir build
    cd build
    cmake -DLLVM_ENABLE_PROJECTS='polly;clang' -G "Unix Makefiles" ../llvm
    make -j4
    sudo make install

Important points:

    make sure to checkout correct version before building
    better to use gold linker instead of ld if you face memory problem while building: https://stackoverflow.com/questions/25197570/llvm-clang-compile-error-with-memory-exhausted
    don't use release type use default debug version (will take about 70GB disk space)

### JSON (for DFG Generator and CGRA mapper):
https://blog.csdn.net/jiaken2660/article/details/105155257


    git clone https://github.com/nlohmann/json.git
    mkdir build
    cd build
    cmake ../
    make -j2
    sudo make install

## Build all the submodules:
bash build_all.sh

## Running example:

1) Activate python3 virtual environment (https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/)
2) Specify the target arch, dfg_type, mapping method, memory bank sizes,.. in config/<>.yaml file. (default_config file targets hycube 4x4 architecture)
3) Run the script:  ``$python run_morpher.py <path to c source code in benchmark folder>  <target function> <configurations(default: config/default_config.yaml)>``. 

Example (running array_add on hycube 4x4): ``$python run_morpher.py morpher_benchmarks/array_add/array_add.c array_add``




