#include <iostream>
using namespace std;
#include <queue>


class Node{
    public:
    int data;
    Node* parent = nullptr;
    Node* left = nullptr;
    Node* right = nullptr;
    Node(int data,Node*P = nullptr){
        this->data = data;
        this->parent = P;
    }
};

class Heap{
    private:
    Node* root = nullptr;
    queue<Node*> q;

    void swap(Node* n){
        while (n->parent && n->parent->data > n->data){
            int x = n->parent->data;
            n->parent->data = n->data;
            n->data = x;

            n = n->parent;
        }

    }

    public:

    void printHeap(){
    if (!root){
        cout << "Heap empty\n";
        return;
    }

    queue<Node*> temp;
    temp.push(root);

    int level = 0;

    while (!temp.empty()){
        int size = temp.size();

        cout << "Level " << level++ << ": ";

        for(int i = 0; i < size; i++){
            Node* curr = temp.front();
            temp.pop();

            cout << curr->data << " ";

            if(curr->left) temp.push(curr->left);
            if(curr->right) temp.push(curr->right);
        }
        cout << endl;
    }
}


    void append(int data){

    Node* newNode;

    if (!root){
        root = new Node(data);
        q.push(root);
        return;
    }

    Node* parent = q.front();

    if (!parent->left){
        parent->left = newNode = new Node(data, parent);
        q.push(newNode);
        swap(newNode);
        return;
    }

    if (!parent->right){
        parent->right = newNode = new Node(data, parent);
        q.push(newNode);
        swap(newNode);

        q.pop();
        return;
    }
}
};


int main(){

    Heap ll;
    ll.append(10);
    ll.append(9);
    ll.append(15);
    ll.append(2);
    ll.append(60);
    ll.append(-1);
    ll.append(0);
    ll.append(-5);
    ll.printHeap();

    return 0;
}
