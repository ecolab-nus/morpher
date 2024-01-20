#include <string.h>
#include <stdio.h>


#define SIZE  8
int C[SIZE*SIZE], B[SIZE*SIZE], C[SIZE*SIZE];
#define C1 10//80
#define R1 4//8
#define C2 10//500
#define R2 C1

int WEIGHT_MATRIX[R1*C1];
int INPUT_MATRIX[R2*C2];
int OUTPUT_MATRIX[R1*C2];
int OUTPUT_MATRIX_EXP[R1*C2];

__attribute__((noinline))
void gemm(){
	int i,j,k,ijk;

        i=0;j=0;k=0;
        for (ijk=0;ijk<R1*C1*C2; ijk++){
          

	   OUTPUT_MATRIX[i*C2+j] += WEIGHT_MATRIX[i*C1+k]* INPUT_MATRIX[k*C2+j];

			if(++k == C1){
				k=0;
				++j;
			}
			if(j == C2){
  				j=0;
				++i;
			}
	}

}

void microspeech_conv_layer(){
	int i,j,k;

	for (i=0;i<R1; i++)
		for (j=0;j<C2; j++)
			for (k=0;k<C1; k++){
				OUTPUT_MATRIX_EXP[i*C2+j] += WEIGHT_MATRIX[i*C1+k]* INPUT_MATRIX[k*C2+j];
			}

}

void main(){

	int i,j;
	for (i=0;i<R1; i++)
		for (j=0; j<C1; j++) {
			WEIGHT_MATRIX[(i)*C1+(j)]= 2*i+1;
		}

	for (i=0;i<R2; i++)
		for (j=0; j<C2; j++) {
			INPUT_MATRIX[(i)*C2+(j)]= i*j+3;
		}


	microspeech_conv_layer();
//microspeech_conv_layer_flattened();
gemm();


	for (i=0;i<R1; i++)
		for (j=0; j<C2; j++) {
			if (OUTPUT_MATRIX[(i)*C2+(j)]!=OUTPUT_MATRIX_EXP[(i)*C2+(j)])
			{
				printf("INCORRECT %d,%d\n",OUTPUT_MATRIX_EXP[(i)*C2+(j)],OUTPUT_MATRIX[(i)*C2+(j)]);
			}else{
				printf("CORRECT %d,%d\n",OUTPUT_MATRIX_EXP[(i)*C2+(j)],OUTPUT_MATRIX[(i)*C2+(j)]);
			}
		}

}


