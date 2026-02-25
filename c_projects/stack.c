#include <stdio.h>
#include <stdlib.h>

typedef struct node{
    int data;
    struct node* next;
    struct node* prev;
} N;

N* head = NULL;

void push(int data){
    N* new_ = (N*)malloc(sizeof(N));

    new_->data = data;
    new_->prev = NULL;
    new_->next = head;

    if (head)
        head->prev = new_;

    head = new_;
}

int pop(){
    if (!head) return -99999;

    N* temp = head;
    int data = head->data;
    head = head->next;

    if (head)
        head->prev = NULL;

    free(temp);
    return data;
}

void print_stack(){
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
    print_stack();
    push(12);
    print_stack();
    push(13);
    print_stack();
    pop();
    print_stack();
    push(23);
    print_stack();
    push(33);
    print_stack();
    pop();
    print_stack();
    pop();
    print_stack();
    push(34);
    print_stack();
    push(555);
    print_stack();
}
