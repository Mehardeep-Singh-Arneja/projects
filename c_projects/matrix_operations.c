#include <stdio.h>

// find cayley hamilton eq , inverse of matrix using cayley hamilton eq, determinant, sum , difference, product of matrices.
// you can also print matrices using print() function neatly.

typedef float mat[3][3];

mat identity = {
    {1,0,0},
    {0,1,0},
    {0,0,1}
};

void print(mat m, int n){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            printf("%0.2f ", m[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void sum(mat A, mat B, int n, mat R){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            R[i][j] = A[i][j] + B[i][j];
        }
    }
}

void diff(mat A, mat B, int n, mat R){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            R[i][j] = A[i][j] - B[i][j];
        }
    }
}

void scalar(mat A, float s, int n, mat R){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            R[i][j] = A[i][j] * s;
        }
    }
}

void mult(mat A, mat B, int n, mat R){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            float c = 0;
            for (int k = 0; k < n; k++){
                c += A[i][k] * B[k][j];
            }
            R[i][j] = c;
        }
    }
}

float det(mat A)
{
    float d = 0;
    d += A[0][0] * (A[1][1]*A[2][2] - A[1][2]*A[2][1]);
    d -= A[0][1] * (A[1][0]*A[2][2] - A[1][2]*A[2][0]);
    d += A[0][2] * (A[1][0]*A[2][1] - A[1][1]*A[2][0]);
    return d;
}

void inverse(mat A, float eq[3], int n, mat R){
    mat A2, xA, qI, temp;
    
    mult(A, A, 3, A2);
    scalar(A, eq[0], 3, xA);
    scalar(identity, eq[1], 3, qI);

    sum(A2, xA, 3, temp);
    sum(temp, qI, 3, R);

    float d = eq[2];

    scalar(R, 1/d, 3, R);
}

void cayley_hamilton(mat A, float eq[3]){
    float trace = A[0][0] + A[1][1] + A[2][2];
    float determinant = det(A);

    int min[3][2] = {
        {1,2},
        {0,2},
        {0,1},
    };
    float q = 0;
    for (int i = 0; i < 3;i++){
        q += A[min[i][0]][min[i][0]]*A[min[i][1]][min[i][1]] - A[min[i][0]][min[i][1]]*A[min[i][1]][min[i][0]];
    }
    eq[0] = -trace;
    eq[1] = q;
    eq[2] = determinant;

    printf("Characteristic eq: λ³ - (%0.2f)λ² + (%0.2f)λ - (%0.2f) = 0\n",
           trace, q, determinant);
}


int main() {

    mat B = {
        {1,0,1},
        {0,1,0},
        {-1,0,1}
    };

    mat diagonal = {
        {1,0,0},
        {0,2,0},
        {0,0,3}
    };

    mat B_1; // B-1
    mat A;mat PD;

    float eq[3];
    cayley_hamilton(B, eq);
    printf("\n");
    inverse(B, eq, 3, B_1);
    mult(B,diagonal,3,PD);
    mult(PD,B_1,3,A);
    print(A,3);

    return 0;
}
