#include<iostream> 
using namespace std;

int* sortArray(int* ptr, int size){
    int *aux=ptr; //copia de apuntador
    int *menor=ptr;
    int *inicio=ptr;
    for(int j=0; j<size+1; j++){
        //Encontrar el menor
        for(int i=j; i<size; i++){
            if(*(aux+i)<*(menor)){
                menor=(aux+i);
            }
        }
        //Lo pasamos hasta adelante
        //cout<<"menor es"<<*menor<<" mover por "<<*inicio;
        int aNum=*inicio;
        //cout<<"guardo "<<aNum;
        *inicio=*menor;
        //cout<<"nuevo inicio"<<*inicio << "y "<<aNum;
        *menor=aNum;
        //cout<<"nuevo menor"<<*menor<<endl;
        //Cambio hecho
        inicio=ptr+j+1;
        menor=inicio;
    }
    /*for(int i=0; i<size; i++){
        cout<<*(aux+i)<<endl;
    }*/
    return ptr;
}


int main(){   //DO NOT change the 'main' signature

    //Fill code here
    int sizep=0;
    cout<<"Enter the size of the array"<<endl;
    cin>>sizep;
    int *array=new int[sizep];
    cout<<"Enter the elements"<<endl;
    for(int i=0; i<sizep; i++){
        cin>>*(array+i);
    }
    //Ordenar
    array=sortArray(array,sizep);
    for(int i=0; i<sizep; i++){
        cout<<*(array+i)<<endl;
    }
}