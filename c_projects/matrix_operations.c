#include <stdio.h>

void print(int mat1[3][3],int n){
    for (int i = 0; i<n;i++ ){
        for (int z= 0; z<n;z++ ){
        printf("%d ",mat1[i][z]);
        }
        printf("\n");
    }
    printf("\n");
}

void sum(int mat1[3][3],int mat2[3][3],int n,int result[3][3]){ // sum of 2 matrices
    for (int i = 0; i< n;i++){
        for (int y = 0; y< n;y++){
            result[i][y] = mat1[i][y] + mat2[i][y];
        }
    }
}

void mult(int mat1[3][3],int mat2[3][3],int n,int result[3][3]){ // multiplication of 2 matrices
    int c = 0;
    
    for (int i = 0; i< n;i++){
        for (int y = 0; y< n;y++){
            c = 0;
            for (int j = 0;j<n;j++){
               c += mat1[i][j]* mat2[j][y];
            }
            result[i][y] = c;
        }
    }
}

int det(int mat1[3][3]) // determinent of matrix
{
    int c1 = 0,h = 1;
    int min_idx[3][2] = {
        {1,2},
        {0,2},
        {0,1},
    };
    for (int i = 0;i < 3;i++){
        h = (i == 1) ? -1 : 1;
        c1 += h*mat1[0][i]*((mat1[1][min_idx[i][0]]*mat1[2][min_idx[i][1]])-(mat1[1][min_idx[i][1]]*mat1[2][min_idx[i][0]]));
    }
    return c1;
}

void cayley_hamilton(int mat2[3][3]){ // cayley hamilton equation of any 3x3 matrix
    int x =0;
    int det1 = det(mat2);
    int i = 0;
    for (i = 0; i < 3;i++){
        x += mat2[i][i];
    }
    int min[3][2] = {
        {1,2},
        {0,2},
        {0,1},
    };
    int q = 0;
    for (i = 0; i < 3;i++){
        q += mat2[min[i][0]][min[i][0]]*mat2[min[i][1]][min[i][1]] - mat2[min[i][0]][min[i][1]]*mat2[min[i][1]][min[i][0]];
    }

    printf("λ³- (%d)λ² + (%d)λ - (%d) = 0\n",x,q,det1);
}


int main() {
    int matrix1[3][3] = {
        {6,6,3},
        {1,2,3},
        {1,3,4}
    };
    
    int matrix2[3][3] = {
        {2,1,1},
        {0,1,0},
        {1,1,2}
    };

    int matrix3[3][3] = {
        {20,16,17},
        {45,-41,80},
        {51,54,32}
    };
    
    
    // print(matrix1,3);
    // print(matrix2,3);
    int result1[3][3];
    int result2[3][3];
    cayley_hamilton(matrix2);
    cayley_hamilton(matrix3);
    return 0;
}
