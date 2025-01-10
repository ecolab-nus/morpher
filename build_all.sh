cd Morpher_DFG_Generator
mkdir build
cd build
cmake  -DCMAKE_BUILD_TYPE=Release ..
make all -j 2
cd ../../Morpher_CGRA_Mapper
mkdir build
cd build
cmake   -DCMAKE_BUILD_TYPE=Release ..
make all -j 8
cd ../../hycube_simulator
cd src
mkdir build
cd build
cmake  ..
make all -j 8
echo "buld success!!!"
