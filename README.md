![morpher_cover](https://user-images.githubusercontent.com/12274945/198943201-17e9ff67-62b3-445f-bd04-feac08da1601.png)

# Morpher: An Open-Source Tool for CGRA Accelerators 

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Build%20and%20Test/badge.svg)](https://github.com/ecolab-nus/morpher/actions)
[![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/Dhananjayadmd/5baff68360b70cb31e4d861cf11f219e/raw/clone.json&logo=github)](https://github.com/MShawon/github-clone-count-badge)

_<b>Morpher_LIGHT: We provide morpher_light now! It can compile and map in seconds!</b>_ [Click here to use the light version of morpher](#using-the-light-version-of-morpher).


Morpher is a powerful, integrated compilation and simulation framework, that can assist design space exploration and application-level developments of CGRA based systems. Morpher can take an application with a compute intensive kernel as input, compile the kernel onto a user-provided CGRA architecture, and automatically validate the compiled kernels through cycle-accurate simulation using test data extracted from the application. Morpher can handle real-world application kernels without being limited to simple toy kernels through its feature-rich compiler. Morpher architecture description language
lets users easily specify architectural features such as complex interconnects, multi-hop routing, and memory organizations. 





![framework](https://user-images.githubusercontent.com/12274945/198694251-ab21d639-8999-424a-bc5a-3e7921c638a0.png)

More information:
    [WOSET 2022 Presentation](https://woset-workshop.github.io/Videos/2022/12-Wijerathne-long.mp4) (Artifact demonstration from 13.25), 
    [WOSET 2022 paper](https://woset-workshop.github.io/PDFs/2022/12-Wijerathne-paper.pdf)
    
![ezgif com-gif-maker(2)](https://user-images.githubusercontent.com/12274945/198826823-5230947d-86eb-4493-a6fc-5f43d61ab2b4.gif)


## Getting Started:
You can build morpher on your Linux machine, or user docker on MAC/Linux.

Note: Morpher requires LLVM 10.0.0 and g++ version cannot be higher than g++-v7. 

### build with docker
 > ***for tutorial***
* Download the [docker file](https://raw.githubusercontent.com/ecolab-nus/morpher/main/Dockerfile) into an empty folder.
* Go to the folder and Build ``morpher`` image: ``$ docker build ./ -t morpher``. This takes around 15 minutes.
* Initalize: ``$ docker run --name morpher_tutorial -it morpher``
* Run ``cd /home/user/morpher`` and build all the submodules ``bash build_all.sh``. This takes a few minutes.
* You should be able to run this command ``python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add`` and see "Simulation test passed!!!". This takes a few minutes.

To start the container again
* Start the container: ``$ docker start morpher_tutorial``
* Get into the container: ``docker exec -it morpher_tutorial /bin/bash``
<br/><br/>
<br/><br/>

### build on your machine
* Pull the code
clone first:  `git clone --recurse-submodules  https://github.com/ecolab-nus/Morpher.git` \
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

1) Specify the target arch, dfg_type, mapping method, memory bank sizes,.. in config/<>.yaml file. (default_config file targets hycube 4x4 architecture)
2) Run the script:  ``$python run_morpher.py <path to c source code in benchmark folder>  <target function> <configurations(default: config/default_config.yaml)>``. 

Examples: 

1. Compile and verify simple kernels on hycube 4x4:

``$python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add``

Please refer the following workflow for more examples.

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Run%20Examples/badge.svg)](https://github.com/ecolab-nus/morpher/actions)

2. Compile and verify kernels from Microspeech Application:

[![Actions Status](https://github.com/ecolab-nus/morpher/workflows/Run%20Microspeech/badge.svg)](https://github.com/ecolab-nus/morpher/actions)



## Miscellaneous

### Using the light version of Morpher

To use the light version of morpher,  make sure `dfg_type: 'PartPredLight'` and `morpher_light: 'yes'` are set in the `config/<>.yaml` file. The following shows the template settings of the config file:

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

If you set morpher_light as "yes", we will force the DFG type to be _PartPredLight_

Examples (running array_add on hycube 4x4 using the light mode):


``$python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add ./config/default_light_config.yaml``

### Change to 16 bit
The default precision is int32. To change to 16 bit, uncomment "#define ARCHI_16BIT" in line 4 of "Morpher_DFG_Generator/include/morpherdfggen/common/ArchPrecision.h" and "hycube_simulator/src/ArchPrecision.h"

## Publications

**If you use Morpher in your work, please cite this paper.**

[ICCAD] [Building an Open CGRA Ecosystem for Agile Innovation](https://arxiv.org/abs/2508.19090)\
Rohan Juneja, Pranav Dangi, Thilini Kaushalya Bandara, Zhaoying Li, Dhananjaya Wijerathne, Li-Shiuan Peh, Tulika Mitra
(to appear in ICCAD 2025)
        
        @misc{juneja2025buildingopencgraecosystem,
        title={Building an Open CGRA Ecosystem for Agile Innovation}, 
        author={Rohan Juneja and Pranav Dangi and Thilini Kaushalya Bandara and Zhaoying Li and Dhananjaya Wijerathne and Li-Shiuan Peh and Tulika Mitra},
        year={2025},
        eprint={2508.19090},
        archivePrefix={arXiv},
        primaryClass={cs.AR},
        url={https://arxiv.org/abs/2508.19090}, }


**Or when working with HyCUBE (now PACE), please reference this paper.**

[HotChips] [PACE: A Scalable and Energy Efficient CGRA in a RISC-V SoC for Edge Computing Applications](https://ieeexplore.ieee.org/abstract/document/10665106)\
Vishnu P. Nambiar, Yi Sheng Chong, Thilini Kaushalya Bandara, Dhananjaya Wijerathne, Zhaoying Li, Rohan Juneja, Li-Shiuan Peh, Tulika Mitra, Anh Tuan Do
IEEE Hot Chips Symposium (HCS) 2024

        @INPROCEEDINGS{10665106,
        author={Nambiar, Vishnu P. and Chong, Yi Sheng and Bandara, Thilini Kaushalya and Wijerathne, Dhananjaya and Li, Zhaoying and Juneja, Rohan and Peh, Li-Shiuan and Mitra, Tulika and Do, Anh Tuan},
        booktitle={2024 IEEE Hot Chips 36 Symposium (HCS)}, 
        title={PACE: A Scalable and Energy Efficient CGRA in a RISC-V SoC for Edge Computing Applications}, 
        year={2024},
        volume={},
        number={},
        pages={1-1},
        keywords={Program processors;Energy efficiency;Vectors;Hardware;Flow graphs;Arrays;Kernel},
        doi={10.1109/HCS61935.2024.10665106}}


[WOSET] [Morpher: An Open-Source Integrated Compilation and Simulation Framework for CGRA](https://www.comp.nus.edu.sg/~tulika/WOSET_MORPHER_2022.pdf)\
Dhananjaya Wijerathne, Zhaoying Li, Manupa Karunaratne, Li-Shiuan Peh, Tulika Mitra
Workshop on Open-Source EDA Technology, International Conference on Computer-Aided Design 2022

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

