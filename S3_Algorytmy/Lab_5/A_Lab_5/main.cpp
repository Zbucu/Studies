//ALGO2 IS1 212A LAB05
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <sstream>
#include <cmath>
#include <random>
#include <string>
#include <algorithm>
using namespace std;

template<typename T>
struct Node{
    string key;
    T value;
    Node* previous;
    Node* next;

    Node(string k, T v){
        key = k;
        value = v;
        this->previous=NULL;
        this->next=NULL;
    }
};




template<typename T>

struct Lista{
    Node<T>* first;
    Node<T>* last;
    int rozmiar;

    Lista(){
        this->first=NULL;
        this->last=NULL;
        this->rozmiar=0;
    }
    void dodaj_na_koncu(Node<T> *ob){
        if(first==NULL)
        {
            first=ob;
        }
        else
        {
            last->next=ob;
        }
        ob->previous=last;
        ob->next=NULL;
        last=ob;
        rozmiar++;
    }
    void dodaj_na_poczatku(Node<T> *ob){
        if(last==NULL)
        {
            last=ob;
        }
        else
        {
            first->previous=ob;
        }
        ob->next=first;
        first=ob;
        rozmiar++;
    }
    void usun_ostatni(){
        if(last==NULL)
        {
            cout<<"Obiekt nie moze zostac usuniety, poniewaz lista jest pusta"<<endl;
        }
        else
        {
            Node<T>* temp = last->previous;
            delete last;
            last=temp;
            last->next->previous=NULL;
            last->next=NULL;
            rozmiar--;

        }
    }
    void usun_pierwszy(){
        if(first==NULL)
        {
            cout<<"Obiekt nie moze zostac usuniety, poniewaz lista jest pusta"<<endl;
        }
        else
        {
            Node<T>* temp = first->next;
            delete first;
            first=temp;
            first->previous->next=NULL;
            first->previous=NULL;
            rozmiar--;
        }
    }
    void pokaz_dane(int indeks){
        if(indeks<0 || indeks>=rozmiar)
        {
            cout<<"indeks jest poza zakresem"<<endl;
        }
        else
        {
            auto x = first;
            for(int i=0;i<indeks;i++)
            {
                x=x->next;
            }
            cout<<"indeks: "<<indeks<<" pole_1: "<<x->key<<" pole_2: "<<x->value<<endl;
        }
    }
    //    template<typename T>
    void zmien_dane(int indeks, string k, T v){
        if(indeks<0 || indeks>=rozmiar)
        {
            cout<<"indeks jest poza zakresem"<<endl;
        }
        else if(typeid(T)!=typeid(first->value))
        {
            cout<<"Podano bledne dane"<<endl;
        }
        else
        {
            auto x = first;
            for(int i=0;i<indeks;i++)
            {
                x=x->next;
            }
            x->key=k;
            x->value=v;
        }
    }

    Node<T>* wyszukaj(string k){
        auto wsk = first;
        bool znalezione = 0;
        while(wsk!=NULL){
            if(wsk->key==k)
            {
                znalezione = 1;
                break;
            }
            else
            {
                wsk=wsk->next;
            }
        };

        if(znalezione==1)
        {
            return wsk;
        }
        else
        {
            wsk=NULL;
            return wsk;
        }
    }

    bool wyszukaj_i_usun(string k){
        auto wsk = first;
        bool sukces = 0;
        do{
            if(wsk->key==k)
            {
                if(wsk==first)
                {
                    first=wsk->next;
                    wsk->next=NULL;
                    if(first!=NULL)
                    {
                        first->previous=NULL;
                    }
                }
                else if(wsk==last)
                {
                    last=wsk->previous;
                    wsk->previous=NULL;
                    last->next=NULL;
                }
                else
                {
                    wsk->previous->next=wsk->next;
                    wsk->next->previous=wsk->previous;
                    wsk->next=NULL;
                    wsk->previous=NULL;
                }
                sukces=1;
                rozmiar--;
                break;
            }
            else
            {
                wsk=wsk->next;
            }
        }while(wsk!=NULL);

        return sukces;
    }

    void dodaj(int indeks,T *ob){
        if(indeks<0 || indeks>=rozmiar)
        {
            cout<<"indeks jest poza zakresem"<<endl;
        }
        else
        {
            auto x = first;
            for(int i=0;i<indeks;i++)
            {
                x=x->next;
            }
            if(x==first)
            {
                dodaj_na_poczatku(ob);
            }
            else
            {
                // auto temp = x->previous;
                x->previous->next=&ob;
                ob->previous=x->previous;
                ob->next=x;
                x->previous=&ob;
            }
        }
    }
    void wyczysc(){
        while(first!=NULL)
        {
            first->previous=NULL;
            first->next=NULL;
            first=first->next;
            rozmiar--;

        }
        last=NULL;
    }

    string to_string(int liczba){
        string out;
        stringstream str;
        str<<"rozmiar listy: "<<rozmiar<<endl;

        auto x = first;
        for(int i=0;i<liczba;i++)
        {
            str<<"element: "<<i<<" key: "<<x->key<<" value: "<<x->value<<endl;
            x=x->next;
        }

        out = str.str();
        return out;

    }


};

template<typename T>

struct Dynamic_Array{
    int rozmiar;
    int max_rozmiar;
    Lista<T>* wsk;
    Dynamic_Array(){
        wsk = new Lista<T>[4];
        rozmiar = 0;
        max_rozmiar = 4;
    }
    void dodaj_na_koncu(Lista<T>* ob){
        if(rozmiar<0.75*max_rozmiar)
        {
            *(wsk+rozmiar)=*ob;
            rozmiar++;
        }
        else
        {
            powieksz();
            *(wsk + rozmiar) = *ob;
            rozmiar++;
            max_rozmiar=2*max_rozmiar;
        }
    }

    void powieksz(){
        Lista<T>* new_tab = new Lista<T>[max_rozmiar*2];
        for (int i = 0; i < max_rozmiar; i++)
        {
            *(new_tab + i) = *(wsk + i);
        }
        delete[] wsk;
        wsk = new_tab;
        max_rozmiar=2*max_rozmiar;
    }

    Lista<T> zwroc(int indeks){
        return wsk[indeks];
    }



    void zamien(int indeks, Lista<T> *ob){
        *(wsk+indeks) = *ob;
    }

    void wyczysc(){


        Lista<T>* new_tab = new Lista<T>[1];
        delete[] wsk;
        wsk = new_tab;
        rozmiar = 0;
        max_rozmiar = 1;
    }

    //    string to_string(int liczba){
    //        string out;
    //        stringstream str;
    //        str<<"rozmiar tablicy: "<<rozmiar<<endl<<"maksymalny rozmiar tablicy: "<<max_rozmiar<<endl;

    //        for(int i=0;i<liczba;i++)
    //        {
    //            str<<"element "<<i<<": "<<wsk[i].pole_1<<endl;
    //        }

    //        out = str.str();
    //        return out;

    //    }

    //    void sortuj(){
    //        bool zamiana;
    //        do
    //        {
    //            zamiana = 0;
    //            for(int i=0;i<rozmiar-1;i++)
    //            {
    //                if(wsk[i]>wsk[i+1])
    //                {
    //                    Node<T> temp = wsk[i+1];
    //                    wsk[i+1]=wsk[i];
    //                    wsk[i]=temp;
    //                    zamiana = 1;

    //                }
    //                else{}
    //            }
    //        }while(zamiana==1);
    //    }
};


template<typename T>
struct Hash_Table{
    Dynamic_Array<T>* tab;

    Hash_Table(){
        tab = new Dynamic_Array<T>();
    }

    void dodaj(Node<T>* ob){
        if(ob!=NULL)
        {
            Node<T>* x = wyszukaj(ob->key);

            if(x!=NULL)
            {
                x->value = ob->value;
            }
            else
            {
                if(tab->rozmiar<0.75*tab->max_rozmiar)
                {
                    int index = hash_function(ob->key);
                    tab->wsk[index].dodaj_na_koncu(ob);
                    tab->rozmiar++;
                }
                else
                {
                    rehash();
                    int index = hash_function(ob->key);
                    tab->wsk[index].dodaj_na_koncu(ob);
                    tab->rozmiar++;
                }

//                            Lista<T>* l = new Lista<T>;
//                            l->dodaj_na_koncu(ob);
//                            tab->dodaj_na_koncu(l);
            }
        }
    }

    Node<T>* wyszukaj(string k){
        int ind = hash_function(k);
        if(tab->wsk[ind].rozmiar!=0)
                    {
                        Node<T>* x = tab->wsk[ind].wyszukaj(k);
                        if(x!=NULL)
                        {
                            return x;
                        }
                    }
        return NULL;

    }

    bool usun(string k){
        int ind = hash_function(k);
        {
            if(tab->wsk[ind].rozmiar!=0)
            {
                bool x = tab->wsk[ind].wyszukaj_i_usun(k);
                if(x==1)
                {
                    tab->rozmiar--;
                    return 1;
                }
            }

        }
        return 0;
    }

    void clear(){
        tab->wyczysc();
    }

    string to_string(){
        string out;
        stringstream str;
        str<<"rozmiar tablicy: "<<tab->rozmiar<<endl<<"maksymalny rozmiar tablicy: "<<tab->max_rozmiar<<endl;

        for(int i=0;i<tab->max_rozmiar;i++)
        {
            Node<T>* x = tab->wsk[i].first;
            if(x!=NULL)
            {
                str<<"element "<<i<<": "<<x->key<<" -> "<<x->value;
                x=x->next;

                while(x!=NULL)
                {
                    str<<", "<<x->key<<" -> "<<x->value;
                    x=x->next;
                }
                str<<";"<<endl;
            }

        }

        out = str.str();
        return out;
    }

    int hash_function(string k){
        int w = 0;
        for(int i=0;i<k.length();i++)
        {
            w+= char(k[i])*pow(31,k.length()-i-1);
        }
        return abs(w)%tab->max_rozmiar;

    }

    void rehash(){
        Lista<T> new_tab[tab->max_rozmiar*2];
        Lista<T>* new_tab1 = new Lista<T>[tab->max_rozmiar*2];
        int temp = tab->max_rozmiar;
        tab-> max_rozmiar=2*tab->max_rozmiar;
        for (int i = 0; i < temp; i++)
        {

            new_tab[i] = *(tab->wsk + i);
            //tab->wsk[i].wyczysc();



        }

        tab->wyczysc();
        tab-> max_rozmiar=2*temp;
        tab->wsk = new_tab1;


        for (int i = 0; i < temp; i++)
        {
            Node<T>* x = (new_tab + i)->first;
            while(x!=NULL)
            {
                Node<T>* temp = x->next;
                dodaj(x);
                x=temp;
            }
        }

    }




};



std::string random_string()
{
    std::string str("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");

    std::random_device rd;
    std::mt19937 generator(rd());

    random_shuffle(str.begin(), str.end());

    return str.substr(6, 16);
}

int main()
{

    Node<int>* a = new Node<int>("a",1);
    Node<int>* b = new Node<int>("b",2);
    Node<int>* c = new Node<int>("c",3);
    Node<int>* d = new Node<int>("d",4);
    Node<int>* e = new Node<int>("e",5);

    Hash_Table<int>* h1 = new Hash_Table<int>();
    h1->dodaj(a);
    h1->dodaj(b);
    h1->dodaj(c);
    h1->dodaj(d);
    h1->dodaj(e);

    for(int i=0;i<20;i++)
    {
        string s = random_string();
        Node<int> *wsk = new Node<int>(s,rand() % 100);
        h1->dodaj(wsk);
    }

    //cout<<h1->wyszukaj("d")->key<<": "<<h1->wyszukaj("d")->value<<endl;
    cout<< h1->usun("c")<<endl;
    // cout<<h1->wyszukaj("d")->key<<": "<<h1->wyszukaj("d")->value<<endl;
    cout<<h1->to_string();
    cout<<endl<<h1->wyszukaj("e")->key<<h1->wyszukaj("e")->value<<endl;



    getchar();
}
