void foo() {
   int array[10];
   int i = get();
   // i = 9;
   if (i > 8 && i <= length(array)) {
       array[i] = 1;  // defect: array[10] overflow
   }
   array[i] = 1;  // defect: array[10] overflow
}

int bad(int x) {
	x = 0;
	// lack of return
}
