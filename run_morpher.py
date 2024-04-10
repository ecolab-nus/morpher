  #!/usr/bin/env python
import sys
import os
import os.path
import shutil

from os import O_TRUNC, listdir
from os.path import isfile, join
import re
import numpy as np
from tqdm import tqdm
import yaml
from time import sleep
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator




def main(csource, function, config= "config/default_config.yaml"):

  runmode = 'runall' # runall, dfg_gen_only, mapper_only, sim_only

  print(r"""
    __  ___                 __                 ________________  ___       ____            _                ______                                             __  
   /  |/  /___  _________  / /_  ___  _____   / ____/ ____/ __ \/   |     / __ \___  _____(_)___ _____     / ____/________ _____ ___  ___ _      ______  _____/ /__
  / /|_/ / __ \/ ___/ __ \/ __ \/ _ \/ ___/  / /   / / __/ /_/ / /| |    / / / / _ \/ ___/ / __ `/ __ \   / /_  / ___/ __ `/ __ `__ \/ _ \ | /| / / __ \/ ___/ //_/
 / /  / / /_/ / /  / /_/ / / / /  __/ /     / /___/ /_/ / _, _/ ___ |   / /_/ /  __(__  ) / /_/ / / / /  / __/ / /  / /_/ / / / / / /  __/ |/ |/ / /_/ / /  / ,<   
/_/  /_/\____/_/  / .___/_/ /_/\___/_/      \____/\____/_/ |_/_/  |_|  /_____/\___/____/_/\__, /_/ /_/  /_/   /_/   \__,_/_/ /_/ /_/\___/|__/|__/\____/_/  /_/|_|  
                 /_/                                                                     /____/                                                                    
    """)

  # https://www.ascii-art-generator.org/
  # Font: slant

  stream = open(config, 'r')
  config_dict = yaml.safe_load(stream)
  # for key, value in config_dict.items():
  #       print (key + " : " + str(value))

  json_arch_before_memupdate = config_dict["json_arch_before_memupdate"]
  json_arch = config_dict["json_arch"]
  mapper_subfolder = config_dict["mapper_subfolder"]
  dfg_type = config_dict["dfg_type"]
  init_II = config_dict["init_II"]
  ydim = config_dict["ydim"]
  xdim = config_dict["xdim"]
  numberofbanks = config_dict["numberofbanks"]
  banksize = config_dict["banksize"] #8192*2 #8192*2
  totalsize = numberofbanks*banksize
  max_test_samples = config_dict["max_test_samples"]
  mapping_method = config_dict["mapping_method"]
  llvm_debug_type = config_dict["llvm_debug_type"] #'nothing' #'instrumentation'
  morpher_light = config_dict["morpher_light"]

  kernel = function
  appfolder, csourcefile = csource.rsplit('/', 1)

  # if not 'MORPHER_HOME' in os.environ:
  #   raise Exception('Set MORPHER_HOME directory as an environment variable (Ex: export MORPHER_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

  MORPHER_HOME = os.getcwd() #os.getenv('MORPHER_HOME')
  DFG_GEN_HOME = MORPHER_HOME + '/Morpher_DFG_Generator'
  MAPPER_HOME = MORPHER_HOME + '/Morpher_CGRA_Mapper'
  SIMULATOR_HOME = MORPHER_HOME + '/hycube_simulator'

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/benchmarks/'+appfolder+'/'
  MAPPER_KERNEL = MAPPER_HOME + '/benchmarks/'+mapper_subfolder+'/'+appfolder+'/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/benchmarks/'+appfolder+'/'

  # my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)
  
  MEM_TRACE = DFG_GEN_KERNEL + 'memtraces'
  
  my_mkdir(MEM_TRACE)
  # print('\n\n############## Morpher CGRA Framework #################\n')
  print('\n Kernel: %s \n C source: %s/benchmarks/%s \n CGRA arch: %s/json_arch/%s \n Config: %s\n Run mode: %s\n'% (kernel, DFG_GEN_HOME,csource, MAPPER_HOME, json_arch, config, runmode))


  

##############################################################################################################################################
  if runmode == 'runall' or runmode == 'dfg_gen_only':
    print('-----Running Morpher_DFG_Generator-----\n')
    os.chdir(DFG_GEN_KERNEL)
  
    
    # os.system('./run_pass.sh %s 2 2048' % (kernel))
    os.system('rm memtraces/*')
    os.system('rm *.xml')
    os.system('rm *.dot')
    print('Generating IR..\n')
    os.system('clang -D CGRA_COMPILER -target i386-unknown-linux-gnu -Wno-implicit-function-declaration -Wno-format -Wno-main-return-type -c -emit-llvm -O2 -fno-tree-vectorize -fno-unroll-loops %s -S -o %s.ll'%(csourcefile,kernel))
    #os.system('clang -D CGRA_COMPILER -target i386-unknown-linux-gnu -Wno-implicit-function-declaration -Wno-format -Wno-main-return-type -c -emit-llvm -O2 -fno-vectorize -fno-slp-vectorize -fno-tree-vectorize -fno-inline -fno-unroll-loops %s -S -o %s.ll'%(csourcefile,kernel))

    print('Optimizing IR..\n')
    os.system('opt -gvn -mem2reg -memdep -memcpyopt -lcssa -loop-simplify -licm -loop-deletion -indvars -simplifycfg -mergereturn -indvars  %s.ll -S -o %s_opt.ll' % (kernel,kernel))

    print('Generating DFG (%s_PartPredDFG.xml/dot) and data layout (%s_mem_alloc.txt)..\n' % (kernel,kernel))
    os.system('opt -load %s/build/src/libdfggenPass.so -fn %s -nobanks %d -banksize %d -type %s  -skeleton %s_opt.ll -S -o %s_opt_instrument.ll' % (DFG_GEN_HOME,kernel,numberofbanks,banksize, dfg_type,kernel,kernel))


    os.system('dot -Tpdf %s_PartPredDFG.dot -o %s_PartPredDFG.pdf' % (kernel,kernel))
    os.system('cp '+kernel+'_PartPredDFG.xml '+ MAPPER_KERNEL )
    os.system('rm *.log')

    #if json_arch == 'hycube_original_mem.json':
    print('\nCode instrumentation..\n')
    os.system('clang -target i386-unknown-linux-gnu -c -emit-llvm -S %s/src/instrumentation/instrumentation.cpp -o instrumentation.ll' % DFG_GEN_HOME)
    if kernel=='kernel_symm':
        os.system('clang -D CGRA_COMPILER -target i386-unknown-linux-gnu -c -emit-llvm -O2 -fno-tree-vectorize -fno-inline -fno-unroll-loops polybench.c -S -o polybench.ll')
        os.system('llvm-link %s_opt_instrument.ll instrumentation.ll polybench.ll -o final.ll' % (kernel))
    else:
        os.system('llvm-link %s_opt_instrument.ll instrumentation.ll -o final.ll' % (kernel))

    os.system('llc -filetype=obj final.ll -o final.o')
    os.system('clang++ -m32 final.o -o final')


  
    print('Running instrumented code to generate the data memory content (memtraces/%s_trace_x.txt)..\n' % kernel)
    os.system('./final 1> final_log.txt 2> final_err_log.txt')
    # os.system('./final')
    os.system('cp memtraces/'+kernel+'_trace_0.txt '+SIMULATOR_KERNEL)
    os.system('cp '+kernel+'_mem_alloc.txt '+SIMULATOR_KERNEL )
    os.system('cp '+kernel+'_mem_alloc.txt '+MAPPER_KERNEL )
    
    os.system('rm *.ll')
  
##############################################################################################################################################
  if runmode == 'runall' or runmode == 'mapper_only':
    print('\n-----Running Morpher_CGRA_Mapper-----\n')
    os.chdir(MAPPER_KERNEL)
     
    #os.system('rm *.bin')  
    if '_mem' in json_arch:
      print('\nUpdating memory allocation..\n')
      os.system('python %s/update_mem_alloc.py %s/json_arch/%s %s_mem_alloc.txt %d %d %s' % (MAPPER_HOME,MAPPER_HOME, json_arch_before_memupdate,kernel,banksize,numberofbanks, json_arch))
      os.system('%s/build/src/cgra_xml_mapper -d %s_PartPredDFG.xml -x %d -y %d -j %s -i %d -t HyCUBE_4REG -m %d' % (MAPPER_HOME,kernel,xdim,ydim,json_arch, init_II, mapping_method))

      os.chdir(SIMULATOR_KERNEL)
      os.system('rm *.bin')  
  
      os.chdir(MAPPER_KERNEL)
      os.system('cp *.bin '+ SIMULATOR_KERNEL)
    else:
      os.system('%s/build/src/cgra_xml_mapper -d %s_PartPredDFG.xml -x %d -y %d -j %s/json_arch/%s -i %d -m %d' % (MAPPER_HOME,kernel,xdim,ydim,MAPPER_HOME, json_arch, init_II, mapping_method))
  
  

##############################################################################################################################################
  # if (runmode == 'runall' or runmode == 'sim_only'):
  #   print('\n-----Running hycube_simulator-----\n')
  #   os.chdir(SIMULATOR_KERNEL)
  
  #   os.system('%s/src/build/hycube_simulator -c *.bin -d %s_trace_0.txt -a %s_mem_alloc.txt' % (SIMULATOR_HOME,kernel,kernel))
    
  #   f = open("sim_result.txt", "r")
  #   sim_result = f.read()
  #   sim_result_ = sim_result.split(",")
  #   sim_result__ = [int(e) for e in sim_result_]
  #   matches, mismatches = sim_result__
  #   if mismatches == 0:
  #     print('Simulation test passed!')

  if ((runmode == 'runall' or runmode == 'sim_only') and not morpher_light):
    print('\n-----Running hycube_simulator-----\n')
    os.chdir(SIMULATOR_KERNEL) 
    files = [f for f in listdir(MEM_TRACE) if isfile(join(MEM_TRACE, f)) and re.match(kernel+"_trace_[0-9]*\.txt", f)]
    # print("Number of memtraces to be verified: "+str(len(files)))
    if len(files) > max_test_samples:
      samplefiles = np.random.choice(files, size=max_test_samples, replace=False)
    else:
      samplefiles = np.random.choice(files, size=len(files), replace=False)

    matches = 0
    mismatches = 0
    for file in tqdm(samplefiles):
        # os.system('cp '+join(MEM_TRACE, file)+' '+SIMULATOR_KERNEL)
        command = SIMULATOR_HOME+'/src/build/hycube_simulator -x '+str(xdim)+' -y '+str(ydim)+ ' -c '+SIMULATOR_KERNEL+'*.bin -d '+join(MEM_TRACE, file)+' -a '+SIMULATOR_KERNEL+kernel+'_mem_alloc.txt -m ' + str(totalsize)
        print(command)
        os.system(command)
        f = open("sim_result.txt", "r")
        sim_result = f.read()
        sim_result_ = sim_result.split(",")
        sim_result__ = [int(e) for e in sim_result_]
        matches_, mismatches_ = sim_result__
        matches = matches + matches_
        mismatches = mismatches + mismatches_
    print('Matches: %d Mismatches: %d' %(matches,mismatches))  #   
    if mismatches == 0:
     print('Simulation test passed!!!')

  

def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
  csource = sys.argv[1]
  function = sys.argv[2]
  if len(sys.argv) == 4:
    config = sys.argv[3]
    main(csource, function, config)
  else:
    main(csource, function)

