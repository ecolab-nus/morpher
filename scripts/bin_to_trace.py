import re
import collections
import subprocess
import sys
import argparse
import os
import os.path

## PYTHON FILE with constants
import scripts.pace_agu_config as HY

def list_to_file(data, name, target):
    length = len(data)

    target.write('#define ' + name.upper() + '_LENGTH ' + str(length) + '\n\n')
    target.write('const unsigned int ' + name + '[' + str(length) + ']' + ' = ' + '{\n')
    for ii in range(int(length)):
        if (ii != length - 1):
            line = '    ' + hex(int(data[ii][0:-1], 2)) + ','  + '\n'
        else:
            line = '    ' + hex(int(data[ii], 2)) + '\n};' + '\n\n'
        target.write(line)

def dump_header(test):
    trace_convert = test + '.h'

    totaldata = open("totaldata.trc","r+")
    totaladdr = open("totaladdr.trc","r+")
    results_expected_file = open("results_expected.trc", "r+")

    addr_list = totaladdr.readlines()
    data_list = totaldata.readlines()
    result_list = results_expected_file.readlines()

    # Check Trace Length
    print('\nNumber of Address : ' + str(len(addr_list)))
    print('Number of Data    : ' + str(len(data_list)))
    print('Number of Result  : ' + str(len(result_list)))

    # Close Trace Files
    totaladdr.close()
    totaldata.close()
    results_expected_file.close()

    # Calculate Trace Length
    trace_register_len = 5
    trace_total_len    = len(addr_list)
    trace_data_len     = len(result_list)
    trace_config_len   = trace_total_len - trace_data_len - trace_register_len
    print('\nLength of Total Memory    :' + str(trace_total_len))
    print('Length of Config Memory   :' + str(trace_config_len))
    print('Length of Data Memory     :' + str(trace_data_len))
    print('Length of Register Memory :' + str(trace_register_len))

    # Slice Trace List
    addr_config_unsort = addr_list[0:trace_config_len]
    addr_data_unsort   = addr_list[trace_config_len:trace_config_len+trace_data_len]
    config_unsort      = data_list[0:trace_config_len]
    data_unsort        = data_list[trace_config_len:trace_config_len+trace_data_len]
    result_unsort      = result_list

    addr_register_unsort = addr_list[-trace_register_len:]
    register_unsort      = data_list[-trace_register_len:]

    # Initialize Sorted List
    addr_config_sort   = []
    addr_data_sort     = []
    config_sort        = []
    data_sort          = []
    result_sort        = []

    addr_register_sort = []
    register_sort      = []

    
    # Covert Config memory
    for ii in range(trace_config_len):
        if ((int(addr_config_unsort[ii], 2) % 4) == 0):
            if (int(addr_config_unsort[0], 2) == int(addr_config_unsort[1], 2) + 2):
                addr_config_sort += [addr_config_unsort[ii]]
                config_sort      += [config_unsort[ii-1][0:-1] + config_unsort[ii]]
            else:
                addr_config_sort += [addr_config_unsort[ii]]
                config_sort      += [config_unsort[ii+1][0:-1] + config_unsort[ii]]

    print('\nLength of Sorted Config Memory Address :' + str(len(addr_config_sort)))
    print('Length of Sorted Config Memory         :' + str(len(config_sort)))
    if HY.DM_WIDTH == 64:
        # Convert Data Memory
        for ii in range(trace_data_len):
            if ((int(addr_data_unsort[ii], 2) % 4) == 0):
                if (int(addr_data_unsort[0], 2) == int(addr_data_unsort[1], 2) + 2):
                    addr_data_sort += [addr_data_unsort[ii]]
                    data_sort      += [data_unsort[ii-1][0:-1] + data_unsort[ii]]
                    result_sort    += [result_unsort[ii-1][0:-1] + result_unsort[ii]]
                else:
                    addr_data_sort += [addr_data_unsort[ii]]
                    data_sort      += [data_unsort[ii+1][0:-1] + data_unsort[ii]]
                    result_sort    += [result_unsort[ii+1][0:-1] + result_unsort[ii]]

    print('\nLength of Sorted Data Memory Address   :' + str(len(addr_data_sort)))
    print('Length of Sorted Data Memory           :' + str(len(data_sort)))
    print('Length of Sorted Results               :' + str(len(result_sort)))

    '''
    print(addr_data_unsort[0], addr_data_unsort[1])
    print(data_unsort[0], data_unsort[1])
    print(addr_data_sort[0], data_sort[0])
    '''

    # Convert Registers
    # print(addr_register_unsort[0], addr_register_unsort[1])
    for ii in range(trace_register_len-1):
        print("ii="+str(ii))
        if ((int(addr_register_unsort[ii], 2) % 4) == 0):
            if (int(addr_register_unsort[0], 2) == int(addr_register_unsort[1], 2) + 2):
                addr_register_sort += [addr_register_unsort[ii]]
                register_sort      += [register_unsort[ii-1][0:-1] + register_unsort[ii]]
            else:
                addr_register_sort += [addr_register_unsort[ii]]
                register_sort      += [register_unsort[ii+1][0:-1] + register_unsort[ii]]
    addr_register_sort += [addr_register_unsort[-1]]
    register_sort      += [register_unsort[-1]]

    print("ADDR:")
    print(addr_register_sort)
    print(register_sort)

    # Write Converted Trace
    with open(trace_convert, 'w+') as header:
        header.write('#ifndef _DEFINE_ARRAY_H\n')
        header.write('#define _DEFINE_ARRAY_H\n\n')

        list_to_file(addr_register_sort, 'addr_reg', header)
        list_to_file(register_sort,      'reg',      header)
        list_to_file(addr_config_sort,   'addr_config',   header)
        list_to_file(config_sort,        'config',        header)
        list_to_file(addr_data_sort,     'addr_data',     header)
        list_to_file(data_sort,          'data',          header)
        list_to_file(result_sort,        'result',        header)

        header.write('#endif\n')

def generate_cm_data_addr(ins_inp, TIMEEXEC):
    
    ###### step 1: split CM instructions by tiles
    num_inst_per_tile = 0
    for cluster in HY.clusters_cm_to_write:
        for i in HY.CLUSTER_ROW_INDEXES[cluster]:
            for j in HY.CLUSTER_COL_INDEXES[cluster]:

                tile_num = (i*HY.TILES_NUM_ROWS) + j  
                os.system("grep -i " + "\"Y=" + str(i) + " " + "X=" + str(j) + "\"" + " " + ins_inp + " >" + " ./mem_files/tile" + str(tile_num) + "_inst.trc")

    ###### step 2: prune instructions, convert 64b to 16b
    for cluster in HY.clusters_cm_to_write:
        for i in HY.CLUSTER_ROW_INDEXES[cluster]:
            for j in HY.CLUSTER_COL_INDEXES[cluster]:
                tile_num = (i*HY.TILES_NUM_ROWS) + j  

                os.system("sed -i " + "\'s/Y=" + str(i) + " " + "X=" + str(j) + ",//\'" + " ./mem_files/tile" + str(tile_num) + "_inst.trc")
               # os.system("grep -c ^" +  " ./mem_files/tile" + str(tile_num) + "_inst.trc")
                #### convert to 16b
                # Construct cmdtorun according to bit widths
                split_iterations = int(HY.CM_WIDTH/HY.DATA_WIDTH)
                cmdtorun = "sed -i \'"
                for x in range(1, split_iterations):
                    if(x!=1):
                        cmdtorun = cmdtorun + ";"
                    cmdtorun = cmdtorun + "s/./&\\n/" + str(x*HY.DATA_WIDTH + (x-1))
                cmdtorun = cmdtorun + "\' ./mem_files/tile" + str(tile_num) + "_inst.trc" 
                os.system(cmdtorun)
    ###### step 3: GENERATE CM binaries
    cmdtorun = "cat "
    for cluster in HY.clusters_cm_to_write:
        for i in HY.CLUSTER_ROW_INDEXES[cluster]:
            for j in HY.CLUSTER_COL_INDEXES[cluster]:
                tile_num = (i*HY.TILES_NUM_ROWS) + j
                cmdtorun = cmdtorun + "./mem_files/tile" + str(tile_num) + "_inst.trc "
    cmdtorun = cmdtorun + "> ./mem_files/ins.trc"

    os.system(cmdtorun)

    cm_addr_file = open("./mem_files/addr_ins.trc","w+")
    if(HY.WRITE_CM):
        addr_mem_type = HY.ADDR_MEM_TYPE_ENCODING["CM"]
        SRAMCELL = int(HY.CM_WIDTH/HY.DATA_WIDTH)

        addr_tile_sel_format = '0' + str(HY.CM_SEL_BITS) + 'b'
        addr_row_sel_format = '0' + str(HY.CM_ROW_SEL_BITS) + 'b'
        addr_byte_sel_format = '0' + str(HY.CM_BYTE_SEL_BITS) + 'b'

        for cluster in HY.clusters_cm_to_write:
            for i in HY.CLUSTER_ROW_INDEXES[cluster]:
                # For each tile
                for j in HY.CLUSTER_COL_INDEXES[cluster]:
                    tile_num = (i*HY.TILES_NUM_ROWS) + j
                    # For each row
                    for k in range(0,TIMEEXEC):
                        # For each byte
                        for l in range(SRAMCELL-1, -1, -1):
                            addr_tile_sel = format(tile_num, addr_tile_sel_format)
                            addr_row_sel = format(k,addr_row_sel_format)
                            addr_byte_sel = format(l,addr_byte_sel_format)

                            totaladdress = HY.ADDR_MSB_ZEROES + addr_mem_type + HY.ADDR_CM_TOP_ZEROES + addr_tile_sel + HY.ADDR_CM_MID1_ZEROES + addr_row_sel + HY.ADDR_CM_MID2_ZEROES + addr_byte_sel + HY.ADDR_CM_LSB_ZEROES
                            cm_addr_file.write(totaladdress + "\n")

    cm_addr_file.close()

def generate_dm_data_addr(data_inp, TIMEEXEC):
    dm_addr_file = open("./mem_files/addr_data.trc","w+")
    dm_data_file = open("./mem_files/data.trc","w+")
    results_expected_file = open("results_expected.trc", "w+")
    dm_src_read_file = open(data_inp,"r")

    if(HY.WRITE_DM):
        addr_mem_type = HY.ADDR_MEM_TYPE_ENCODING["DM"]

        dataToWrite = {}
        dataVal = {}
        dataVal_Ordered = {}
        dataToWrite_backup = {}
        lines_n = []
        lines = dm_src_read_file.readlines()

        print("automate.py [INFO]: DM details  size-> ",len(lines))

        for line in lines:
            allField = line.split(',')
            match = re.match(r"([0-9]+)", allField[0], re.I)
            if(match):
                allField_dm =  int((int(allField[0])//(HY.DATA_WIDTH/8)) // HY.DM_BLOCK_DEPTH) # DM row index // DM depth
                allField_RowandByte = int((int(allField[0])) % (HY.DM_BLOCK_DEPTH * (HY.DATA_WIDTH/8)))
                key1 = 2*allField_dm;
                key2 = 2*allField_dm+1;
                if key1 not in dataToWrite.keys():
                    dataToWrite[key1] = []
                    dataToWrite_backup[key1] = []

                if key2 not in dataToWrite.keys():
                    dataToWrite[key2] = []
                    dataToWrite_backup[key2]= []

                dataToWrite_backup[key1].append(allField_RowandByte)
                dataToWrite_backup[key2].append(allField_RowandByte)

                dataToWrite[key1].append([allField_RowandByte, allField[1], allField[2]])
                dataToWrite[key2].append([allField_RowandByte, allField[1], allField[2]])

        for dm_index in dataToWrite.keys():
            print("automate.py [INFO]: DM details  dm_index-> ",dm_index) 
            dataVal[dm_index] = {}
            dataVal_Ordered[dm_index] = {}

            for custom_range in HY.dmem_range_to_write_zeroes:
                for i in range(custom_range[0], custom_range[1]):
                    if i not in dataToWrite_backup[dm_index]:
                        dataToWrite[dm_index].append([str(i), "0", "0"])

        for dm in dataToWrite:
            for i in dataToWrite[dm]:
                byte = int(i[0])
                row = int(i[0])//2
                if row not in dataVal[dm].keys():
                    dataVal[dm][row] = [0, 0, 0, 0] # [LSB pre-run, LSB post-run, MSB pre-run, MSB post-run]
                if(byte%2):
                    dataVal[dm][row][2] = int(i[1]) # pre-run data (byte)
                    dataVal[dm][row][3] = int(i[2]) # post-run data (byte)
                else:
                    dataVal[dm][row][0] = int(i[1]) # pre-run data (byte)
                    dataVal[dm][row][1] = int(i[2]) # post-run data (byte)

            dataVal_Ordered[dm] = collections.OrderedDict(sorted(dataVal[dm].items()))

        '''
        # After sorting, dataVal_Ordered will be as follows:
        # OrderedDict([(0, [pre-LSB, post-LSB, pre-MSB, post-MSB]), 
        #              (2, [pre-LSB, post-LSB, pre-MSB, post-MSB]),
        #               ...])
        # pre: pre-run data
        # post: post-run data
        '''
        addr_dm_sel_format = '0' + str(HY.DM_SEL_BITS) + 'b'
        addr_row_sel_format = '0' + str(HY.DM_ROW_SEL_BITS) + 'b'
        addr_byte_sel_format = '0' + str(HY.DM_BYTE_SEL_BITS) + 'b'

        for dm in dataToWrite:
            if ((dm %2)==0): 
                bytes_in_curr_row = 0
                addr_dm_sel = format(dm, addr_dm_sel_format)
                print("automate.py [INFO]: Writing to DM ", dm, ", Rows ", min(dataVal_Ordered[dm].keys()), " to ", max(dataVal_Ordered[dm].keys()))
                for i in dataVal_Ordered[dm].keys():
                    bytes_in_curr_row += 2
                    
                    if HY.DM_WIDTH == 64:
                        i = int (i // 4 )# 64 bits in one row
                    
                    addr_row_sel = format(i, addr_row_sel_format)
                    addr_byte_sel = format(0, addr_byte_sel_format)

                    if HY.DM_WIDTH == 64:
                        addr_byte_sel = '' # no need byte selection

                    totaladdress = HY.ADDR_MSB_ZEROES + addr_mem_type + HY.ADDR_DM_TOP_ZEROES + addr_dm_sel + HY.ADDR_DM_MID1_ZEROES + addr_row_sel + HY.ADDR_DM_MID2_ZEROES + addr_byte_sel + HY.ADDR_DM_LSB_ZEROES


                    if HY.DM_WIDTH == 64 and bytes_in_curr_row == 8 :
                        # 64 bit in one row
                        dm_addr_file.write(totaladdress + "\n")
                    elif HY.DM_WIDTH == 16:
                        dm_addr_file.write(totaladdress + "\n")

                    ValinKey = dataVal_Ordered[dm][i]

                    pre_dataLSB = ValinKey[0]
                    post_dataLSB = ValinKey[1]
                    pre_dataMSB = ValinKey[2]
                    post_dataMSB = ValinKey[3]

                    pre_data2file = format(pre_dataMSB,'08b') + format(pre_dataLSB,'08b')
                    post_data2file = format(post_dataMSB,'08b') + format(post_dataLSB,'08b')

                    
                    isNewLine = ""
                    if HY.DM_WIDTH == 64:
                        # if reachs 64 bit(4 bytes), we start a new line
                        if bytes_in_curr_row == 8:
                            isNewLine = "\n"
                            bytes_in_curr_row = 0
                    else:
                        isNewLine = "\n"
                    dm_data_file.write(pre_data2file + isNewLine)
                    results_expected_file.write(post_data2file + isNewLine)
                    if(i==4095):
                        print("automate.py [INFO]: DM details  addr-> ",totaladdress , "MSB ", pre_dataMSB, " LSB ", pre_dataLSB)
    dm_addr_file.close()
    dm_data_file.close()
    results_expected_file.close()

def dump_trace_full(ins_inp,data_inp,TIMEEXEC,no_clusters_on,test):
    generate_cm_data_addr(ins_inp, TIMEEXEC)
    generate_dm_data_addr(data_inp, TIMEEXEC)
    os.system("cat ./mem_files/ins.trc ./mem_files/data.trc > totaldata.trc")
    os.system("cat ./mem_files/addr_ins.trc ./mem_files/addr_data.trc > totaladdr.trc")

    if(HY.WRITE_LUT):
        totaldata = open("totaldata.trc","a+")
        totaladdr = open("totaladdr.trc","a+")
        extraaddr = "1000000000000000000\n1000000000000000010\n1000000000000000100\n1000000000000000110\n"
        extradata = "0000000000001011\n0000000000000000\n0000000000000000\n0000000000000000\n"
        totaldata.write(extradata)
        totaladdr.write(extraaddr)

    if(HY.WRITE_CLUS_EN):
        totaldata = open("totaldata.trc","a+")
        totaladdr = open("totaladdr.trc","a+")
        extraaddr = "1100000000000000000"
    
        clus_en_word = HY.DATA_WIDTH * ['1']

        for cluster in range(no_clusters_on):
            clus_en_word[HY.DATA_WIDTH-1-cluster] = '0'


        extradata = "".join(clus_en_word)
        totaldata.write(extradata)
        totaladdr.write(extraaddr)
        totaladdr.close()
        totaldata.close()

        dump_header(test)


def dump_trace_no_cmem(data_inp,TIMEEXEC,no_clusters_on,test):
    generate_dm_data_addr(data_inp, TIMEEXEC)
    os.system("cat ./mem_files/data.trc > totaldata.trc")
    os.system("cat ./mem_files/addr_data.trc > totaladdr.trc")

    if(HY.WRITE_LUT):
        totaldata = open("totaldata.trc","a+")
        totaladdr = open("totaladdr.trc","a+")
        extraaddr = "1000000000000000000\n1000000000000000010\n1000000000000000100\n1000000000000000110\n"
        extradata = "0000000000001011\n0000000000000000\n0000000000000000\n0000000000000000\n"
        totaldata.write(extradata)
        totaladdr.write(extraaddr)

    if(HY.WRITE_CLUS_EN):
        totaldata = open("totaldata.trc","a+")
        totaladdr = open("totaladdr.trc","a+")
        extraaddr = "1100000000000000000"
    
        clus_en_word = HY.DATA_WIDTH * ['1']

        for cluster in range(no_clusters_on):
            clus_en_word[HY.DATA_WIDTH-1-cluster] = '0'


        extradata = "".join(clus_en_word)
        totaldata.write(extradata)
        totaladdr.write(extraaddr)
        totaladdr.close()
        totaldata.close()

        dump_header(test)


