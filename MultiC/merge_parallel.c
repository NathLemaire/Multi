#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <sys/wait.h>

#define N 10000000
#define threads 1


/* UTILITY FUNCTIONS */
/* Function to print an array */
void printArray(int A[], int size)
{
	int i;
    	for (i = 0; i < size; i++)
        	printf("%d ", A[i]);
    	printf("\n");
}

// Merges two subarrays of arr[].
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
void merge(int arr[], int l, int m, int r)
{
	int i, j, k;
	int n1 = m - l + 1;
	int n2 = r - m;

	/* create temp arrays */
	int* L = (int*) malloc(sizeof(int)*n1);
	int* R = (int*) malloc(sizeof(int)*n2);

	/* Copy data to temp arrays L[] and R[] */
	for (i = 0; i < n1; i++)
		L[i] = arr[l + i];
	for (j = 0; j < n2; j++)
		R[j] = arr[m + 1 + j];

	/* Merge the temp arrays back into arr[l..r]*/
	i = 0; // Initial index of first subarray
	j = 0; // Initial index of second subarray
	k = l; // Initial index of merged subarray
	while (i < n1 && j < n2) {
		if (L[i] <= R[j]) {
			arr[k] = L[i];
			i++;
		}
		else {
			arr[k] = R[j];
			j++;
		}
		k++;
	}

	/* Copy the remaining elements of L[], if there
	are any */
	while (i < n1) {
		arr[k] = L[i];
		i++;
		k++;
	}

	/* Copy the remaining elements of R[], if there
	are any */
	while (j < n2) {
		arr[k] = R[j];
		j++;
		k++;
	}
	free(L);
	free(R);
}

/* l is for left index and r is right index of the
sub-array of arr to be sorted */
void mergemator(int arr[], int l, int r, int depth, int sync_depth)
{
	if (l < r) {
		//printf("%d, %d\n", l, r);
		// Same as (l+r)/2, but avoids overflow for
		// large l and h
		int m = l + (r - l) / 2;
		if (depth<sync_depth){
			int f[2];
			pipe(f);
			if (fork()==0){
				mergemator(arr, l, m, depth+1, sync_depth);
				for(int i = l; i < m+1; i++){
  					write(f[1], &arr[i], sizeof(int));
  				}
  				exit(0);
			}else{
				mergemator(arr, m + 1, r, depth+1, sync_depth);
				for(int i = l; i < m+1; i++){
  					read(f[0], &arr[i], sizeof(int));
  				}
  				merge(arr, l, m, r);
			}
			
		}else{
			// Sort first and second halves
			mergemator(arr, l, m, depth+1, sync_depth);
			mergemator(arr, m + 1, r, depth+1, sync_depth);
			merge(arr, l, m, r);
		}
	}
}

int calculate_depth_parallel(int arrsize, int nbthreads){
	int a = log2(nbthreads);
	return a;
}


int check_array(int a[], int array_size){
	for (int i = 1; i < array_size; i++){
        	if(a[i]<a[i-1]){
			return 0;
        	}
        }
        return 1;
}

void merge_sort(int arr[], int array_size){
	mergemator(arr, 0, array_size - 1, 0, calculate_depth_parallel(array_size, threads));
}

/* Driver code */
int main()
{
	int* arr = (int*) malloc(N * sizeof(int));
	int arr_size = N;
        srand(time(NULL));
        for(int i=0;i<arr_size;i++){
                arr[i]=(rand()%100000);
        }
        clock_t t; 
    	t = clock(); 
    	merge_sort(arr, N);
   	t = clock() - t; 
   	double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds 
   	printf("sort took %f seconds to execute \n", time_taken); 
	printf("array: %d \n", check_array(arr, N));
	//printArray(arr, N);
	return 0;
}

