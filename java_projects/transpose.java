public class mehar{
    public static void main(){
        int[][] matrix = {
                {1,2,3,7,6},
                {4,5,6,9,0},
                {7,8,9,5,6},
        };
        int a = matrix.length, b = matrix[0].length;
        int[][] transpose = new int[b][a];

        for (int i = 0; i < matrix.length; i++){
            System.out.print("\n");
            for (int k = 0; k < matrix[0].length; k++){
                System.out.print(matrix[i][k]+"  ");
                transpose[k][i] = matrix[i][k];
            }
        }
        System.out.print("\n\n");
        for (int i = 0; i < transpose.length; i++) {
            System.out.print("\n");
            for (int k = 0; k < transpose[0].length; k++) {
                System.out.print(transpose[i][k] + "  ");
            }
        }
    }
}
