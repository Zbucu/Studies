//ALGO2 IS1 212A LAB08
//Szymon Buckowski
//bs49220@zut.edu.pl
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

struct Node{
    double x;
    double y;
    Node(){
    }
};

struct Edge{
    int ind_x;
    int ind_y;
    double cost;
    Edge(){
    }
};

struct Union_Find{
    int *tab_p;
    int *tab_r;
    Union_Find(int n)
    {
        tab_p = new int[n];
        tab_r = new int[n];
        for(int i=0;i<n;i++)
        {
            tab_p[i]=i;
            tab_r[i]=0;
        }
    }
    int Find(int x){

        if(x == tab_p[x])
        {
            return x;
        }

        int root = Find(tab_p[x]);
        if(root!=tab_p[x])
        {
            tab_p[x] = root;
        }
        return root;
    }
    void Union(int x,int y){
        if(tab_r[x]<tab_r[y])
        {
            tab_p[x]=y;
        }
        else if(tab_r[x]>tab_r[y])
        {
            tab_p[y]=x;
        }
        else
        {
            if(x<y)
            {
               tab_p[y]=x;
               tab_r[x]++;
            }
            else
            {
                tab_p[x]=y;
                tab_r[y]++;
            }
        }
    }
};

bool compare_edges(Edge e1, Edge e2){
    return(e1.cost<e2.cost);
}

struct Graph{
    Node *tab_N;
    Edge *tab_E;
    int N_Nodes;
    int N_Edges;
    Graph(Node *Node_tab, Edge *Edge_tab,int n_N, int n_E)
    {
        tab_N = Node_tab;
        tab_E = Edge_tab;
        N_Nodes = n_N;
        N_Edges = n_E;
       sort(tab_E, tab_E+N_Edges, compare_edges);
//        for(int i=0;i<N_Edges;i++)
//        {
//            cout<<tab_E[i].cost<<endl;
//        }
    }


};

vector<Edge> Kruskal(Graph graf)
{
    vector<Edge> wynik;
    Union_Find uf(graf.N_Nodes);
    int liczba_unii = 0;
    for(int i=0;i<graf.N_Edges;i++)
    {
        int x_root = uf.Find(graf.tab_E[i].ind_x);
        int y_root = uf.Find(graf.tab_E[i].ind_y);

        if(x_root!=y_root)
        {
            wynik.emplace_back(graf.tab_E[i]);
            uf.Union(graf.tab_E[i].ind_x,graf.tab_E[i].ind_y);
            liczba_unii++;
            if(liczba_unii==graf.N_Nodes-1)
            {
                break;
            }
        }
    }
    return wynik;
}



int main()
{

    string myText;
    ifstream MyReadFile("g2.txt");
    string n_Nodes;
    getline (MyReadFile, n_Nodes);
    Node *Node_tab = new Node[stoi(n_Nodes)];
    for(int i=0;i<stoi(n_Nodes);i++)
    {
        getline (MyReadFile, myText);
        size_t pos = 0;
        std::string token;
        pos = myText.find(" ");
            token = myText.substr(0, pos);
            myText.erase(0, pos + 1);
    Node a;
    a.x=stod(token);
    a.y=stod(myText);
    Node_tab[i]=a;
    }
    string n_Edges;
    getline (MyReadFile, n_Edges);
    Edge *Edge_tab= new Edge[stoi(n_Edges)];
    for(int i=0;i<stoi(n_Edges);i++)
    {
        getline (MyReadFile, myText);
        size_t pos = 0;
        std::string token;
        pos = myText.find(" ");
            token = myText.substr(0, pos);
            myText.erase(0, pos + 1);
    Edge a;
    a.ind_x=stoi(token);
    pos = myText.find(" ");
        token = myText.substr(0, pos);
        myText.erase(0, pos + 1);
    a.ind_y=stoi(token);
    a.cost=stod(myText);
    Edge_tab[i]=a;
    }

    Graph graf(Node_tab,Edge_tab,stoi(n_Nodes),stoi(n_Edges));
    vector<Edge> result = Kruskal(graf);
    double suma = 0;
    for(int i=0;i<result.size();i++)
    {
        cout<<result[i].ind_x<<" "<<result[i].ind_y<<" "<<result[i].cost<<" "<<endl;
        suma+=result[i].cost;
    }
    cout<<suma<<endl;

    getchar();
    return 0;
}
