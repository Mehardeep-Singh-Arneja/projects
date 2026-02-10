
#include <stdio.h>
#include <queue>
#include <string.h>
#include <iostream>
using namespace std;

class Heap{
    public:
    ~Heap(){
        clear();
    }

    class Node{ // node
        public:
        Node* parent = nullptr;
        Node* left = nullptr;
        Node* right = nullptr;

        int data;
        int cust_id;
        Node(int data, int cust_id){
            this->data = data;
            this->cust_id = cust_id;
        }
    };

    private:
    void destroy(Node* n){
        if(!n) return;

        destroy(n->left);
        destroy(n->right);

        delete n; // delete all object to which pointers point to
        return;
    }


    public:

    void clear(){
        destroy(root);
        root = nullptr; // set root to nullptr to reuse later

        while(!q.empty())// empty the q
            q.pop();
    }


    void swap(Node* a){
    while (a->parent && a->data < a->parent->data){
        std::swap(a->data, a->parent->data);
        std::swap(a->cust_id, a->parent->cust_id);
        a = a->parent;
    }
}


    queue<Node*> q; // heap queue
    Node* root = nullptr; // root node

    Node* getRoot(){
        return root;
    }

    void append(int data, int cust_id)
    {
        Node* new_node = new Node(data,cust_id);

        if (!root){
            root = new_node;
            q.push(root);
            return;
        }

        Node* parent = q.front();
        new_node->parent = parent;

        if (!parent->left){
            parent->left = new_node;
        }
        else{
            parent->right = new_node;
            q.pop();              // parent is now full
        }

        q.push(new_node);         // new node may receive children later
        swap(new_node);           // heapify up
    }


    void print()
    {
        if(!root){
            cout << "Heap empty\n";
            return;
        }
        queue<Node*> q2; // print queue
        q2.push(root);

        while (!q2.empty())
        {
            Node* curr = q2.front();
            if (!curr->parent){ 
                cout << "root : " << curr->data << ", customer id : " << curr->cust_id << "\n";
            }else{
                cout << curr->parent->data << "'s child : " << curr->data << ", customer id : " << curr->cust_id << "\n";
            }
            if (curr->left){
                q2.push(curr->left);
            }
            if (curr->right){
                q2.push(curr->right);
            }
            q2.pop();
        }

    }

};

typedef Heap::Node* node; // defining node type

typedef enum order_priority {
    drink = 1,
    burger,
    pizza,
    biriyani,
    tiramisu
} priority;

int calc_alpha(vector<priority> order_list){
    int alpha = 0;
    for (int i = 0; i < order_list.size(); i++)
    {
        alpha += order_list.at(i);
    }
    return alpha;
}

void insert_order(vector<priority> order_list,int cust_id, Heap* heap){

    int alpha = calc_alpha(order_list);
    heap->append(alpha,cust_id);

}

int main()
{
    Heap max; // no pointer

    vector<priority> order1 = {drink,tiramisu};
    insert_order(order1,1,&max);

    vector<priority> order2 = {drink,drink,burger,tiramisu};
    insert_order(order2,2,&max);

    vector<priority> order3 = {burger,pizza,pizza};
    insert_order(order3,3,&max);

    vector<priority> order4 = {burger,burger,burger,drink,drink};
    insert_order(order4,4,&max);

    vector<priority> order5 = {drink,biriyani};
    insert_order(order5,5,&max);

    max.print();
}
