
#define TVM_EXPORTS

#include "tvm_header.h"
#include <math.h>
#include <stdbool.h>
#ifdef __cplusplus
extern "C"
#endif
int8_t data[744];
int8_t kernel[192];
int8_t dwconv2[564];// tvm target: c -keys=cpu 

TVM_DLL int32_t conv_main(void* args, int32_t* arg_type_ids, int32_t num_args, void* out_ret_value, int32_t* out_ret_tcode, void* resource_handle) {
  void* arg_data = (((TVMValue*)args)[0].v_handle);
  int32_t arg_data_code = arg_type_ids[0];
  void* arg_kernel = (((TVMValue*)args)[1].v_handle);
  int32_t arg_kernel_code = arg_type_ids[1];
  void* arg_dwconv2 = (((TVMValue*)args)[2].v_handle);
  int32_t arg_dwconv2_code = arg_type_ids[2];
  // void* data = (((DLTensor*)arg_data)[0].data);
  void* arg_data_shape = (((DLTensor*)arg_data)[0].shape);
  void* arg_data_strides = (((DLTensor*)arg_data)[0].strides);
  int32_t dev_id = (((DLTensor*)arg_data)[0].device.device_id);
  // void* kernel = (((DLTensor*)arg_kernel)[0].data);
  void* arg_kernel_shape = (((DLTensor*)arg_kernel)[0].shape);
  void* arg_kernel_strides = (((DLTensor*)arg_kernel)[0].strides);
  // void* dwconv2 = (((DLTensor*)arg_dwconv2)[0].data);
  void* arg_dwconv2_shape = (((DLTensor*)arg_dwconv2)[0].shape);
  void* arg_dwconv2_strides = (((DLTensor*)arg_dwconv2)[0].strides);
  if (!(arg_data_strides == NULL)) {
  }
  if (!(arg_kernel_strides == NULL)) {
  }
  if (!(arg_dwconv2_strides == NULL)) {
  }
  for (int32_t c_outer = 0; c_outer < 4; ++c_outer) {
    for (int32_t c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused_init = 0; c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused_init < 282; ++c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused_init) {
      ((int8_t*)dwconv2)[(((((c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused_init % 94) >> 1) * 12) + (c_outer * 3)) + (c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused_init / 94))] = (int8_t)0;
    }
    int32_t div_94_i = 0;
    int32_t div_94_j = 0;
    for (int32_t c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused = 0; c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused < 282; ++c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused) {
      #ifdef CGRA_COMPILER  
      please_map_me();
      #endif

      int32_t cse_var_7 = (c_outer * 3);
      // int32_t cse_var_6 = (c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused / 94);
      int32_t cse_var_6 = div_94_i;
      int32_t cse_var_5 = ((c_inner_oh_fused_ow_fused_m_fused_rh_fused_rw_outer_fused & 1) * 96);
      int32_t cse_var_4 = ((div_94_j >> 1) * 12);
      int32_t cse_var_3 = ((cse_var_5 + cse_var_7) + cse_var_6);
      int32_t cse_var_2 = ((cse_var_4 + cse_var_7) + cse_var_6);
      int32_t cse_var_1 = (((cse_var_5 + cse_var_4) + cse_var_7) + cse_var_6);
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[cse_var_1] * ((int8_t*)kernel)[cse_var_3]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 12)] * ((int8_t*)kernel)[(cse_var_3 + 12)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 24)] * ((int8_t*)kernel)[(cse_var_3 + 24)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 36)] * ((int8_t*)kernel)[(cse_var_3 + 36)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 48)] * ((int8_t*)kernel)[(cse_var_3 + 48)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 60)] * ((int8_t*)kernel)[(cse_var_3 + 60)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 72)] * ((int8_t*)kernel)[(cse_var_3 + 72)]));
      ((int8_t*)dwconv2)[cse_var_2] = (((int8_t*)dwconv2)[cse_var_2] + (((int8_t*)data)[(cse_var_1 + 84)] * ((int8_t*)kernel)[(cse_var_3 + 84)]));
      if (div_94_j +1 == 94) {
        div_94_i++;
        div_94_j= 0;
      } else {
        div_94_j++;
      }
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
    
    int64_t shape_data[3] = {1,62,12};
    //int8_t data[744];
    DLDataType type_data;
    type_data.code = (uint8_t)kDLInt;
    type_data.bits = 8;
    type_data.lanes = 1;
    read_int8_data("dwconv2_data.txt", data, 744);
    DLTensor dlt_data;
    create_dl_tensor(&dlt_data, data, 3, type_data, shape_data);
    TVMValue v_data;
    v_data.v_handle = &dlt_data;
    
    // kernel
    
    int64_t shape_kernel[4] = {1,16,12,1};
    //int8_t kernel[192];
    DLDataType type_kernel;
    type_kernel.code = (uint8_t)kDLInt;
    type_kernel.bits = 8;
    type_kernel.lanes = 1;
    read_int8_data("dwconv2_kernel.txt", kernel, 192);
    DLTensor dlt_kernel;
    create_dl_tensor(&dlt_kernel, kernel, 4, type_kernel, shape_kernel);
    TVMValue v_kernel;
    v_kernel.v_handle = &dlt_kernel;
    
    // dwconv2
    
    int64_t shape_dwconv2[4] = {1,47,12,1};
    //int8_t dwconv2[564];
    DLDataType type_dwconv2;
    type_dwconv2.code = (uint8_t)kDLInt;
    type_dwconv2.bits = 8;
    type_dwconv2.lanes = 1;
    
    DLTensor dlt_dwconv2;
    create_dl_tensor(&dlt_dwconv2, dwconv2, 4, type_dwconv2, shape_dwconv2);
    TVMValue v_dwconv2;
    v_dwconv2.v_handle = &dlt_dwconv2;
    

    TVMValue args[3] = {v_data, v_kernel, v_dwconv2};
    int32_t fake[] = {0,0,0};
    conv_main(args, fake, 3, NULL, NULL, NULL);
    
    // write out tensor
    if (write_int8_data("dwconv2_output.txt", dwconv2, 564) != 0) {
      printf("write data failed");
      return -1;
    }
    
    
    return 0;
}
        