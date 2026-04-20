  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
import re
import numpy as np
from tqdm import tqdm
import logging
import xml.etree.ElementTree as ET
import xmltodict

import scripts.bin_to_trace as BT
from fire import Fire

logging.basicConfig(level=logging.DEBUG)

############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

from pathlib import Path

MORPHER_HOME = Path(os. getcwd())
DFG_GEN_HOME = MORPHER_HOME / 'Morpher_DFG_Generator'
MAPPER_HOME = MORPHER_HOME / 'Morpher_CGRA_Mapper'
SIMULATOR_HOME = MORPHER_HOME / 'hycube_simulator'

class GenFiles: 

  def __init__(self, work_dir : Path, c_file_name : str, func_name : str) -> None:
    self.work_dir = work_dir
    self.c_file_name = Path(c_file_name)
    self.func_name = func_name

    if not (self.work_dir / self.c_file_name).exists():
      logging.error(f"Missing {self.c_file_name}")
    pass

  @property
  def ll_file(self):
    return self.c_file_name.with_suffix(".ll")

  @property
  def opt_ll_file(self): 
    return self.c_file_name.with_suffix(".opt.ll")

  @property
  def opt_instr_ll_file(self): 
    return self.c_file_name.with_suffix(".opt_instrument.ll")

  @property
  def instr_ll_file(self): 
    return  "instrumentation.ll"

  @property
  def libgendfgpass_file(self): 
    return DFG_GEN_HOME / "build/src/libdfggenPass.so"

  @property
  def final_ll(self): 
    return  "final.ll"

  @property
  def final_o(self): 
    return  "final.o"

  @property
  def final_bin(self): 
    return "final"

  @property
  def dfg_xml(self):
    return Path(f"{self.func_name}_PartPredDFG.xml")

  @property
  def dfg_dot(self):
    return Path(f"{self.func_name}_PartPredDFG.dot")

  @property
  def dfg_pdf(self):
    return Path(f"{self.func_name}_PartPredDFG.pdf")

  @property
  def memtrace_dir(self): 
    return Path("memtraces")

  @property
  def memtrace_int16_dir(self): 
    return Path("memtraces_16")

  def memtrace_file(self, i): 
    for f in os.listdir("memtraces"):
      if str(i)+".txt" in f:
        return f"{self.memtrace_dir}/{f}" 

    return ""

  @property
  def mem_alloc(self):
    return Path(f"{self.func_name}_mem_alloc.txt")

  @property
  def mem_alloc_int16(self):
    return Path(f"{self.func_name}_mem_alloc_16.txt")

  @property
  def binary_dir(self):
    return Path("binary")

  @property
  def left_binary(self):
    return Path("left.bin")

  @property
  def right_binary(self):
    return Path("right.bin")

  @property
  def traces(self):
    return Path("traces")

  @property
  def data_dump(self):
    return Path("dataDump")

  @property
  def raw_data_dump(self):
    return "dumped_raw_data.txt"

  def raw_data_dump_i(self, i):
    return self.data_dump / f"dumped_raw_data_{i}.txt"

  @property
  def memfiles(self):
    return Path("mem_files")

def rm_if_exists(f):
  f = Path(f)
  if f.exists():
    cmd(f"rm {f}")


def clear_files(fnames : GenFiles):
  cwd = os.getcwd()
  os.chdir(fnames.work_dir)
  rm_if_exists("*.bin")
  rm_if_exists("binary/*")
  rm_if_exists(f"*{fnames.func_name}*")
  rm_if_exists("*.txt")
  rm_if_exists("memtraces_16/*")
  rm_if_exists("memtraces_8/*")
  os.chdir(cwd)

def cmd(x):
  logging.debug(x)
  res = os.system(x)
  if res != 0:
    exit(-1)

def modify_storeb_to_storeh(xml_file, out_name):
  with open(xml_file) as fp:
    xml_data = fp.read()
    # temporary fix not well-formed code, should fix in xml generation
    xml_data = xml_data.replace("BB=", " BB=")
    xml_data = xml_data.replace("CONST=", " CONST=")
    xml_data = f'<root>{xml_data}</root>'

  root = ET.fromstring(xml_data)
  # Find the <Node> element with specific conditions and change the OP attribute
  for node in root.findall(".//Node"):
      base_pointer_name = node.find(".//BasePointerName")
      if base_pointer_name is not None and base_pointer_name.text == out_name:
          op = node.find(".//OP")
          if op is not None and op.text == "STOREB":
              logging.debug(f"Modify node {str(node)}")
              # Modify the OP attribute
              op.text = "STOREH"

  # # Print the modified XML
  modified_xml = ET.tostring(root, encoding="unicode")
  modified_xml = modified_xml.replace("<root>", "\n").replace("/root", "\n")

  logging.debug(f"Backup old xml file to {xml_file}.back")
  cmd(f"cp {xml_file} {xml_file}.back")

  with open(xml_file, "w") as fp:
    fp.write(modified_xml)


def dfg(fnames):
  if fnames.mem_alloc.exists() and fnames.dfg_xml.exists():
    logging.info(f"Skip generating DFG, {fnames.mem_alloc} and {fnames.dfg_xml} already exist.")
    return

  pwd = os.getcwd()
  os.chdir(fnames.work_dir)
  cmd(f"clang -D CGRA_COMPILER  -c -emit-llvm -O3 -fno-vectorize -fno-slp-vectorize -fno-tree-vectorize -fno-inline -fno-unroll-loops -m32 {fnames.c_file_name} -S -o {fnames.ll_file}")
  cmd(f"opt -gvn -mem2reg -memdep -memcpyopt -lcssa -loop-simplify -licm -disable-slp-vectorization -loop-deletion -indvars -simplifycfg -mergereturn -indvars {fnames.ll_file} -S -o {fnames.opt_ll_file}")
  cmd(f"opt -load {fnames.libgendfgpass_file} -fn conv_main -nobanks 2 -banksize 8192 -skeleton {fnames.opt_ll_file} -S -o {fnames.opt_instr_ll_file}")
  cmd(f"llvm-link {fnames.opt_instr_ll_file} {fnames.instr_ll_file} -o {fnames.final_ll}")
  cmd(f"llc -filetype=obj {fnames.final_ll} -o {fnames.final_o}")
  cmd(f"clang++ -m32  {fnames.final_o} -o {fnames.final_bin}")
  fnames.memtrace_dir.mkdir(parents=True, exist_ok=True)
  cmd(f"cd {fnames.work_dir}; ./final; cd -")
  cmd(f'dot -Tpdf {fnames.dfg_dot} -o {fnames.dfg_pdf}')


  # check output files
  if not fnames.memtrace_dir.exists():
    logging.error("Memtrace not successfully generated!")

  if not fnames.dfg_xml.exists():
    logging.error(f"{fnames.dfg_xml} not successfully generated!")

  # get trace number
  num_memory_traces = len(os.listdir(fnames.memtrace_dir))
  logging.info(f"num_memory_traces number: {num_memory_traces}")

  os.chdir(pwd)
  return num_memory_traces


def check_exists(f):
  if not Path(f).exists():
    logging.error(f"{f} not exists!")
    sys.exit(-1)

def mapping(fnames : GenFiles, start_ll):
    cwd = os.getcwd()
    os.chdir(fnames.work_dir)
    mapper_tool = MAPPER_HOME / "build/src/cgra_xml_mapper"
    check_exists(mapper_tool)

    if Path("*.bin").exists():
      cmd('rm *.bin') 

    fnames.binary_dir.mkdir(parents=True, exist_ok=True)
    
    def _compile(is_left, fnames, start_ll):
      """mapping for left or right, return the II number
      """
      if is_left:
        suffix = ""
      else:
        suffix = "_RC"

      cmd(f'python {MAPPER_HOME}/update_mem_alloc.py {MAPPER_HOME}/json_arch/hycube_original_updatemem{suffix}.json {fnames.mem_alloc} 8192 2 hycube_original_mem{suffix}.json')
      cmd(f'{mapper_tool} -d {fnames.dfg_xml} -x 4 -y 4 -j hycube_original_mem{suffix}.json -i {start_ll} -t HyCUBE_4REG')
      bin_file = None
      for file in os.listdir("./"):
        if file.endswith(".bin") and "II" in file:
          bin_file = file
          match = re.search(r"II=(\d+)", file)
          if match:
            II = int(match.group(1))
          else:
            logging.error("Generating II failed!")

      if is_left:
        cmd(f'mv {bin_file} binary/left.bin')
      else:
        cmd(f'mv {bin_file} binary/right.bin')

      return II
      

    II_left = _compile(True, fnames, start_ll)
    II_right = _compile(False, fnames, start_ll)

    if II_left != II_right:
      sys.exit(f'Left = {II_left} and right = {II_left} II does not match!!')
    
    os.chdir(cwd)
    logging.debug("Mapping finished!")
    return II_left

    
def simulate(fnames : GenFiles, II):
  cwd = os.getcwd()
  os.chdir(fnames.work_dir)

  num_memory_traces = len(os.listdir(fnames.memtrace_dir))
  cmd(f'python {SIMULATOR_HOME}/scripts/duplicate_config.py {fnames.mem_alloc} > dup.log')


  invocation = num_memory_traces
  if num_memory_traces >= 4:
    invocation = num_memory_traces // 4
    half_invocations = num_memory_traces % 4
    

  assert invocation > 0

  fnames.data_dump.mkdir(parents=True, exist_ok=True)

  simu_bin = SIMULATOR_HOME / "src/build/hycube_simulator"
  for i in range(invocation) :
    cmd(f'{simu_bin} duplicated_config.bin {fnames.memtrace_file(i*4)} {fnames.mem_alloc} 8 8 16384 {fnames.memtrace_file(i*4+1)}  {fnames.memtrace_file(i*4+2)} {fnames.memtrace_file(i*4+3)} | tail -n 2 | head -n 1 > output.log')


    with open("output.log", 'r') as fp:
      for line in fp:
        if re.search("Mismatches::0", line):
          success = True
        else:
          success = False

      if not success:
        logging.error("ERROR: FAIL AT MEMTRACE "+ str(i))
        exit(-1)
      else:
        logging.debug("SUCCEED AT MEMTRACE "+ str(i))

    exit(-1)
    cmd(f"mv {fnames.raw_data_dump} {fnames.raw_data_dump_i(i)}")
    BT.dump_trace_full("duplicated_config.bin", fnames.raw_data_dump_i(i), II, 4, fnames.c_file_name)

  os.chdir(cwd)
  logging.debug('\nSimulation done! -> invocations = %d , half invocations = %d ,memory traces=%d\n' % (invocation,half_invocations,num_memory_traces))

def keep_memfiles_int16(fnames : GenFiles):
  # keep memtraces  
  cwd = os.getcwd()
  os.chdir(fnames.work_dir)
  fnames.memtrace_dir.mkdir(parents=True,exist_ok=True)
  fnames.memtrace_int16_dir.mkdir(parents=True,exist_ok=True)
  cmd(f"mv {fnames.mem_alloc} {fnames.mem_alloc_int16}")
  cmd(f"mv {fnames.memtrace_dir}/* {fnames.memtrace_int16_dir}/")
  os.chdir(cwd)

def restore_memfiles_int16(fnames : GenFiles):
  cwd = os.getcwd()
  os.chdir(fnames.work_dir)
  cmd(f"mv {fnames.mem_alloc_int16} {fnames.mem_alloc}")
  cmd(f"mv {fnames.memtrace_int16_dir}/* {fnames.memtrace_dir}/")
  os.chdir(cwd)

def compile(layer):
  def _compile(work_dir, c_file, c_file_int16, func_name, out_tensor, st_ll):
    fnames_int16 = GenFiles(Path(work_dir), c_file_int16, func_name)
    clear_files(fnames_int16)
    dfg(fnames_int16)
    keep_memfiles_int16(fnames_int16)

    fnames = GenFiles(Path(work_dir), c_file, func_name)
    dfg(fnames)
    modify_storeb_to_storeh(fnames.work_dir / fnames.dfg_xml, out_tensor)
    ll = mapping(fnames, st_ll)

    restore_memfiles_int16(fnames)
    simulate(fnames, st_ll)

  _compile(layer[0], layer[1], layer[2], layer[3], layer[4], layer[5])

def compile_int8(layer):
  def _compile(work_dir, c_file, func_name, st_ll):
    fnames = GenFiles(Path(work_dir), c_file, func_name)
    dfg(fnames)
    ll = mapping(fnames, st_ll)
    simulate(fnames, 9)

  _compile(layer[0], layer[1], layer[3], layer[5])

layers = {
  "dwconv1": ["eeg/dwconv1", "dwconv1.c", "dwconv1_int16.c", "conv_main", "dwconv1", 9],
  "dwconv1-new": ["eeg/dwconv1-new", "dwconv1.c", "dwconv1.c", "conv_main", "dwconv1", 3],
  "dwconv1_single": ["eeg/dwconv1", "dwconv1_single.c", "dwconv1_int16_single.c", "conv_main", "dwconv1", 9],
  "dwconv1_single_int8": ["eeg/dwconv1_int8", "dwconv1.c", "dwconv1_int16_single.c", "conv_main", "dwconv1", 9],
  "dwconv2": ["eeg/dwconv2", "dwconv2.c", "dwconv2_int16.c", "conv_main", "dwconv2", 15],
  "conv1": ["eeg/conv1-splitmem", "conv1.c", "conv1.c", "conv_main", "conv1", 15]
}

## int8/int16 is legacy, need refactor this.
def main(name, is_int8 = True):
  if is_int8:
    compile_int8(layers[name])
  else:
    compile(layers[name])

if __name__ == '__main__':
  Fire(main)
