cd Morpher_DFG_Generator
mkdir build
cd build
cmake ..
make all -j 
cd ../../Morpher_CGRA_Mapper
mkdir build
cd build
cmake ..
make all -j
cd ../../hycube_simulator
cd src
mkdir build
cd build
cmake ..
make all -j
echo "buld success!!!"
