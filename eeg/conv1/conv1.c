
#define TVM_EXPORTS

#include "tvm_header.h"
int16_t data[1575];
int16_t kernel[768];
int16_t conv1[5640];// tvm target: c -keys=cpu 
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
  for (int32_t w_outer = 0; w_outer < 4; ++w_outer) {
    for (int32_t w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init = 0; w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init < 45120; ++w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init) {
      ((int16_t*)conv1)[((((((w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init % 960) / 192) * 1128) + (w_outer * 282)) + ((w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init / 960) * 6)) + ((w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused_init % 192) >> 5))] = (int16_t)0;
    }
    for (int32_t w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused = 0; w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused < 45120; ++w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused) {
      int32_t cse_var_6 = (w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused % 192);
      int32_t cse_var_5 = (w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused / 960);
      int32_t cse_var_4 = ((w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused % 960) / 192);
      int32_t cse_var_3 = (cse_var_6 * 4);
      int32_t cse_var_2 = ((((cse_var_4 * 315) + (w_outer * 47)) + ((w_inner_h_fused_oc_fused_rh_fused_rw_outer_fused & 31) * 4)) + cse_var_5);
      int32_t cse_var_1 = ((((cse_var_4 * 1128) + (w_outer * 282)) + (cse_var_5 * 6)) + (cse_var_6 >> 5));
      ((int16_t*)conv1)[cse_var_1] = (((int16_t*)conv1)[cse_var_1] + (((int16_t*)data)[cse_var_2] * ((int16_t*)kernel)[cse_var_3]));
      ((int16_t*)conv1)[cse_var_1] = (((int16_t*)conv1)[cse_var_1] + (((int16_t*)data)[(cse_var_2 + 1)] * ((int16_t*)kernel)[(cse_var_3 + 1)]));
      ((int16_t*)conv1)[cse_var_1] = (((int16_t*)conv1)[cse_var_1] + (((int16_t*)data)[(cse_var_2 + 2)] * ((int16_t*)kernel)[(cse_var_3 + 2)]));
      ((int16_t*)conv1)[cse_var_1] = (((int16_t*)conv1)[cse_var_1] + (((int16_t*)data)[(cse_var_2 + 3)] * ((int16_t*)kernel)[(cse_var_3 + 3)]));
    }
  }
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
        
