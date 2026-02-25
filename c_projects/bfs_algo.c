#include <stdio.h>
#define len_queue 50
#define mat_len 20

int arr[mat_len][mat_len] = {
    {0,1,0,1,0,0,0,1,0,1, 0,0,0,1,0,1,0,0,0,1},
{0,1,0,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1,0,1},
{0,0,0,0,0,1,0,0,0,0, 0,1,0,0,0,0,0,1,0,0},
{1,1,1,1,0,1,1,1,1,1, 0,1,1,1,0,1,1,1,0,1},
{0,0,0,1,0,0,0,0,0,1, 0,0,0,1,0,0,0,0,0,1},

{0,1,0,1,1,1,1,1,0,1, 1,1,0,1,1,1,1,1,0,1},
{0,1,0,0,0,0,0,1,0,0, 0,0,0,1,0,0,0,1,0,0},
{0,1,1,1,1,1,0,1,1,1, 1,1,0,1,1,1,0,1,1,1},
{0,0,0,0,0,1,0,0,0,0, 0,1,0,0,0,0,0,1,0,0},
{1,1,1,1,0,1,1,1,1,1, 0,1,1,1,0,1,1,1,2,1},

{0,0,0,1,0,0,0,0,0,1, 0,0,0,1,0,0,0,0,0,1},
{0,1,0,1,1,1,1,1,0,1, 1,1,0,1,1,1,1,1,0,1},
{0,1,0,0,0,0,0,1,0,0, 0,0,0,1,0,0,0,1,0,0},
{0,1,1,1,1,1,0,1,1,1, 1,1,0,1,1,1,0,1,1,1},
{0,0,0,0,0,1,0,0,0,0, 0,1,0,0,0,0,0,1,0,0},

{1,1,1,1,0,1,1,1,1,1, 0,1,1,1,0,1,1,1,0,1},
{0,0,0,1,0,0,0,0,0,1, 0,0,0,1,0,0,0,0,0,1},
{0,1,0,1,1,1,1,1,0,1, 1,1,0,1,1,1,1,1,0,1},
{0,1,0,0,0,0,0,1,0,0, 0,0,0,1,0,0,0,1,0,0},
{0,1,1,1,1,1,0,1,1,1, 1,1,0,1,1,1,0,1,1,2}
};

int print_queue(int queue[len_queue][2],int len){
    if (len == 0){
        printf("queue empty !\n");
        return -1;
    }
    printf("[");
    int i = 0;
    for (i = 0; i < len-1;i++){
        printf("(%d,%d) , ",queue[i][0],queue[i][1]);
    }
    printf("(%d,%d)",queue[i][0],queue[i][1]);
    printf("]\n");
    return 0;
}

void init_queue(int queue[len_queue][2]){
    for (int i = 0; i < len_queue;i++){
        queue[i][0] = -1;
        queue[i][1] = -1;
    }
}

void q_append(int queue[len_queue][2],int *len,int point[2]){
    queue[*len][0] = point[0];
    queue[*len][1] = point[1];
    ++(*len);
}

int membership(int set[len_queue][2],int len,int point[2]){
    if (len == 0){
        printf("set empty !\n");
        return -1;
    }
    for (int i = 0; i< len;i++){
        if (set[i][0] == point[0] && set[i][1] == point[1]){
            return 1;
        }
    }
    return 0;
}

int pop_left(int queue[len_queue][2],int *len,int p[2]){
    if (*len == 0){
        printf("queue empty !\n");
        p[0] = -1; p[1] = -1;
        return -1;
    }

    p[0] = queue[0][0];
    p[1] = queue[0][1];

    for (int i = 0; i < *len - 1; i++){
        queue[i][0] = queue[i+1][0];
        queue[i][1] = queue[i+1][1];
    }

    queue[*len - 1][0] = -1;
    queue[*len - 1][1] = -1;

    --(*len);
    return 1;
}


int bfs(){
    int x = 0,y = 0;        // x = queue length, y = visited length
    int queue[len_queue][2];
    int set[len_queue][2];
    init_queue(queue);
    init_queue(set);

    int point[2] = {0,0};
    q_append(queue,&x,point);
    q_append(set,&y,point);

    int dirs[4][2] = {
        {-1,0},{1,0},{0,-1},{0,1}
    };

    while (x > 0){
        pop_left(queue,&x,point);
        printf("point (%d,%d)\n",point[1]+1,point[0]+1);

        for (int i = 0; i < 4; i++){
            int ny = point[0] + dirs[i][0];
            int nx = point[1] + dirs[i][1];

            // boundary check
            if (ny < 0 || ny >= mat_len || nx < 0 || nx >= mat_len)
                continue;
            if (arr[ny][nx] == 2){ // destination check
                printf("point (%d,%d) -> reached !!\n",nx+1,ny+1);
                return 1;
            }
            if (arr[ny][nx] != 0) // check path
                continue;

            int next[2] = {ny,nx};
            int mem = membership(set,y,next);

            if (mem <= 0){  // not visited
                q_append(set,&y,next);
                q_append(queue,&x,next);
            }
        }
    }
    return 0;
}

int main(){
    bfs();
    return 0;
}
