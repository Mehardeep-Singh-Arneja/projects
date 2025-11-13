
#include <stdio.h>

#define SIZE 10
int HASH[SIZE];

int hash(int n){
    return (n%SIZE);
}

void init_table(){
    for (int i = 0;i<SIZE;i++){
        HASH[i] = -1;
    }
}

int insert(int n){
    int idx = hash(n);
    if (HASH[idx] == -1)
    {
        HASH[idx] = n;
        return 0;
    }

    int c = idx;
    int re = 0;

    while (HASH[idx] != -1){ // linear probing
        if (idx == c && re != 0){
            printf("Table full! Cannot insert %d\n", n);
            return -1;
        }
        if (idx == SIZE-1)
        {
            idx = 0;
        }
        else
        {
            idx ++;
        }
        re = 1;
    }
    HASH[idx] = n;

    return 0;
}

void main(){
    init_table();
    insert(10);
    insert(17);
    insert(27);
    insert(37);
    insert(57);
    insert(26);
    insert(46);
    insert(77);
    insert(66);
    insert(44);
    insert(5);

    for(int i = 0;i<SIZE;i++){
        printf("%d ",HASH[i]);
    }
} // mehardeep => author
