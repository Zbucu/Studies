//ALGO2 IS1 212A LAB06
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <sstream>
#include <cmath>
using namespace std;


template<typename T>

struct Node{
    T pole_1;

    Node(){
    }

    Node(T dane){
        pole_1=dane;
    }
};

template<typename T>

struct Dynamic_Array{
    int rozmiar;
    int max_rozmiar;
    Node<T>* wsk;
    Dynamic_Array(){
        wsk = new Node<T>[1];
        rozmiar = 0;
        max_rozmiar = 1;
    }
    void dodaj_na_koncu(Node<T>* ob){
        if(rozmiar!=max_rozmiar)
        {
            *(wsk+rozmiar)=*ob;
            rozmiar++;
        }
        else
        {
            Node<T>* new_tab = new Node<T>[max_rozmiar*2];
            for (int i = 0; i < max_rozmiar; i++)
            {
                *(new_tab + i) = *(wsk + i);
            }
            delete[] wsk;
            wsk = new_tab;
            *(wsk + rozmiar) = *ob;
            rozmiar++;
            max_rozmiar=2*max_rozmiar;
        }
    }

    Node<T> zwroc(int indeks){
        return wsk[indeks];
    }



    void zamien(int indeks, Node<T> *ob){
        *(wsk+indeks) = *ob;
    }

    void wyczysc(){


        Node<T>* new_tab = new Node<T>[1];
        delete[] wsk;
        wsk = new_tab;
        rozmiar = 0;
        max_rozmiar = 1;
    }

    string to_string(int liczba){
        string out;
        stringstream str;
        str<<"rozmiar tablicy: "<<rozmiar<<endl<<"maksymalny rozmiar tablicy: "<<max_rozmiar<<endl;

        for(int i=0;i<liczba;i++)
        {
            str<<"element "<<i<<": "<<wsk[i].pole_1<<endl;
        }

        out = str.str();
        return out;

    }

    void sortuj(){
        bool zamiana;
        do
        {
            zamiana = 0;
            for(int i=0;i<rozmiar-1;i++)
            {
                if(wsk[i]>wsk[i+1])
                {
                    Node<T> temp = wsk[i+1];
                    wsk[i+1]=wsk[i];
                    wsk[i]=temp;
                    zamiana = 1;

                }
                else{}
            }
        }while(zamiana==1);
    }
};

template<typename T>

struct Binary_Heap{
    Dynamic_Array<T>* tab;

    Binary_Heap(){
        tab = new Dynamic_Array<T>();
    }

    void Przekopcowanie_w_gore(int i){
        if(i!=0)
        {
            int parent = floor((i-1)/2);
            while(tab->wsk[i].pole_1>tab->wsk[parent].pole_1)
            {
                Node<T> temp = tab->wsk[parent];
                tab->wsk[parent] = tab->wsk[i];
                tab->wsk[i] = temp;
                i = parent;
                //parent = floor((i-1)/2);
                Przekopcowanie_w_gore(i);
            }
        }
    }

    void Przekopcowanie_w_dol(int i){
        int left  = 2*i+1;
        int right = 2*i+2;
        while(right<=tab->rozmiar-1 )
        {
            if(tab->wsk[i].pole_1<tab->wsk[left].pole_1 || tab->wsk[i].pole_1<tab->wsk[right].pole_1)
            {
                Node<T> temp = tab->wsk[i];
                if(tab->wsk[left].pole_1>tab->wsk[right].pole_1)
                {
                    tab->wsk[i] = tab->wsk[left];
                    tab->wsk[left] = temp;
                    Przekopcowanie_w_dol(left);
                }
                else
                {
                    tab->wsk[i] = tab->wsk[right];
                    tab->wsk[right] = temp;
                    Przekopcowanie_w_dol(right);
                }

            }
            else
            {
                break;
            }
        }
        if (left<=tab->rozmiar-1 && tab->wsk[i].pole_1<tab->wsk[left].pole_1)
        {
            Node<T> temp = tab->wsk[i];
            tab->wsk[i] = tab->wsk[left];
            tab->wsk[left] = temp;
        }
    }

    void dodaj(Node<T>* ob){
        tab->dodaj_na_koncu(ob);
        Przekopcowanie_w_gore(tab->rozmiar-1);
    }

    Node<T> usun_max(){
        if(tab->rozmiar==0)
        {
            return NULL;
        }
        else
        {
        Node<T> w = tab->zwroc(0);
        tab->wsk[0] = tab->wsk[tab->rozmiar-1];
        tab->wsk[tab->rozmiar-1] = w;
        tab->rozmiar-=1;
        Przekopcowanie_w_dol(0);

        return w;
        }
//        Node<T> w =tab->zwroc(0);
//        Node<T>* new_tab = new Node<T>[tab->max_rozmiar];
//        *new_tab = *(tab->wsk + tab->rozmiar-1);
//        for (int i = 1; i < tab->rozmiar-1; i++)
//        {
//            *(new_tab + i) = *(tab->wsk + i);
//        }
//        delete[] tab->wsk;
//        tab->wsk = new_tab;
//        tab->rozmiar--;

//        int i = 0;
//        Przekopcowanie_w_dol(i);


//        return w;
    }

    void clear(){
        tab->wyczysc();
    }

    string to_string(int liczba){
        return tab->to_string(liczba);
    }


};


int main()
{
    Node<int>* a = new Node<int>(5);
    Node<int>* b = new Node<int>(1);
    Node<int>* c = new Node<int>(14);
    Node<int>* d = new Node<int>(2);
    Node<int>* e = new Node<int>(7);
    Node<int>* f = new Node<int>(9);

    Binary_Heap<int>* b1 = new Binary_Heap<int>();
    b1->dodaj(a);
    b1->dodaj(b);
    b1->dodaj(c);
    b1->dodaj(d);
    b1->dodaj(e);
    cout<<b1->to_string(5)<<endl;
    cout<<b1->usun_max().pole_1<<endl;
    b1->dodaj(f);
    cout<<b1->to_string(5)<<endl;
    b1->clear();

    getchar();
}
