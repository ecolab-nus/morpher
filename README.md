![morpher_cover](https://user-images.githubusercontent.com/12274945/198943201-17e9ff67-62b3-445f-bd04-feac08da1601.png)

# Morpher_light: A lightweight version of Morpher

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Build%20and%20Test/badge.svg)](https://github.com/ecolab-nus/morpher/actions)
[![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/Dhananjayadmd/5baff68360b70cb31e4d861cf11f219e/raw/clone.json&logo=github)](https://github.com/MShawon/github-clone-count-badge)


Morpher_light is a simplified version of morpher, achieved by removing AGI instructions to simplify DFG generation. It offers a faster yet accurate simulation for CGRA-based systems. It also supports real-world applications and allows easy specification of complex architectural features. This version is ideal for rapid design space exploration and application-level development.


## Getting Started:

Note: Morpher_light requires LLVM 10.0.0 and g++ version cannot be higher than g++-v7. 


### build on your machine
* Pull the code
clone first:  `git clone --branch mopher_light https://github.com/ecolab-nus/morpher.git` \
pull the latest changes of submodules.:  `git submodule update --init --remote`


* Install LLVM, clang, polly (for DFG Generator):

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

* Build all the submodules:
    `bash build_all.sh`
* Test Environment Dependencies:\
    Activate python3 virtual environment\
    `pip install -r python_requirements.txt`\
    `sudo apt-get install gcc-multilib g++-multilib`

## Compiling kernels:

1) If you want to use the morpher_light version, make sure `dfg_type: 'PartPredLight'` and `morpher_light: 'yes'` in config/<>.yaml file (default_config file targets hycube 4x4 architecture). The following shows the template settings of the config file:

        json_arch: "hycube_original_mem.json"
        json_arch_before_memupdate: 'hycube_original_updatemem.json'
        mapper_subfolder: 'hycube'
        dfg_type: 'PartPredLight'
        init_II: 0
        ydim: 4
        xdim: 4
        numberofbanks: 2
        banksize: 2048
        max_test_samples: 5
        mapping_method: 0
        llvm_debug_type: 'no'
        morpher_light: 'yes'

2) Run the script:  ``$python run_morpher.py <path to c source code in benchmark folder>  <target function> <configurations(default: config/default_config.yaml)>``. 

Examples (running array_add on hycube 4x4):

``$python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add ./config/default_light_config.yaml``

# Publications

[WOSET] [Morpher: An Open-Source Integrated Compilation and Simulation Framework for CGRA](https://www.comp.nus.edu.sg/~tulika/WOSET_MORPHER_2022.pdf)\
(to appear in Workshop on Open-Source EDA Technology co-sponsored by ICCAD 2022)

        @article{morpher-woset2022,
            title   = "{Morpher: An Open-Source Integrated Compilation and Simulation Framework for CGRA}",
            author  = {Dhananjaya Wijerathne, Zhaoying Li, Manupa Karunaratne, Li-Shiuan Peh, Tulika Mitra},
            journal = {Fifth Workshop on Open-Source EDA Technology (WOSET)},
            month   = {November},
            year    = {2022},
        } 
        
[DAC] [PANORAMA: Divide-and-Conquer Approach for Mapping Complex Loop Kernels on CGRA](https://www.comp.nus.edu.sg/~tulika/DAC22.pdf)\
Dhananjaya Wijerathne, Zhaoying Li, Thilini Kaushalya Bandara, Tulika Mitra\
59th ACM/IEEE Design Automation Conference, 2022 __Publicity Paper__\
[Artifact Link](https://github.com/ecolab-nus/panorama)

[HPCA] [LISA: Graph Neural Network based Portable Mapping on Spatial Accelerators](https://www.comp.nus.edu.sg/~tulika/HPCA_LISA_2022.pdf)\
Zhaoying Li, Dan Wu, Dhananjaya Wijerathne, Tulika Mitra\
28th IEEE International Symposium on High-Performance Computer Architecture, 2022\
[Artifact Link](https://github.com/ecolab-nus/lisa) __Distinguished Artifact Award__

[ASPLOS] [REVAMP: A Systematic Framework for Heterogeneous CGRA Realization](https://www.comp.nus.edu.sg/~tulika/asplos22.pdf)\
Thilini Kaushalya Bandara, Dhananjaya Wijerathne, Tulika Mitra, Li-Shiuan Peh\
27th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, 2022\
[Artifact Link](https://zenodo.org/record/5848404#.YgyrPTFByUk)

[TCAD] [HiMap: Fast and Scalable High-Quality Mapping on CGRA via Hierarchical Abstraction](https://www.comp.nus.edu.sg/~tulika/HiMap-TCAD.pdf)\
Dhananjaya Wijerathne, Zhaoying Li, Anuj Pathania, Tulika Mitra, Lothar Thiele\
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 41(10) 2022

[TCAD] [ChordMap: Automated Mapping of Streaming Applications onto CGRA](https://ieeexplore.ieee.org/document/9351547)\
Zhaoying Li, Dhananjaya Wijerathne, Xianzhang Chen, Anuj Pathania, Tulika Mitra\
IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 41(2) 2022

[Book Chapter] [Coarse-Grained Reconfigurable Array (CGRA)](https://www.comp.nus.edu.sg/~tulika/CGRA-Survey.pdf)\
Zhaoying Li, Dhananjaya Wĳerathne, Tulika Mitra\
Book chapter in “Handbook of Computer Architecture”, Springer (Invited)

[DATE] [HiMap: Fast and Scalable High-Quality Mapping on CGRA via Hierarchical Abstraction](https://www.comp.nus.edu.sg/~tulika/HiMap_DATE_2021.pdf)\
Dhananjaya Wijerathne, Zhaoying Li, Anuj Pathania, Tulika Mitra, Lothar Thiele\
Design Automation and Test in Europe 2021

[TECS] [CASCADE: High Throughput Data Streaming via Decoupled Access/Execute CGRA](https://www.comp.nus.edu.sg/~tulika/TECS-CASCADE19.pdf)\
Dhananjaya Wijerathne, Zhaoying Li, Manupa Karunaratne, Anuj Pathania, Tulika Mitra\
ACM Transactions on Embedded Computing Systems\
Special Issue on ACM/IEEE International Conference on Compilers, Architecture, and Synthesis for Embedded Systems 2019

[ICCAD] [4D-CGRA : Introducing the branch dimension to spatio-temporal application mapping of CGRAs](https://www.comp.nus.edu.sg/~tulika/4D-CGRA-ICCAD19.pdf)\
Manupa Karunaratne, Dhananjaya Wijerathne, Tulika Mitra, Li-Shiuan Peh\
38th ACM/IEEE International Conference on Computer Aided Design, November 2019

[A-SSCC] [HyCUBE: a 0.9V 26.4 MOPS/mW, 290 pJ/cycle, Power Efficient Accelerator for IoT Applications](https://www.comp.nus.edu.sg/~tulika/Hycube_for_ASSCC_2019.pdf)\
Bo Wang, Manupa Karunarathne, Aditi Kulkarni, Tulika Mitra, Li-Shiuan Peh\
IEEE Asian Solid-State Circuits Conference, November 2019

[DAC] [DNestMap : Mapping Deeply-Nested Loops on Ultra-Low Power CGRAs](https://www.comp.nus.edu.sg/~tulika/DAC18-CGRA.pdf)\
Manupa Karunaratne, Cheng Tan, Aditi Kulkarni, Tulika Mitra, Li-Shiuan Peh\
55th ACM/IEEE Design Automation Conference, June 2018

[DAC] [HyCUBE : A CGRA with Reconfigurable Single-cycle Multi-hop Interconnect](https://www.comp.nus.edu.sg/~tulika/DAC17.pdf)\
Manupa Karunaratne, Aditi Kulkarni, Tulika Mitra, Li-Shiuan Peh\
54th ACM/IEEE Design Automation Conference, June 2017

[ACM-TRETS] [Graph Minor Approach for Application Mapping on CGRAs](https://www.comp.nus.edu.sg/~tulika/TRETS14.pdf)\
Liang Chen, Tulika Mitra\
ACM Transactions on Reconfigurable Technology and Systems 2014

[FPT] Graph Minor Approach for Application Mapping on CGRAs [Much expanded journal version](https://www.comp.nus.edu.sg/~tulika/TRETS14.pdf)\
Liang Chen, Tulika Mitra\
International Conference on Field Programmable Technology, December 2012\
__Best Paper Award__

