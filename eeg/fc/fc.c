
#define TVM_EXPORTS

#include "tvm_header.h"
int16_t data[60];
int16_t kernel[240];
int16_t fc[4];// tvm target: c -keys=cpu 
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
  void* arg_fc = (((TVMValue*)args)[2].v_handle);
  int32_t arg_fc_code = arg_type_ids[2];
  // void* data = (((DLTensor*)arg_data)[0].data);
  void* arg_data_shape = (((DLTensor*)arg_data)[0].shape);
  void* arg_data_strides = (((DLTensor*)arg_data)[0].strides);
  int32_t dev_id = (((DLTensor*)arg_data)[0].device.device_id);
  // void* kernel = (((DLTensor*)arg_kernel)[0].data);
  void* arg_kernel_shape = (((DLTensor*)arg_kernel)[0].shape);
  void* arg_kernel_strides = (((DLTensor*)arg_kernel)[0].strides);
  // void* fc = (((DLTensor*)arg_fc)[0].data);
  void* arg_fc_shape = (((DLTensor*)arg_fc)[0].shape);
  void* arg_fc_strides = (((DLTensor*)arg_fc)[0].strides);
  if (!(arg_data_strides == NULL)) {
  }
  if (!(arg_kernel_strides == NULL)) {
  }
  if (!(arg_fc_strides == NULL)) {
  }
  for (int32_t j_outer = 0; j_outer < 4; ++j_outer) {
    for (int32_t j_inner_k_outer_fused_init = 0; j_inner_k_outer_fused_init < 10; ++j_inner_k_outer_fused_init) {
      ((int16_t*)fc)[j_outer] = (int16_t)0;
    }
    for (int32_t j_inner_k_outer_fused = 0; j_inner_k_outer_fused < 10; ++j_inner_k_outer_fused) {
      int32_t cse_var_2 = (j_inner_k_outer_fused * 6);
      int32_t cse_var_1 = ((j_inner_k_outer_fused * 24) + j_outer);
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[cse_var_2] * ((int16_t*)kernel)[cse_var_1]));
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[(cse_var_2 + 1)] * ((int16_t*)kernel)[(cse_var_1 + 4)]));
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[(cse_var_2 + 2)] * ((int16_t*)kernel)[(cse_var_1 + 8)]));
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[(cse_var_2 + 3)] * ((int16_t*)kernel)[(cse_var_1 + 12)]));
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[(cse_var_2 + 4)] * ((int16_t*)kernel)[(cse_var_1 + 16)]));
      ((int16_t*)fc)[j_outer] = (((int16_t*)fc)[j_outer] + (((int16_t*)data)[(cse_var_2 + 5)] * ((int16_t*)kernel)[(cse_var_1 + 20)]));
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
    
    int64_t shape_data[2] = {1,60};
    //int16_t data[60];
    DLDataType type_data;
    type_data.code = (uint8_t)kDLInt;
    type_data.bits = 8;
    type_data.lanes = 1;
    read_int16_data("fc_data.txt", data, 60);
    DLTensor dlt_data;
    create_dl_tensor(&dlt_data, data, 2, type_data, shape_data);
    TVMValue v_data;
    v_data.v_handle = &dlt_data;
    
    // kernel
    
    int64_t shape_kernel[2] = {60,4};
    //int16_t kernel[240];
    DLDataType type_kernel;
    type_kernel.code = (uint8_t)kDLInt;
    type_kernel.bits = 8;
    type_kernel.lanes = 1;
    read_int16_data("fc_kernel.txt", kernel, 240);
    DLTensor dlt_kernel;
    create_dl_tensor(&dlt_kernel, kernel, 2, type_kernel, shape_kernel);
    TVMValue v_kernel;
    v_kernel.v_handle = &dlt_kernel;
    
    // fc
    
    int64_t shape_fc[2] = {1,4};
    //int16_t fc[4];
    DLDataType type_fc;
    type_fc.code = (uint8_t)kDLInt;
    type_fc.bits = 8;
    type_fc.lanes = 1;
    
    DLTensor dlt_fc;
    create_dl_tensor(&dlt_fc, fc, 2, type_fc, shape_fc);
    TVMValue v_fc;
    v_fc.v_handle = &dlt_fc;
    

    TVMValue args[3] = {v_data, v_kernel, v_fc};
    int32_t fake[] = {0,0,0};
    conv_main(args, fake, 3, NULL, NULL, NULL);
    
    // write out tensor
    if (write_int16_data("fc_output.txt", fc, 4) != 0) {
      printf("write data failed");
      return -1;
    }
    
    
    return 0;
}
        
