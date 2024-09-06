
#include <stdint.h>
#include <stdio.h>

typedef enum
{
  /*! \brief CPU device */
  kDLCPU = 1,
  /*! \brief CUDA GPU device */
  kDLCUDA = 2,
  /*!
   * \brief Pinned CUDA CPU memory by cudaMallocHost
   */
  kDLCUDAHost = 3,
  /*! \brief OpenCL devices. */
  kDLOpenCL = 4,
  /*! \brief Vulkan buffer for next generation graphics. */
  kDLVulkan = 7,
  /*! \brief Metal for Apple GPU. */
  kDLMetal = 8,
  /*! \brief Verilog simulator buffer */
  kDLVPI = 9,
  /*! \brief ROCm GPUs for AMD GPUs */
  kDLROCM = 10,
  /*!
   * \brief Pinned ROCm CPU memory allocated by hipMallocHost
   */
  kDLROCMHost = 11,
  /*!
   * \brief Reserved extension device type,
   * used for quickly test extension device
   * The semantics can differ depending on the implementation.
   */
  kDLExtDev = 12,
  /*!
   * \brief CUDA managed/unified memory allocated by cudaMallocManaged
   */
  kDLCUDAManaged = 13,
  /*!
   * \brief Unified shared memory allocated on a oneAPI non-partititioned
   * device. Call to oneAPI runtime is required to determine the device
   * type, the USM allocation type and the sycl context it is bound to.
   *
   */
  kDLOneAPI = 14,
  /*! \brief GPU support for next generation WebGPU standard. */
  kDLWebGPU = 15,
  /*! \brief Qualcomm Hexagon DSP */
  kDLHexagon = 16,
} DLDeviceType;

/*!
 * \brief A Device for Tensor and operator.
 */
typedef struct
{
  /*! \brief The device type used in the device. */
  DLDeviceType device_type;
  /*!
   * \brief The device index.
   * For vanilla CPU memory, pinned memory, or managed memory, this is set to 0.
   */
  int32_t device_id;
} DLDevice;

typedef enum
{
  /*! \brief signed integer */
  kDLInt = 0U,
  /*! \brief unsigned integer */
  kDLUInt = 1U,
  /*! \brief IEEE floating point */
  kDLFloat = 2U,
  /*!
   * \brief Opaque handle type, reserved for testing purposes.
   * Frameworks need to agree on the handle data type for the exchange to be well-defined.
   */
  kDLOpaqueHandle = 3U,
  /*! \brief bfloat16 */
  kDLBfloat = 4U,
  /*!
   * \brief complex number
   * (C/C++/Python layout: compact struct per complex number)
   */
  kDLComplex = 5U,
} DLDataTypeCode;

typedef struct
{
  /*!
   * \brief Type code of base types.
   * We keep it uint8_t instead of DLDataTypeCode for minimal memory
   * footprint, but the value should be one of DLDataTypeCode enum values.
   * */
  uint8_t code;
  /*!
   * \brief Number of bits, common choices are 8, 16, 32.
   */
  uint8_t bits;
  /*! \brief Number of lanes in the type, used for vector types. */
  uint16_t lanes;
} DLDataType;

typedef union
{
  int64_t v_int64;
  double v_float64;
  void *v_handle;
  const char *v_str;
  DLDataType v_type;
  DLDevice v_device;
} TVMValue;

typedef struct
{
  /*!
   * \brief The data pointer points to the allocated data. This will be CUDA
   * device pointer or cl_mem handle in OpenCL. It may be opaque on some device
   * types. This pointer is always aligned to 256 bytes as in CUDA. The
   * `byte_offset` field should be used to point to the beginning of the data.
   *
   * Note that as of Nov 2021, multiply libraries (CuPy, PyTorch, TensorFlow,
   * TVM, perhaps others) do not adhere to this 256 byte aligment requirement
   * on CPU/CUDA/ROCm, and always use `byte_offset=0`.  This must be fixed
   * (after which this note will be updated); at the moment it is recommended
   * to not rely on the data pointer being correctly aligned.
   *
   * For given DLTensor, the size of memory required to store the contents of
   * data is calculated as follows:
   *
   * \code{.c}
   * static inline size_t GetDataSize(const DLTensor* t) {
   *   size_t size = 1;
   *   for (tvm_index_t i = 0; i < t->ndim; ++i) {
   *     size *= t->shape[i];
   *   }
   *   size *= (t->dtype.bits * t->dtype.lanes + 7) / 8;
   *   return size;
   * }
   * \endcode
   */
  void *data;
  /*! \brief The device of the tensor */
  DLDevice device;
  /*! \brief Number of dimensions */
  int32_t ndim;
  /*! \brief The data type of the pointer*/
  DLDataType dtype;
  /*! \brief The shape of the tensor */
  int64_t *shape;
  /*!
   * \brief strides of the tensor (in number of elements, not bytes)
   *  can be NULL, indicating tensor is compact and row-majored.
   */
  int64_t *strides;
  /*! \brief The offset in bytes to the beginning pointer to data */
  uint64_t byte_offset;
} DLTensor;

#define TVM_DLL

void create_dl_tensor(DLTensor *dltensor, void *data, int32_t ndim,
                      DLDataType dtype,
                      int64_t *shape)
{
  dltensor->data = data;
  dltensor->ndim = ndim;
  dltensor->dtype = dtype;
  dltensor->shape = shape;
  dltensor->strides = NULL;
  dltensor->byte_offset = 0;
  dltensor->device.device_id = 0;
  dltensor->device.device_type = kDLCPU;
}

/* int read_int8_data(const char *filename, int8_t *array, int size) */
/* { */
/*   FILE *file = fopen(filename, "rb"); */
/*   if (file == NULL) */
/*   { */
/*     perror("Error opening file"); */
/*     return 1; */
/*   } */

/*   // Read data from file */
/*   size_t elements_read = fread(array, sizeof(int8_t), size, file); */
/*   if (elements_read != size) */
/*   { */
/*     perror("Error reading file"); */
/*     fclose(file); */
/*     return 1; */
/*   } */

/*   fclose(file); */
/*   return 0; */
/* } */

/* int write_int8_data(const char *filename, int8_t *array, int size) */
/* { */
/*   FILE *file = fopen(filename, "wb"); */
/*   if (file == NULL) */
/*   { */
/*     perror("Error opening file"); */
/*     return 1; */
/*   } */

/*   // Write array data to file */
/*   size_t elements_written = fwrite(array, sizeof(int8_t), size, file); */
/*   if (elements_written != size) */
/*   { */
/*     perror("Error writing file"); */
/*     fclose(file); */
/*     return 1; */
/*   } */

/*   // Close the file */
/*   fclose(file); */

/*   printf("Array successfully written to file: %s\n", filename); */
/*   return 0; */
/* } */


#define _WRITE_DATA(TYPE, NAME, FORMAT) \
int write_##NAME##_data(const char *filename, TYPE *array, int size) \
{\
  FILE *file = fopen(filename, "w");\
  if (file == NULL) {\
    perror("Error opening file");\
    return 1;\
  }\
  for (int i = 0; i < size; ++i) { fprintf(file, FORMAT "\n", array[i]);}\
  fclose(file);\
  printf("Array successfully written to file: %s\n", filename);\
  return 0;\
}

_WRITE_DATA(int8_t, int8, "%d")
_WRITE_DATA(uint8_t, uint8, "%d")
_WRITE_DATA(int32_t, int32, "%d")
_WRITE_DATA(uint32_t, uint32, "%ud")
_WRITE_DATA(float, float32, "%f")
_WRITE_DATA(int16_t, int16, "%d")
_WRITE_DATA(uint16_t, uint16, "%ud")


#define _READ_DATA(TYPE, NAME, FORMAT) \
int read_##NAME##_data(const char *filename, TYPE *array, int size) \
{\
  FILE *file = fopen(filename, "r");\
  if (file == NULL) {\
    printf("Error opening file %s", filename);\
    return 1;\
  }\
  for (int i = 0; i < size; ++i) {fscanf(file, FORMAT, &array[i]);} \
  fclose(file);\
  printf("Array successfully read from file: %s\n", filename);\
  return 0;\
}

_READ_DATA(int8_t, int8, "%hhd")
_READ_DATA(uint8_t, uint8, "%hhu")
_READ_DATA(int32_t, int32, "%d")
_READ_DATA(uint32_t, uint32, "%u")
_READ_DATA(float, float32, "%f")
_READ_DATA(int16_t, int16, "%hd")
_READ_DATA(uint16_t, uint16, "%hu")
