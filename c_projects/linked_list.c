#include <stdio.h>
#include <stdlib.h>

struct node
{
    int data;
    struct node * next;
};

struct node * head = NULL;
int append(int value){
    struct node * n = (struct node *)malloc(sizeof(struct node));
    n->data = value;
    n->next = NULL;

    if (head == NULL){
        head = n;
        return 0;
    }

    struct node * curr = head;
    while (curr->next != NULL) 
    {
        curr = curr->next;
    }
    curr->next = n;
}


void display() {
    struct node * temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main(){

    append(10);
    append(20);
    append(30);

    display();

    return 0;
}
