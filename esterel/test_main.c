#include <stdio.h>

void DRIVE_O_o();
void DRIVE_O_o() 
{
  printf("%s", "o");
}

#include "test.c"

int main()
{
  printf("+ Printing . ");
  int i;
  for(i = 0; i < 10; i++)
  {
    DRIVE_I_a();
    DRIVE_I_b();
    DRIVE();
  }
  return 0;
}
