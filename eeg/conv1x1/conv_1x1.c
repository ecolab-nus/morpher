
#define TVM_EXPORTS

#include "tvm_header.h"
int16_t data[564];
int16_t kernel[144];
int16_t conv_1x1[564];// tvm target: c -keys=cpu 
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
  void* arg_conv_1x1 = (((TVMValue*)args)[2].v_handle);
  int32_t arg_conv_1x1_code = arg_type_ids[2];
  // void* data = (((DLTensor*)arg_data)[0].data);
  void* arg_data_shape = (((DLTensor*)arg_data)[0].shape);
  void* arg_data_strides = (((DLTensor*)arg_data)[0].strides);
  int32_t dev_id = (((DLTensor*)arg_data)[0].device.device_id);
  // void* kernel = (((DLTensor*)arg_kernel)[0].data);
  void* arg_kernel_shape = (((DLTensor*)arg_kernel)[0].shape);
  void* arg_kernel_strides = (((DLTensor*)arg_kernel)[0].strides);
  // void* conv_1x1 = (((DLTensor*)arg_conv_1x1)[0].data);
  void* arg_conv_1x1_shape = (((DLTensor*)arg_conv_1x1)[0].shape);
  void* arg_conv_1x1_strides = (((DLTensor*)arg_conv_1x1)[0].strides);
  if (!(arg_data_strides == NULL)) {
  }
  if (!(arg_kernel_strides == NULL)) {
  }
  if (!(arg_conv_1x1_strides == NULL)) {
  }
  for (int32_t j_outer = 0; j_outer < 4; ++j_outer) {
    for (int32_t j_inner_i_fused = 0; j_inner_i_fused < 141; ++j_inner_i_fused) {
      int32_t cse_var_5 = (j_outer * 3);
      int32_t cse_var_4 = (j_inner_i_fused / 47);
      int32_t cse_var_3 = ((j_inner_i_fused % 47) * 12);
      int32_t cse_var_2 = (cse_var_5 + cse_var_4);
      int32_t cse_var_1 = ((cse_var_3 + cse_var_5) + cse_var_4);
      ((int16_t*)conv_1x1)[cse_var_1] = (int16_t)0;
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[cse_var_3] * ((int16_t*)kernel)[cse_var_2]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 1)] * ((int16_t*)kernel)[(cse_var_2 + 12)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 2)] * ((int16_t*)kernel)[(cse_var_2 + 24)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 3)] * ((int16_t*)kernel)[(cse_var_2 + 36)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 4)] * ((int16_t*)kernel)[(cse_var_2 + 48)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 5)] * ((int16_t*)kernel)[(cse_var_2 + 60)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 6)] * ((int16_t*)kernel)[(cse_var_2 + 72)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 7)] * ((int16_t*)kernel)[(cse_var_2 + 84)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 8)] * ((int16_t*)kernel)[(cse_var_2 + 96)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 9)] * ((int16_t*)kernel)[(cse_var_2 + 108)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 10)] * ((int16_t*)kernel)[(cse_var_2 + 120)]));
      ((int16_t*)conv_1x1)[cse_var_1] = (((int16_t*)conv_1x1)[cse_var_1] + (((int16_t*)data)[(cse_var_3 + 11)] * ((int16_t*)kernel)[(cse_var_2 + 132)]));
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
    
    int64_t shape_data[2] = {47,12};
    //int16_t data[564];
    DLDataType type_data;
    type_data.code = (uint8_t)kDLInt;
    type_data.bits = 8;
    type_data.lanes = 1;
    read_int16_data("conv_1x1_data.txt", data, 564);
    DLTensor dlt_data;
    create_dl_tensor(&dlt_data, data, 2, type_data, shape_data);
    TVMValue v_data;
    v_data.v_handle = &dlt_data;
    
    // kernel
    
    int64_t shape_kernel[2] = {12,12};
    //int16_t kernel[144];
    DLDataType type_kernel;
    type_kernel.code = (uint8_t)kDLInt;
    type_kernel.bits = 8;
    type_kernel.lanes = 1;
    read_int16_data("conv_1x1_kernel.txt", kernel, 144);
    DLTensor dlt_kernel;
    create_dl_tensor(&dlt_kernel, kernel, 2, type_kernel, shape_kernel);
    TVMValue v_kernel;
    v_kernel.v_handle = &dlt_kernel;
    
    // conv_1x1
    
    int64_t shape_conv_1x1[2] = {47,12};
    //int16_t conv_1x1[564];
    DLDataType type_conv_1x1;
    type_conv_1x1.code = (uint8_t)kDLInt;
    type_conv_1x1.bits = 8;
    type_conv_1x1.lanes = 1;
    
    DLTensor dlt_conv_1x1;
    create_dl_tensor(&dlt_conv_1x1, conv_1x1, 2, type_conv_1x1, shape_conv_1x1);
    TVMValue v_conv_1x1;
    v_conv_1x1.v_handle = &dlt_conv_1x1;
    

    TVMValue args[3] = {v_data, v_kernel, v_conv_1x1};
    int32_t fake[] = {0,0,0};
    conv_main(args, fake, 3, NULL, NULL, NULL);
    
    // write out tensor
    if (write_int16_data("conv_1x1_output.txt", conv_1x1, 564) != 0) {
      printf("write data failed");
      return -1;
    }
    
    
    return 0;
}
        
