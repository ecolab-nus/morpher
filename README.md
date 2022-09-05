# Morpher - An end-to-end Toolchain for CGRA

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Build%20and%20Test/badge.svg)](https://github.com/ecolab-nus/morpher/actions)

Morpher is a powerful, integrated compilation and simulation framework for CGRA, that fills this gap
with a flexible approach enabling easy specification of complex architectural features and automated
modeling of these features in efficient compiler, simulator.



## Getting Started:

Note: Morpher requires LLVM 10.0.0 and g++ version cannot be higher than g++-v7. 

### 1. Pull the code
clone first:  `git clone --recurse-submodules  https://github.com/ecolab-nus/Morpher.git` \
pull the latest change of submodule.:  `git submodule update --remote`


### 2. Install LLVM, clang, polly (for DFG Generator):

Read https://llvm.org/docs/GettingStarted.html
follow https://github.com/llvm/llvm-project

    git clone https://github.com/llvm/llvm-project.git
    cd llvm-project
    git checkout llvmorg-10.0.0
    mkdir build
    cd build
    cmake -DLLVM_ENABLE_PROJECTS='polly;clang' -G "Unix Makefiles" ../llvm
    make -j4
    sudo make install

Important points:

    make sure to checkout correct version before building
    better to use gold linker instead of ld if you face memory problem while building: https://stackoverflow.com/questions/25197570/llvm-clang-compile-error-with-memory-exhausted
    use default debug version (will take about 70GB disk space)


### 3. Build all the submodules:
    bash build_all.sh

### 4. Test Dependencies:
    Activate python3 virtual environment (https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/)
    pip install -r python_requirements.txt
    sudo apt-get install gcc-multilib g++-multilib

## Running example:

1) Specify the target arch, dfg_type, mapping method, memory bank sizes,.. in config/<>.yaml file. (default_config file targets hycube 4x4 architecture)
2) Run the script:  ``$python run_morpher.py <path to c source code in benchmark folder>  <target function> <configurations(default: config/default_config.yaml)>``. 

Example (running array_add on hycube 4x4): ``$python run_morpher.py morpher_benchmarks/array_add/array_add.c array_add``




