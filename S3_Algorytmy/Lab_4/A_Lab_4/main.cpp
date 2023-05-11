//ALGO2 IS1 212A LAB04
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

template<typename T>

struct Node{
    T pole_1;
    int poziom;
    Node* parent;
    Node* left;
    Node* right;
    bool red;
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
struct Drzewo_Czerwono_Czarne{
    Node<T>* root;
    int rozmiar;
    Drzewo_Czerwono_Czarne(){
        root = NULL;
        rozmiar = 0;
    }

    void rotate_left(Node<T>* ob){
        Node<T>* temp = ob->parent;
        if(root!=ob)
        {
            if(root==ob->parent)
            {
                root=ob;
            }
            else
            {
                if(ob->parent->parent->right==ob->parent)
                {
                    ob->parent->parent->right=ob;
                }
                else
                {
                    ob->parent->parent->left=ob;
                }
            }
            ob->parent=ob->parent->parent;
            temp->right=ob->left;
            if(ob->left!=NULL)
            {
                ob->left->parent=temp;

            }
            ob->left=temp;
            temp->parent=ob;
        }
    }

    //    void rotate_left(Node<T>* ob){
    //        if(ob->parent->parent!=NULL)
    //        {
    //            if(ob->parent->parent->right == ob->parent)
    //            {
    //                ob->parent->parent->right = ob;
    //            }
    //            else
    //            {
    //                ob->parent->parent->left = ob;
    //            }
    //        }
    //        else
    //        {
    //            root = ob;
    //        }
    //        Node<T>* temp = ob->left;
    //        ob->left = ob->parent;
    //        ob->parent->right = temp;

    //    }

    void rotate_right(Node<T>* ob){
        Node<T>* temp = ob->parent;
        if(root!=ob)
        {
            if(root==ob->parent)
            {
                root=ob;
            }
            else
            {
                if(ob->parent->parent->right==ob->parent)
                {
                    ob->parent->parent->right=ob;
                }
                else
                {
                    ob->parent->parent->left=ob;
                }
                ob->parent=ob->parent->parent;
                temp->left=ob->right;
                if(ob->right!=NULL)
                {
                    ob->right->parent=temp;

                }
            }
            ob->right=temp;
            temp->parent=ob;
        }
    }

    //    void rotate_right(Node<T>* ob){
    //        if(ob->parent->parent!=NULL)
    //        {
    //            if(ob->parent->parent->right == ob->parent)
    //            {
    //                ob->parent->parent->right = ob;
    //            }
    //            else
    //            {
    //                ob->parent->parent->left = ob;
    //            }
    //        }
    //        else
    //        {
    //            root = ob;
    //        }
    //        Node<T>* temp = ob->right;
    //        ob->right = ob->parent;
    //        ob->parent->left = temp;

    //    }

    //    void dodaj(Node<T>* ob){
    //        if(rozmiar==0)
    //        {
    //            root = ob;
    //            root->parent=NULL;
    //            ob->red = 0;
    //        }
    //        else
    //        {
    //            Node<T>* wsk = root;
    //            do
    //            {
    //                if(wsk->pole_1>= ob->pole_1)
    //                {
    //                    if(wsk->left!=NULL)
    //                    {
    //                        wsk=wsk->left;
    //                        ob->poziom++;
    //                    }
    //                    else
    //                    {
    //                        ob->poziom++;
    //                        wsk->left=ob;
    //                        ob->parent=wsk;
    //                        wsk=NULL;
    //                    }
    //                }
    //                else
    //                {
    //                    if(wsk->right!=NULL)
    //                    {
    //                        wsk=wsk->right;
    //                        ob->poziom++;
    //                    }
    //                    else
    //                    {
    //                        ob->poziom++;
    //                        wsk->right=ob;
    //                        ob->parent=wsk;
    //                        wsk=NULL;
    //                    }
    //                }
    //            }while(wsk!=NULL);

    //            ob->red = 1;
    //        }
    //        rozmiar++;

    //    }

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
        ob->red=1;
        Node<T>* x =ob;
        while(root!=x && x->parent->red==1)
        {
            if(x->parent == x->parent->parent->left)
            {
                Node<T>* y=x->parent->parent->right;
                if(y!=NULL && y->red==1)
                {
                    x->parent->red = 0;
                    y->red = 0;
                    x->parent->parent->red = 1;
                    x = x->parent->parent;
                }
                else
                {
                    if(x==x->parent->right)
                    {
                        Node<T>* temp = x->parent;
                        rotate_left(x);
                        x=temp;
                    }
                    if(x->parent!=NULL)
                    {
                        x->parent->red = 0;
                        if(x->parent->parent!=NULL)
                        {
                            x->parent->parent->red = 1;
                        }
                        rotate_right(x->parent);
                    }
                }


            }
            else
            {
                Node<T>* y = x->parent->parent->left;
                if(y!=NULL && y->red==1)
                {
                    x->parent->red = 0;
                    y->red = 0;
                    x->parent->parent->red = 1;
                    x = x->parent->parent;
                }
                else
                {
                    if(x==x->parent->left)
                    {
                        Node<T>* temp = x->parent;
                        rotate_right(x);
                        x=temp;
                    }
                    if(x->parent!=NULL)
                    {
                        x->parent->red = 0;
                        if(x->parent->parent!=NULL)
                        {
                            x->parent->parent->red = 1;
                        }
                        rotate_left(x->parent);
                    }
                }
            }
        }
        root->red = 0;
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
            delete(vec[i]);
        }
        rozmiar=0;
    }

    int wysokosc(){
        vector<Node<T>*> vec;
        scan_preorder(root,vec);
        int n = rozmiar;
        int h = 0;
        for(int i=0;i<n;i++)
        {
            int wys = 0;
            Node<T>* temp = vec[i];
            while(temp!=root)
            {
                temp=temp->parent;
                wys++;

            }
            if(wys>h)
            {
                h=wys;
            }
        }
        return h;
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
            str<<"("<<v[i]->pole_1<<": [p: "<<p<<", l: "<<l<<", r: "<<r<<"], czerwony: "<<v[i]->red<<"),"<<endl;
        }
        str<<"}"<<endl;
        out=str.str();
        return out;
    }

};


int main()
{
    Node<int>* a = new Node<int>(7);
    Node<int>* b = new Node<int>(2);
    Node<int>* c = new Node<int>(14);
    Node<int>* d = new Node<int>(1);
    Node<int>* e = new Node<int>(5);
    Node<int>* f = new Node<int>(8);
    Node<int>* g = new Node<int>(11);
    Node<int>* h = new Node<int>(15);

    Drzewo_Czerwono_Czarne<int>* d1 = new Drzewo_Czerwono_Czarne<int>();
    d1->dodaj(a);
    d1->dodaj(b);
    d1->dodaj(f);
    d1->dodaj(d);
    d1->dodaj(e);
    d1->dodaj(c);
    d1->dodaj(h);
    d1->dodaj(g);

    Node<int>* i = new Node<int>(13);
    d1->dodaj(i);

    Node<int>* j = new Node<int>(17);
    d1->dodaj(j);


    Node<int>* k = new Node<int>(9);
    d1->dodaj(k);

    Node<int>* l = new Node<int>(12);
    d1->dodaj(l);

    vector<Node<int>*> v;
    d1->scan_inorder(d1->root,v);

    for(int i=0;i<v.size();i++)
    {
        cout<<v[i]->pole_1<<", ";
    }

    //d1->wyczysc();
    cout<<endl<<d1->wysokosc()<<endl;
    string s=d1->to_string(d1->rozmiar);
    cout<<s;

    getchar();
}
