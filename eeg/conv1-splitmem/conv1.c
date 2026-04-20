#include "tvm_header.h"

int16_t data[1575];
int16_t kernel[768];
int16_t conv1[5640];// tvm target: c -keys=cpu

int16_t kernel_shared[768];
int16_t data_shared[870];
int16_t conv1_shared[1410];

#define TVM_EXPORTS


#include <math.h>
#include <stdbool.h>
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t conv_main(void* args, int32_t* arg_type_ids, int32_t num_args, void* out_ret_value, int32_t* out_ret_tcode, void* resource_handle) {
  void* arg_data = (((TVMValue*)args)[0].v_handle);
  int32_t arg_data_code = arg_type_ids[0];
  void* arg_kernel = (((TVMValue*)args)[1].v_handle);
  int32_t arg_kernel_code = arg_type_ids[1];
  void* arg_conv1 = (((TVMValue*)args)[2].v_handle);
  int32_t arg_conv1_code = arg_type_ids[2];
  // void* data = (((DLTensor*)arg_data)[0].data);
  void* arg_data_shape = (((DLTensor*)arg_data)[0].shape);
  void* arg_data_strides = (((DLTensor*)arg_data)[0].strides);
  int32_t dev_id = (((DLTensor*)arg_data)[0].device.device_id);
  // void* kernel = (((DLTensor*)arg_kernel)[0].data);
  void* arg_kernel_shape = (((DLTensor*)arg_kernel)[0].shape);
  void* arg_kernel_strides = (((DLTensor*)arg_kernel)[0].strides);
  // void* conv1 = (((DLTensor*)arg_conv1)[0].data);
  void* arg_conv1_shape = (((DLTensor*)arg_conv1)[0].shape);
  void* arg_conv1_strides = (((DLTensor*)arg_conv1)[0].strides);
  if (!(arg_data_strides == NULL)) {
  }
  if (!(arg_kernel_strides == NULL)) {
  }
  if (!(arg_conv1_strides == NULL)) {
  }
  // void* kernel_shared = TVMBackendAllocWorkspace(1, dev_id, (uint64_t)1536, 0, 16);
  /* if (kernel_shared == NULL) { */
  /*   return -1; */
  /* } */

  for (int32_t ax0 = 0; ax0 < 6; ++ax0) {
    for (int32_t ax2 = 0; ax2 < 128; ++ax2) {
      int32_t cse_var_1 = ((ax0 * 128) + ax2);
      ((int16_t*)kernel_shared)[cse_var_1] = ((int16_t*)kernel)[cse_var_1];
    }
  }
  int32_t w_outer = 0;
  /* for (int32_t w_outer = 0; w_outer < 4; ++w_outer) { */
    // void* data_shared = TVMBackendAllocWorkspace(1, dev_id, (uint64_t)1740, 0, 16);
    /* if (data_shared == NULL) { */
    /*   return -1; */
    /* } */
    // void* conv1_shared = TVMBackendAllocWorkspace(1, dev_id, (uint64_t)2820, 0, 16);
    /* if (conv1_shared == NULL) { */
    /*   return -1; */
    /* } */
    for (int32_t ax0_1 = 0; ax0_1 < 5; ++ax0_1) {
      for (int32_t ax1 = 0; ax1 < 174; ++ax1) {
        ((int16_t*)data_shared)[((ax0_1 * 174) + ax1)] = ((int16_t*)data)[(((ax0_1 * 315) + (w_outer * 47)) + ax1)];
      }
    }
    for (int32_t w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused_init = 0; w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused_init < 45120; ++w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused_init) {
      ((int16_t*)conv1_shared)[(w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused_init >> 5)] = (int16_t)0;
    }

    int32_t mod_192_i = 0;
    int32_t div_192_i = 0, div_192_j= 0;
    int32_t mod_960_i = 0;
    int32_t div_960_i = 0;
    int32_t div_960_j  = 0;

    /////// this function is for cgra
    for (int32_t w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused = 0; w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused < 45120; ++w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused) {
      #ifdef CGRA_COMPILER
      please_map_me();
      #endif
      int32_t cse_var_4 = (w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused >> 5);
      int32_t cse_var_3 = (mod_192_i * 4);
      /* int32_t cse_var_3 = w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused % 192 * 4; */
      /* int32_t cse_var_2 = (((((w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused % 960) / 192) * 174) + ((w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused & 31) * 4)) + (w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused / 960)); */
      int32_t cse_var_2 = (((div_192_i * 174) + ((w_c_h_c_fused_oc_c_fused_rh_fused_rw_outer_fused & 31) * 4)) + div_960_i);
      ((int16_t*)conv1_shared)[cse_var_4] = (((int16_t*)conv1_shared)[cse_var_4] + (((int16_t*)data_shared)[cse_var_2] * ((int16_t*)kernel_shared)[cse_var_3]));
      ((int16_t*)conv1_shared)[cse_var_4] = (((int16_t*)conv1_shared)[cse_var_4] + (((int16_t*)data_shared)[(cse_var_2 + 1)] * ((int16_t*)kernel_shared)[(cse_var_3 + 1)]));
      ((int16_t*)conv1_shared)[cse_var_4] = (((int16_t*)conv1_shared)[cse_var_4] + (((int16_t*)data_shared)[(cse_var_2 + 2)] * ((int16_t*)kernel_shared)[(cse_var_3 + 2)]));
      ((int16_t*)conv1_shared)[cse_var_4] = (((int16_t*)conv1_shared)[cse_var_4] + (((int16_t*)data_shared)[(cse_var_2 + 3)] * ((int16_t*)kernel_shared)[(cse_var_3 + 3)]));

      if(mod_192_i+1 == 192){
        mod_192_i = 0;
      } else {
        mod_192_i++;
      }

      if (div_192_j +1 == 192) {
        div_192_i++;
        div_192_j= 0;
      } else {
        div_192_j++;
      }

      if (mod_960_i + 1 == 960) {
        div_960_i++;
        mod_960_i=0;
        div_192_i=0;
        div_192_j=0;
      } else {
        mod_960_i++;
      }

    }

    for (int32_t w_inner = 0; w_inner < 47; ++w_inner) {
      for (int32_t h = 0; h < 5; ++h) {
        for (int32_t oc = 0; oc < 6; ++oc) {
          ((int16_t*)conv1)[((((h * 1128) + (w_outer * 282)) + (w_inner * 6)) + oc)] = ((int16_t*)conv1_shared)[(((w_inner * 30) + (h * 6)) + oc)];
        }
      }
    }
  /* } */
  return 0;
}

// CodegenC: NOTE: Auto-generated entry function
#ifdef __cplusplus
extern "C"
#endif
TVM_DLL int32_t __tvm_conv_main__(void* args, int* arg_type_ids, int num_args, void* out_ret_value, int* out_ret_tcode, void* resource_handle) {
  return conv_main(args, arg_type_ids, num_args, out_ret_value, out_ret_tcode, resource_handle);
}

int main() {
    // data
    
    int64_t shape_data[3] = {5,315,1};
    //int16_t data[1575];
    DLDataType type_data;
    type_data.code = (uint8_t)kDLInt;
    type_data.bits = 8;
    type_data.lanes = 1;
    read_int16_data("conv1_data.txt", data, 1575);
    DLTensor dlt_data;
    create_dl_tensor(&dlt_data, data, 3, type_data, shape_data);
    TVMValue v_data;
    v_data.v_handle = &dlt_data;
    
    // kernel
    
    int64_t shape_kernel[4] = {6,1,128,1};
    //int16_t kernel[768];
    DLDataType type_kernel;
    type_kernel.code = (uint8_t)kDLInt;
    type_kernel.bits = 8;
    type_kernel.lanes = 1;
    read_int16_data("conv1_kernel.txt", kernel, 768);
    DLTensor dlt_kernel;
    create_dl_tensor(&dlt_kernel, kernel, 4, type_kernel, shape_kernel);
    TVMValue v_kernel;
    v_kernel.v_handle = &dlt_kernel;
    
    // conv1
    
    int64_t shape_conv1[3] = {5,188,6};
    //int16_t conv1[5640];
    DLDataType type_conv1;
    type_conv1.code = (uint8_t)kDLInt;
    type_conv1.bits = 8;
    type_conv1.lanes = 1;
    
    DLTensor dlt_conv1;
    create_dl_tensor(&dlt_conv1, conv1, 3, type_conv1, shape_conv1);
    TVMValue v_conv1;
    v_conv1.v_handle = &dlt_conv1;
    

    TVMValue args[3] = {v_data, v_kernel, v_conv1};
    int32_t fake[] = {0,0,0};
    conv_main(args, fake, 3, NULL, NULL, NULL);
    
    // write out tensor
    if (write_int16_data("conv1_output.txt", conv1, 5640) != 0) {
      printf("write data failed");
      return -1;
    }
    
    
    return 0;
}
