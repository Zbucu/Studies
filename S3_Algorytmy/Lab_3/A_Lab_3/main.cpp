//ALGO2 IS1 212A LAB03
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <algorithm>
#include <vector>
#include <sstream>
#include <string>
using namespace std;

template<typename T>

struct Node{
    T pole_1;
    int poziom;
    Node* parent;
    Node* left;
    Node* right;
    Node(){
        parent=NULL;
        left=NULL;
        right=NULL;
        poziom=0;
    }
    Node(T dane){
        pole_1=dane;
        parent=NULL;
        left=NULL;
        right=NULL;
        poziom=0;
    }
};

template<typename T>
struct Drzewo_BST{
    Node<T>* root;
    int rozmiar;
    Drzewo_BST(){
        root = NULL;
        rozmiar = 0;
    }
    void dodaj(Node<T>* ob){
        if(rozmiar==0)
        {
            root = ob;
            root->parent=NULL;
        }
        else
        {
            Node<T>* wsk = root;
            do
            {
                if(wsk->pole_1>= ob->pole_1)
                {
                    if(wsk->left!=NULL)
                    {
                        wsk=wsk->left;
                        ob->poziom++;
                    }
                    else
                    {
                        ob->poziom++;
                        wsk->left=ob;
                        ob->parent=wsk;
                        wsk=NULL;
                    }
                }
                else
                {
                    if(wsk->right!=NULL)
                    {
                        wsk=wsk->right;
                        ob->poziom++;
                    }
                    else
                    {
                        ob->poziom++;
                        wsk->right=ob;
                        ob->parent=wsk;
                        wsk=NULL;
                    }
                }
            }while(wsk!=NULL);


        }
        rozmiar++;
    }

    Node<T>* szukaj(T dane){
        Node<T>* wsk = root;
        while(wsk!=NULL)
        {
            if(wsk->pole_1==dane)
            {
                return wsk;
            }
            else if(wsk->pole_1>dane)
            {
                wsk=wsk->left;
            }
            else
            {
                wsk=wsk->right;
            }
        }
        return NULL;
    }

    void usun(Node<T>* wsk){


        if(wsk->left==NULL && wsk->right==NULL) //lisc
        {
            if(wsk==root)
            {
                root=NULL;
            }
            else
            {
                if(wsk->parent->pole_1>=wsk->pole_1)
                {
                    wsk->parent->left=NULL;
                }
                else
                {
                    wsk->parent->right=NULL;
                }
            }

            delete wsk;
            rozmiar--;
        }
        else if(wsk->left==NULL || wsk->right==NULL) //wezel 1 stopnia
        {
            if(wsk->left==NULL)
            {
                Node<T>* temp = wsk->right;
                if(wsk!=root)
                {
                    temp->parent=wsk->parent;
                    if(temp->parent->pole_1>=temp->pole_1)
                    {
                        temp->parent->left=temp;
                    }
                    else
                    {
                        temp->parent->right=temp;
                    }
                }
                else
                {
                    root = temp;
                }
                delete wsk;
                rozmiar--;
            }
            if(wsk->right==NULL)
            {
                Node<T>* temp = wsk->left;
                if(wsk!=root)
                {
                    temp->parent=wsk->parent;
                    if(temp->parent->pole_1>=temp->pole_1)
                    {
                        temp->parent->left=temp;
                    }
                    else
                    {
                        temp->parent->right=temp;
                    }
                }
                else
                {
                    root = temp;
                }
                delete wsk;
                rozmiar--;
            }
        }
        else                                    //wezel drugiego stopnia
        {
            Node<T>* poprzednik = wsk->left;
            while(poprzednik->right!=NULL)
            {
                poprzednik = poprzednik->right;
            }

            if(poprzednik->left!=NULL)
            {
                Node<T>* temp = poprzednik->left;
                temp->parent=poprzednik->parent;
                if(poprzednik->parent!=wsk)
                {
                    poprzednik->parent->right=temp;
                }
            }
            else
            {
                if(poprzednik->parent->left==poprzednik)
                {
                    poprzednik->parent->left = NULL;
                }
                if(poprzednik->parent->right==poprzednik)
                {
                    poprzednik->parent->right = NULL;
                }
                //      if()
                //   }
            }

            if(poprzednik->parent!=wsk)
            {
                poprzednik->left = wsk->left;
            }
            poprzednik->right = wsk->right;
            if(poprzednik->left!=NULL)
            {
                poprzednik->left->parent=poprzednik;
            }
            if(poprzednik->left!=NULL)
            {
                poprzednik->right->parent=poprzednik;
            }
            if(wsk==root)
            {
                poprzednik->parent=NULL;
                root=poprzednik;
            }
            else
            {
                poprzednik->parent=wsk->parent;
                if(poprzednik->parent->pole_1>=poprzednik->pole_1)
                {
                    poprzednik->parent->left=poprzednik;
                }
                else
                {
                    poprzednik->parent->right=poprzednik;
                }
            }
            delete wsk;
            rozmiar--;
        }

    }

    void scan_preorder(Node<T>* wsk,vector<Node<T>*> &vec){
        if(wsk!=NULL)
        {

            vec.emplace_back(wsk);
            scan_preorder(wsk->left,vec);
            scan_preorder(wsk->right,vec);
        }
    }

    void scan_inorder(Node<T>* wsk,vector<Node<T>*> &vec){
        if(wsk!=NULL)
        {
            scan_inorder(wsk->left,vec);
            vec.emplace_back(wsk);
            scan_inorder(wsk->right,vec);
        }
    }
    void wyczysc(){
        vector<Node<T>*> vec;
        scan_preorder(root,vec);
        int n = rozmiar;
        for(int i=0;i<n;i++)
        {
            usun(vec[i]);
        }
    }

    int wysokosc(){
        vector<Node<T>*> vec;
        scan_preorder(root,vec);
        int n = rozmiar;
        int w = 0;
        for(int i=0;i<n;i++)
        {
            if(vec[i]->poziom>w)
            {
                w = vec[i]->poziom;
            }
        }
        return w;
    }

    string to_string(int liczba){
        string out;
        stringstream str;
        str<<"rozmiar drzewa: "<<rozmiar<<endl<<"wysokosc drzewa: "<<wysokosc()<<endl<<"{"<<endl;
        vector<Node<int>*> v;
        scan_preorder(root,v);
        for(int i=0;i<liczba;i++)
        {
            string p;
            string l;
            string r;
            if(v[i]->parent==NULL)
            {
                p="NULL";
            }
            else
            {
                p = std::to_string(v[i]->parent->pole_1);
            }
            if(v[i]->left==NULL)
            {
                l="NULL";
            }
            else
            {
                l = std::to_string(v[i]->left->pole_1);
            }
            if(v[i]->right==NULL)
            {
                r="NULL";
            }
            else
            {
                r = std::to_string(v[i]->right->pole_1);
            }
            str<<"("<<v[i]->pole_1<<": [p: "<<p<<", l: "<<l<<", r: "<<r<<"], poziom: "<<v[i]->poziom<<"),"<<endl;
        }
        str<<"}"<<endl;
        out=str.str();
        return out;
    }

};

int main()
{
    //    Node<int>* a = new Node<int>(15);
    //    Node<int>* b = new Node<int>(24);
    //    Node<int>* c = new Node<int>(10);

    Drzewo_BST<int>* d1 = new Drzewo_BST<int>();
    //    d1->dodaj(a);
    //    d1->dodaj(b);
    //    d1->dodaj(c);

    int n[30] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30};
    random_shuffle(n, n + 30);
    for(int i=0;i<30;i++)
    {
        Node<int> *wsk = new Node<int>(n[i]);
        d1->dodaj(wsk);
        cout<<n[i]<<endl;
    }

    Node<int> *aaa = d1->szukaj(20);
    cout<<aaa->pole_1<<endl;

    //d1->usun(d1->szukaj(13));
    vector<Node<int>*> v;
    d1->scan_preorder(d1->root,v);


    for(int i=0;i<v.size();i++)
    {
        cout<<v[i]->pole_1<<", ";
    }
    //    d1->usun(d1->szukaj(13));
    //    d1->usun(d1->szukaj(2));
    //    d1->usun(d1->szukaj(27));
    //    d1->usun(d1->szukaj(26));
    // d1->wyczysc();

    cout<<endl<<d1->wysokosc()<<endl;
    string s=d1->to_string(30);
    cout<<s;
    getchar();
}
