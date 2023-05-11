//ALGO2 IS1 212A LAB09
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <fstream>
#include <iomanip>
#include <algorithm>
#include <math.h>
#include <vector>
using namespace std;

struct Point{
    double x;
    double y;
    int numer;
    Point(){
    }
};

bool kmp(Point p1, Point p2){
    double w = (p2.x*p1.y-p1.x*p2.y);
    return(p2.x*p1.y-p1.x*p2.y)<=0;
}

vector<Point> Graham_scan(Point* tab_points, int n_p){
    Point start = tab_points[0];
    for(int i=0;i<n_p;i++)
    {
        if(tab_points[i].y<start.y)
        {
            start=tab_points[i];
        }
        else if(tab_points[i].y==start.y && tab_points[i].x<start.x)
        {
            start=tab_points[i];
        }
    }
    Point tab_nowy[n_p];
    int counter = 0;
    for(int i=0;i<n_p;i++)
    {
        Point a;
        a.x=tab_points[i].x-start.x;
        a.y=tab_points[i].y-start.y;
        a.numer=tab_points[i].numer;
        if(a.x!=0 || a.y!=0)
        {
            tab_nowy[counter] = a;
            counter++;
        }
    }
    sort(tab_nowy, tab_nowy+counter, kmp);
//    cout<<endl;
//    for (int i=0;i<counter;i++)
//    {
//        cout<<tab_nowy[i].x<<" "<<tab_nowy[i].y<<" "<<tab_nowy[i].numer<<endl;
//    }

    vector<Point> wynik;
    wynik.emplace_back(start);
    wynik.emplace_back(tab_nowy[0]);

    for(int i=1;i<counter;i++)
    {
        wynik.emplace_back(tab_nowy[i]);
        Point a;
        Point b;
        do
        {
            if(wynik.size()==3)
            {
                a.x= wynik[wynik.size()-2].x;
                a.y= wynik[wynik.size()-2].y;
            }
            else
            {
            a.x= wynik[wynik.size()-2].x-wynik[wynik.size()-3].x;
            a.y= wynik[wynik.size()-2].y-wynik[wynik.size()-3].y;
            }


            b.x= wynik[wynik.size()-1].x-wynik[wynik.size()-2].x;
            b.y= wynik[wynik.size()-1].y-wynik[wynik.size()-2].y;
            if(kmp(a,b)==false)
            {
                wynik.erase(wynik.begin()+wynik.size()-2);
            }
        }while(kmp(a,b)==false);

    }
    return wynik;

}

int main()
{
    string myText;
    ifstream MyReadFile("points2.txt");
    string n_Points;
    getline (MyReadFile, n_Points);
    Point *Point_tab = new Point[stoi(n_Points)];
    for(int i=0;i<stoi(n_Points);i++)
    {
        getline (MyReadFile, myText);
        size_t pos = 0;
        std::string token;
        pos = myText.find(" ");
        token = myText.substr(0, pos);
        myText.erase(0, pos + 1);
        Point a;
        a.x=stod(token);
        a.y=stod(myText);
        a.numer=i;
        Point_tab[i]=a;
    }
    cout<<setprecision(10);
    //    for (int i=0;i<stoi(n_Points);i++)
    //    {
    //        cout<<Point_tab[i].x<<" "<<Point_tab[i].y<<" "<<Point_tab[i].numer<<endl;
    //    }

    vector<Point> Powloka = Graham_scan(Point_tab,stoi(n_Points));
    cout<<endl;
    for(int i=0;i<Powloka.size();i++)
    {
        cout<<Powloka[i].x<<" "<<Powloka[i].y<<" "<<Powloka[i].numer<<" "<<endl;
        //suma+=result[i].cost;
    }
    return 0;
}
