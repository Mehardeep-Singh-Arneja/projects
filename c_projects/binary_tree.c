#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node {
    struct node *left;
    struct node *right;
    char name[10];
    int age;
} Node;


Node * append(Node * parent_node,char * name,int age,int node_number){
    Node * new = (Node *)malloc(sizeof(Node));
    new->left = NULL;
    new->right = NULL;
    strcpy(new->name,name);
    new->age = age;

    if (node_number == 1){
        parent_node->left = new;
    }
    else if (node_number == 2){
        parent_node->right = new;
    }
    return new;
}

void inorder(Node *root, int depth) {
    if (root == NULL)
        return;

    printf("Level %d : %s (%d)\n", depth, root->name, root->age);
    inorder(root->left, depth + 1);
    inorder(root->right, depth + 1);
}


int main() {
    
    Node *root = malloc(sizeof(Node));

    root->left = NULL;
    root->right = NULL;
    strcpy(root->name, "john");
    root->age = 18;

    Node * mariana = append(root, "mariana", 18, 1);
    Node * jade =  append(root, "jade", 20, 2);

    Node * robin = append(mariana, "robin", 17, 1);
    Node * steve = append(mariana, "steve", 19, 2);

    inorder(root, 0);

    return 0;
}
