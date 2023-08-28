  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
import re
import numpy as np
from tqdm import tqdm

import scripts.bin_to_trace as BT

############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

def main():

  #if not 'MORPHER_HOME' in os.environ:
  #  raise Exception('Set MORPHER_HOME directory as an environment variable (Ex: export MORPHER_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

  MORPHER_HOME = os. getcwd() #os.getenv('MORPHER_HOME')
  DFG_GEN_HOME = MORPHER_HOME + '/Morpher_DFG_Generator'
  MAPPER_HOME = MORPHER_HOME + '/Morpher_CGRA_Mapper'
  SIMULATOR_HOME = MORPHER_HOME + '/hycube_simulator'

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/benchmarks/pace_chip_experiments/array_add/' 
  MAPPER_KERNEL = MAPPER_HOME + '/applications/hycube8x8/array_add/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/hycube8x8/array_add/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)



#############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  os.system('./run_pass.sh array_add 2 8192')
  os.system('dot -Tpdf array_add_PartPredDFG.dot -o array_add_PartPredDFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final')
  list = os.listdir(MEM_TRACE)
  num_memory_traces = len(list)
  
  print("num_memory_traces number: ",num_memory_traces)
 # os.system('cp memtraces/loop_microspeech_conv_layer_hycube_INNERMOST_LN13_0.txt '+SIMULATOR_KERNEL)
  os.system('cp -r memtraces/ '+SIMULATOR_KERNEL)
  os.system('cp array_add_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp array_add_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp array_add_PartPredDFG.xml '+ MAPPER_KERNEL)

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system('rm *.bin') 
  os.system('mkdir binary')
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem.json array_add_mem_alloc.txt 8192 2 hycube_original_mem.json')
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem_RC.json array_add_mem_alloc.txt 8192 2 hycube_original_mem_RC.json')
  print('\nupdate memory allocation done!\n')

  os.system('../../../build/src/cgra_xml_mapper -d array_add_PartPredDFG.xml -x 4 -y 4 -j hycube_original_mem.json -t HyCUBE_4REG')
  for file in os.listdir("./"):
    if file.endswith(".bin"):
        II_left=int(file.split('II=')[-1].split(' ')[0].split('_MTP')[0].split(' ')[0])+1
    os.system('mv *.bin binary/left.bin')
  os.system('../../../build/src/cgra_xml_mapper -d array_add_PartPredDFG.xml -x 4 -y 4 -j hycube_original_mem_RC.json -t HyCUBE_4REG')
  for file in os.listdir("./"):
    if file.endswith(".bin"):
        II_right=int(file.split('II=')[-1].split(' ')[0].split('_MTP')[0].split(' ')[0])+1
  os.system('mv *.bin binary/right.bin')
  if II_left != II_right:
    sys.exit('Left and right II does not match!!')
    
 # os.chdir(SIMULATOR_KERNEL)
 # os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp binary/*.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)
  # list = os.listdir('memtraces')
  num_memory_traces = len(list) #comment it for whole invocation
  
  os.system('mv array_add_mem_alloc.txt mem_alloc.txt')
  os.system('python3 ../../../scripts/duplicate_config.py > dup.log')

  for invocations in range(0,num_memory_traces) :
    data_file = SIMULATOR_KERNEL + '/memtraces/array_add_trace_' + str(invocations) + '.txt'
    os.system('python3 ../../../scripts/skipdata.py --cubedata '+data_file)
    data_file_new = 'data_modi_' + str(invocations) + '.txt'
    os.system('cp data_modi.txt '+data_file_new)
  
  invocation = num_memory_traces // 4
  half_invocations = num_memory_traces % 4

  # invocation = min(invocation,10)
  print("invocation number: ",invocation)
  os.system('mkdir dataDump')
  if invocation > 0 :
   for i in range(0,invocation) :
    os.system('../../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str(i*4) +'.txt mem_alloc.txt 8 8 16384 data_modi_' + str((i*4 + 1)) + '.txt data_modi_' + str((i*4 + 2)) + '.txt data_modi_' + str((i*4 + 3)) +'.txt | tail -n 2 |head -n 1 > output.log')
    out_file = 'dumped_raw_data_i' + str(i)
    os.system('cp dumped_raw_data.txt dataDump/'+ out_file + '.txt')
    with open("output.log", 'r') as f:
      line = f.readline()
      success = False
      while line:
        if re.search("Mismatches::0", line):
          success = True
          line = f.readline()
      if not success:
        print("ERROR: FAIL AT MEMTRACE "+ str(i))
      else:
        print("SUCCEED AT MEMTRACE "+ str(i))

  if half_invocations == 1 :
    os.system('../../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384 | tail -n 2 |head -n 1 > output.log')
    out_file = 'dumped_raw_data_i' + str(invocation)
    os.system('cp dumped_raw_data.txt dataDump/'+ out_file + '.txt')

  
  if half_invocations == 2 :
    os.system('../../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384 data_modi_'  + str((invocation*4 + 1)) +'.txt | tail -n 2 |head -n 1 > output.log')
    out_file = 'dumped_raw_data_i' + str(invocation)
    os.system('cp dumped_raw_data.txt dataDump/'+ out_file + '.txt')


  if half_invocations == 3 :
    os.system('../../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384 data_modi_'  + str((invocation*4 + 1))  + '.txt data_modi_' + str((invocation*4 + 2)) +'.txt | tail -n 2 |head -n 1 > output.log')
    out_file = 'dumped_raw_data_i' + str(invocation)
    os.system('cp dumped_raw_data.txt dataDump/'+ out_file + '.txt')


  with open("output.log", 'r') as f:
    line = f.readline()
    success = False
    while line:
      if re.search("Mismatches::0", line):
        success = True
        line = f.readline()
    if not success:
      print("ERROR: FAIL AT MEMTRACE half invocation")
    else:
      print("SUCCEED AT MEMTRACE half invocation")

	
  print('\nSimulation done! -> invocations = %d , half invocations = %d ,memory traces=%d\n' % (invocation,half_invocations,num_memory_traces))

#############################################################################################################################################
##############                                                  DUMP TRACE                                                    ###############
#############################################################################################################################################
  os.chdir(SIMULATOR_KERNEL)
  os.system('mkdir traces')
  os.system('mkdir mem_files')
  for filename in os.listdir('dataDump'):
      if filename == 'dumped_raw_data_i0.txt':
        BT.dump_trace_full("duplicated_config.bin",'dataDump/'+filename,II_left,4,"array_add")
      else:
        BT.dump_trace_no_cmem('dataDump/'+filename,II_left,4)
       
  os.system('mv *.trc *.h traces/')



def my_mkdir(dir):
    try:
        os.makedirs(dir)  
    except:
        pass

if __name__ == '__main__':
  main()
