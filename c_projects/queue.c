#include <stdio.h>
#include <stdlib.h>

typedef struct node{
    int data;
    struct node* next;
    struct node* prev;
} N;

N* head = NULL;
N* tail = NULL;

void push(int data){
    N* new_ = (N*)malloc(sizeof(N));
    new_->data = data;
    new_->prev = tail;
    new_->next = NULL;
    if (!head){
        head = new_;
    }
    if (tail)
        tail->next = new_;
    tail = new_;
}
int pop(){
    if (!head) return -99999;
    N* temp = head;
    int data = head->data;
    head = head->next;
    if (head)
        head->prev = NULL;
    else
        tail = NULL;
    free(temp);
    return data;
}
void print_queue(){
    if (!head){
        printf("Empty\n");
        return;
    }
    N* curr = head;
    while (curr){
        printf("%d ", curr->data);
        curr = curr->next;
    }
    printf("\n");
}

int main(){
    push(10);
    print_queue();
    push(12);
    print_queue();
    push(13);
    print_queue();
    pop();
    print_queue();
    push(23);
    print_queue();
    push(33);
    print_queue();
    pop();
    print_queue();
    pop();
    print_queue();
    push(34);
    print_queue();
    push(555);
    print_queue();
}
