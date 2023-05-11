//ALGO2 IS1 212A LAB01
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <string>
#include <sstream>
#include <time.h>
using namespace std;

template<typename T, typename U>

struct Node{
    T pole_1;
    U pole_2;
    Node* previous;
    Node* next;
    Node(){
        this->previous=NULL;
        this->next=NULL;
    }
};

template<typename T>
struct Lista{
    T* first;
    T* last;
    int rozmiar;

    Lista(){
        this->first=NULL;
        this->last=NULL;
        this->rozmiar=0;
    }

    void dodaj_na_koncu(T *ob){
        if(first==NULL)
        {
            first=ob;
        }
        else
        {
            last->next=ob;
        }
        ob->previous=last;
        last=ob;
        rozmiar++;
    }
    void dodaj_na_poczatku(T &ob){
        if(last==NULL)
        {
            last=&ob;
        }
        else
        {
            first->previous=&ob;
        }
        ob.next=first;
        first=&ob;
        rozmiar++;
    }
    void usun_ostatni(){
        if(last==NULL)
        {
            cout<<"Obiekt nie moze zostac usuniety, poniewaz lista jest pusta"<<endl;
        }
        else
        {
            T* temp = last;
            delete temp;
            last=last->previous;
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
            first=first->next;
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
            cout<<"indeks: "<<indeks<<" pole_1: "<<x->pole_1<<" pole_2: "<<x->pole_2<<endl;
        }
    }
    template<typename U, typename W>
    void zmien_dane(int indeks, U p1, W p2){
        if(indeks<0 || indeks>=rozmiar)
        {
            cout<<"indeks jest poza zakresem"<<endl;
        }
        else if(typeid(U)!=typeid(first->pole_1) || typeid(W)!=typeid(first->pole_2))
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
            x->pole_1=p1;
            x->pole_2=p2;
        }
    }
    template<typename U, typename W>
    T* wyszukaj(U p1, W p2){
        auto wsk = first;
        bool znalezione = 0;
        do{
            if(wsk->pole_1==p1 && wsk->pole_2==p2)
            {
                znalezione = 1;
                break;
            }
            else
            {
                wsk=wsk->next;
            }
        }while(wsk!=NULL);

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

    template<typename U, typename W>
    bool wyszukaj_i_usun(U p1, W p2){
        auto wsk = first;
        bool sukces = 0;
        do{
            if(wsk->pole_1==p1 && wsk->pole_2==p2)
            {
                if(wsk==first)
                {
                    first=wsk->next;
                    wsk->next=NULL;
                    first->previous=NULL;
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

    void dodaj(int indeks,T &ob){
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
                ob.previous=x->previous;
                ob.next=x;
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
            str<<"element: "<<i<<" pole_1: "<<x->pole_1<<" pole_2: "<<x->pole_2<<endl;
            x=x->next;
        }

        out = str.str();
        return out;

    }


};

int main()
{

    //    Obiekt<int, char> a;
    //    a.pole_1=7;
    //    a.pole_2='a';
    Lista<Node<int,char>>* l1 = new Lista<Node<int,char>>();
    l1->usun_ostatni();

    clock_t t1 = clock();
    //    l1->dodaj_na_koncu(a);


    //    Obiekt<int, char> b;
    //    b.pole_1=100;
    //    b.pole_2='z';
    //    l1->dodaj_na_koncu(b);

    Node<int, char> c;
    c.pole_1=20;
    c.pole_2='o';
    l1->dodaj(1,c);

    for(int i=0;i<1000;i++)
    {
        Node<int,char> *wsk = new Node<int,char>;
        wsk->pole_1 = rand() % 100;
        int ch= rand() % 70;
        wsk->pole_2 = 'a'+ch;
        l1->dodaj_na_koncu(wsk);
    }
    // l1->usun_ostatni();
    //l1->zmien_dane(1,1,'b');
    // auto fl=l1->wyszukaj_i_usun(1000,'z');
    //l1->wyczysc();

    string s=l1->to_string(40);
    cout<<s;
    clock_t t2 = clock();
    double time = (t2-t1)/(double)CLOCKS_PER_SEC;
    cout<<time<<endl;






    return 0;
}
