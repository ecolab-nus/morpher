# please change simulator to 8x8-4tile branch and edit "Morpher_DFG_Generator/include/morpherdfggen/common/dfg.h", uncomment "#define ARCHI_16BIT". And run bash build_all.sh
# edit Morpher_DFG_Generator/benchmarks/pace_chip_experiments/microspeech/microspeech_int16_test.c line 874 and 886 to your location
export MORPHER_HOME="$PWD"
python run_morpher_microspeech16.py
