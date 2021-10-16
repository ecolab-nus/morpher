# Morpher
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

## build all the submodules:
bash build_all.sh
