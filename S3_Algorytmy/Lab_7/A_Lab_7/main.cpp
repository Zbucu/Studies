//ALGO2 IS1 212A LAB07
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <sstream>
#include <cmath>
#include <algorithm>
using namespace std;


template<typename T>

struct Node{
    T pole_1;
    Node* previous;
    Node* next;
    Node(){
    }

    Node(T dane){
        pole_1=dane;
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
    void dodaj(Node<T> *ob){
        if(first==NULL)
        {
            first=ob;
            last=ob;
        }
        else
        {
            Node<T> *wsk = first;
            while(wsk!=NULL)
            {
                if(ob->pole_1<wsk->pole_1)
                {
                    if(first==wsk)
                    {
                        first=ob;
                    }
                    else
                    {
                        wsk->previous->next=ob;
                    }
                    ob->previous=wsk->previous;
                    wsk->previous=ob;
                    ob->next=wsk;
                    break;
                }
                else
                {
                    wsk=wsk->next;
                }
            }
            if(wsk==NULL)
            {
                last->next=ob;
                ob->previous=last;
                last=ob;
            }
        }
        rozmiar++;
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
            cout<<"indeks: "<<indeks<<" pole_1: "<<x->pole_1<<endl;
        }
    }
    void zmien_dane(int indeks, T v){
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
            x->pole_1=v;
        }
    }

    Node<T>* wyszukaj(T k){
        auto wsk = first;
        bool znalezione = 0;
        while(wsk!=NULL){
            if(wsk->pole_1==k)
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

    bool wyszukaj_i_usun(T k){
        auto wsk = first;
        bool sukces = 0;
        do{
            if(wsk->pole_1==k)
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

    void wyczysc(){
        while(first!=NULL)
        {
            first->previous=NULL;
            Node<T> *tmp = first->next->next;
            delete first->next;
            delete first;
            first = tmp;
        }
        last=NULL;
        rozmiar = 0;
    }

    string to_string(int liczba){
        string out;
        stringstream str;
        str<<"rozmiar listy: "<<rozmiar<<endl;

        auto x = first;
        for(int i=0;i<liczba;i++)
        {
            str<<"element: "<<i<<" pole_1: "<<x->pole_1<<endl;
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

    Binary_Heap(T *arr, int arr_size){
        tab = new Dynamic_Array<T>();
        for(int i=0;i<arr_size;i++)
        {
            Node<T>* x = new Node<T>(arr[i]);
            dodaj(x);
        }
//        if(td==0)
//        {
//            for(int i=0;i<arr_size;i++)
//            {
//            bottom_up(arr, arr_size,i);
//            }
//        }
//        else
//        {
//            for(int i=0;i<arr_size;i++)
//            {
//            top_down(arr, arr_size, i);
//            }
//        }
    }

    void top_down(T *arr, int arr_size, int i){
        int left = 2*i+1;
        int right = 2*i+2;
        while(right<=arr_size-1)
        {
            if(arr[i]<arr[left] || arr[i]<arr[right])
            {
                T temp = arr[i];
                if(arr[left]>arr[right])
                {
                    arr[i]=arr[left];
                    arr[left]=temp;
                    top_down(arr, arr_size, left);
                }
                else
                {
                    arr[i]=arr[right];
                    arr[right]=temp;
                    top_down(arr, arr_size, right);
                }
            }
            else
            {
                break;
            }
        }
        if(left<=arr_size-1 && left<=arr[arr_size-1] && arr[i]<arr[left])
        {
            T temp=arr[i];
            arr[i]=arr[left];
            arr[left]=temp;
        }
    }

    void bottom_up(T *arr, int arr_size, int i){
        if(i!=0)
        {
            int parent = floor((i-1)/2);
            while(arr[i]>arr[parent])
            {
                T temp=arr[parent];
                arr[parent]=arr[i];
                arr[i]=temp;
                i=parent;
                bottom_up(arr, arr_size, i);
            }
        }
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
                for(int i=0;i<5;i++)
                        {
                            cout<<tab->wsk[i].pole_1<<endl;
                        }
                cout<<endl;
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
//            for(int i=0;i<5;i++)
//                    {
//                        cout<<tab->wsk[i].pole_1<<endl;
//                    }
//            cout<<endl;
        }
        if (left<=tab->rozmiar-1 && tab->wsk[i].pole_1<tab->wsk[left].pole_1 && tab->wsk[i].pole_1<tab->wsk[left].pole_1)
        {
            Node<T> temp = tab->wsk[i];
            tab->wsk[i] = tab->wsk[left];
            tab->wsk[left] = temp;
        }
    }

    void dodaj(Node<T>* ob){
        tab->dodaj_na_koncu(ob);
        Przekopcowanie_w_gore(tab->rozmiar-1);
       // Przekopcowanie_w_dol(0);
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
           // Przekopcowanie_w_dol(0);
            Przekopcowanie_w_gore(tab->rozmiar-1);



            return w;
        }

    }

    void clear(){
        tab->wyczysc();
    }

    string to_string(int liczba){
        return tab->to_string(liczba);
    }



};


void sort_counting(int *B,int rozmiar,int m)
{
    int A[rozmiar];
    memcpy(A,B,sizeof(A));
    int C[m];

    for(int i=0;i<m;i++)
    {
        C[i] = 0;
    }
    for(int i=0;i<rozmiar;i++)
    {
        C[A[i]-1]++;
    }
    for(int i=1;i<m;i++)
    {
        C[i]+=C[i-1];
    }
    for(int i=rozmiar-1;i>=0;i--)
    {
        B[C[A[i]-1]-1]=A[i];
        C[A[i]-1]--;
    }



    //    for(int i=0;i<10;i++)
    //    {
    //        cout<<B[i]<<endl;
    //    }
}


void sort_bucket(int *B, int rozmiar,int m)
{
    int A[rozmiar];
    memcpy(A,B,sizeof(A));
    Lista<int> C[rozmiar];
    double p = (double)m/rozmiar;
    for(int i=0;i<rozmiar;i++)
    {
        int ind = floor(A[i]/p);
        Node<int>* x = new Node<int>(A[i]);
        C[ind].dodaj(x);
    }

    int ind = 0;
    for(int i=0;i<rozmiar;i++)
    {
        Node<int> * wsk= C[i].first;
        while(wsk!=NULL)
        {
            B[ind]=wsk->pole_1;
            ind++;
            wsk=wsk->next;
        }
    }


}
template<typename T>
void sort_bucket(T *B, int rozmiar,int m)
{
    T A[rozmiar];
    memcpy(A,B,sizeof(A));
    Lista<T> C[rozmiar];
    double p = (double)m/rozmiar;
    for(int i=0;i<rozmiar;i++)
    {
        int ind = floor(A[i]/p);
        Node<T>* x = new Node<T>(A[i]);
        C[ind].dodaj(x);
    }

    int ind = 0;
    for(int i=0;i<rozmiar;i++)
    {
        Node<T> * wsk= C[i].first;
        while(wsk!=NULL)
        {
            B[ind]=wsk->pole_1;
            ind++;
            wsk=wsk->next;
        }
    }


}

template<typename T>
void sort_heap(T *arr, int arr_size){
    Binary_Heap<int>* b1 = new Binary_Heap<int>(arr,arr_size);
    for(int i=arr_size;i>0;i--)
    {
        arr[i-1]=b1->usun_max().pole_1;
    }
//    for(int i=arr_size; i > 1; i--)
//    {
//        T temp= arr[0];
//        arr[0]=arr[i-1];
//        arr[i-1]=temp;
//        Binary_Heap<int>* b1 = new Binary_Heap<int>(arr,i-1);
//        for(int i=0;i<5;i++)
//                {
//                    cout<<arr[i]<<endl;
//                }
//        cout<<endl;
//    }
}

int main()
{

    int t[10];
    t[0] = 5;
         t[1] =    1;
            t[2] = 4;
           t[3] =  8;
            t[4] = 0;
//    for(int i=0;i<10;i++)
//    {
//       t[i] = ((rand()<<15) + rand()) % 60;
//    }
    int *tab = t;
//    sort_bucket(tab,10,60);
//    //    sort_counting(tab,10,6);
//        for(int i=0;i<10;i++)
//        {
//            cout<<tab[i]<<endl;
//        }

//        double td[10];
//        for(int i=0;i<10;i++)
//        {
//           td[i] = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/60));;
//        }
//        double *tabd = td;
//        for(int i=0;i<10;i++)
//        {
//            cout<<tabd[i]<<endl;
//        }
//        cout<<endl<<endl;
//        sort_bucket(tabd,10,60);
//        //    sort_counting(tab,10,6);
//            for(int i=0;i<10;i++)
//            {
//                cout<<tabd[i]<<endl;
//            }

    Binary_Heap<int>* b1 = new Binary_Heap<int>(t,10);

    for(int i=0;i<5;i++)
            {
                cout<<tab[i]<<endl;
            }
    cout<<endl<<endl;
    sort_heap(t,5);
    for(int i=0;i<5;i++)
            {
                cout<<tab[i]<<endl;
            }




    getchar();
    return 0;
}
