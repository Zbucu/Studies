//ALGO2 IS1 212A LAB02
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <sstream>
using namespace std;

template<typename T>

struct Dynamic_Array{
    int rozmiar;
    int max_rozmiar;
    T* wsk;
    Dynamic_Array(){
        wsk = new T[1];
        rozmiar = 0;
        max_rozmiar = 1;
    }
    void dodaj_na_koncu(T ob){
        if(rozmiar!=max_rozmiar)
        {
            *(wsk+rozmiar)=ob;
            rozmiar++;
        }
        else
        {
            T* new_tab = new T[max_rozmiar*2];
            for (int i = 0; i < max_rozmiar; i++)
            {
                *(new_tab + i) = *(wsk + i);
            }
            delete[] wsk;
            wsk = new_tab;
            *(wsk + rozmiar) = ob;
            rozmiar++;
            max_rozmiar=2*max_rozmiar;
        }
    }

    T zwroc(int indeks){
        return wsk[indeks];
    }



    void zamien(int indeks, T ob){
        *(wsk+indeks) = ob;
    }

    void wyczysc(){


        T* new_tab = new T[1];
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
            str<<"element "<<i<<": "<<wsk[i]<<endl;
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
                    T temp = wsk[i+1];
                    wsk[i+1]=wsk[i];
                    wsk[i]=temp;
                    zamiana = 1;

                }
                else{}
            }
        }while(zamiana==1);
    }


};

int main()
{
    Dynamic_Array<int>* l1 = new Dynamic_Array<int>();
    Dynamic_Array<char>* l3 = new Dynamic_Array<char>();
    for(int i=0;i<30;i++)
    {
        l1->dodaj_na_koncu(rand() % 100);
        l3->dodaj_na_koncu('a'+(rand() % 20));
    }

    Dynamic_Array<string>* l2 = new Dynamic_Array<string>();
    l2->dodaj_na_koncu("aaa");
    l2->dodaj_na_koncu("bbb");
    l2->dodaj_na_koncu("ccc");
    cout<<l2->zwroc(0)<<endl<<l2->zwroc(1)<<endl<<l2->zwroc(2)<<endl;

    l2->zamien(2,"zzz");
    cout<<l2->zwroc(0)<<endl<<l2->zwroc(1)<<endl<<l2->zwroc(2)<<endl;

    //cout<<l2[0]<<endl<<l2[1]<<endl;

    //l1->wyczysc();
    string s = l3->to_string(30);
    cout<<s<<endl;
    l3->sortuj();
    s = l3->to_string(30);
    cout<<s<<endl;
    getchar();
}
