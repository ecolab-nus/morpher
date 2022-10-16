# Morpher - Integrated Compilation and Simulation Framework for CGRA

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

### 3. Build all the submodules:
    bash build_all.sh

### 4. Test Environment Dependencies:
    Activate python3 virtual environment
    pip install -r python_requirements.txt
    sudo apt-get install gcc-multilib g++-multilib

## Compiling kernels:

1) Specify the target arch, dfg_type, mapping method, memory bank sizes,.. in config/<>.yaml file. (default_config file targets hycube 4x4 architecture)
2) Run the script:  ``$python run_morpher.py <path to c source code in benchmark folder>  <target function> <configurations(default: config/default_config.yaml)>``. 

Examples: 

1. Compile and verify simple kernels on hycube 4x4:

``$python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add``

Please refer the following workflow for more examples.

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Run%20Examples/badge.svg)](https://github.com/ecolab-nus/morpher/actions)

2. Compile and verify kernels from Microspeech Application:

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Run%20Microspeech/badge.svg)](https://github.com/ecolab-nus/morpher/actions)


# Publications

[Morpher: An Open-Source Integrated Compilation and Simulation Framework for CGRA](https://www.comp.nus.edu.sg/~tulika/WOSET_MORPHER_2022.pdf)
(to appear in Workshop on Open-Source EDA Technology co-sponsored by ICCAD 2022)

        @article{morpher-woset2022,
            title   = "{Morpher: An Open-Source Integrated Compilation and Simulation Framework for CGRA}",
            author  = {Dhananjaya Wijerathne, Zhaoying Li, Manupa Karunaratne, Li-Shiuan Peh, Tulika Mitra},
            journal = {Fifth Workshop on Open-Source EDA Technology (WOSET)},
            month   = {November},
            year    = {2022},
        } 


