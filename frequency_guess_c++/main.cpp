//
//  main.cpp
//  trexquan_exercise
//
//  Created by lun zhang on 12/9/16.
//  Copyright © 2016 lun zhang. All rights reserved.
//

#include <iostream>
#include "fstream"
#include "string.h"
#include "vector"
#include "unordered_map"
#include <time.h>
using namespace std;
void hangman_1();
bool helper(string);
void hangman_2();
int MAX_GUESS = 6;
string table = "etaoinshrdlcumwfgypbvkjxqz"; // frequency order
//string table ="abcdefghijklmnopqrstuvwxyz";
int main(int argc, const char * argv[]) {
    
    hangman_2();
    
}



void hangman_1(){
    string s;
    vector<char> missed;
    cout << "./hangman"<<endl;
    cin >> s;
    size_t len = s.size();
    unordered_map<char, vector<int>> tableofword;
    for (int i = 0;i<len;i++){
        tableofword[s[i]].push_back(i);
    }
    vector<string> result (len,"_");
    int count =0;
    int t =0; // the table element select to compare with the element in
    
    for (vector<string>::iterator out = result.begin();out!=result.end(); out++) {
        cout << *out<<" ";
    }
    cout <<"missed:"<<endl;
    
    while (count < MAX_GUESS){
        if (tableofword.empty()){
            return;
        }
        char guess = table[t];
        cout << "guess:" <<guess<<endl;
        if (tableofword.find(guess)!= tableofword.end()) {
            for(auto i:tableofword[guess]){
                result[i] = table[t];
            }
            tableofword.erase(table[t]);
            for (vector<string>::iterator it = result.begin();it != result.end(); it++) {
                cout << *it<<" ";
            }
            cout<<"missed:";
            for (vector<char>::iterator it=missed.begin(); it!=missed.end(); it++) {
                cout << *it<<",";
            }
        } else{
            //cout << "here is one" <<endl;
            count++;
            t++;
            missed.push_back(guess);
            for (vector<string>::iterator it = result.begin();it != result.end(); it++) {
                cout << *it<<" ";
            }
            cout<<"missed:";
            for (vector<char>::iterator it=missed.begin(); it!=missed.end(); it++) {
                cout << *it<<",";
            }
        }
        cout << endl;
        
    }
    
        cout<< endl;
        cout <<"Failed. Guess is more than"<<MAX_GUESS<<"."<<endl;
        
        return;
}

bool helper(string s){
    vector<char> missed;
    size_t len = s.size();
    unordered_map<char, vector<int>> tableofword;
    for (int i = 0;i<len;i++){
        tableofword[s[i]].push_back(i);
    }
    vector<string> result (len,"_");
    int count =0;
    int t =0;
    while (count < MAX_GUESS){
        if (tableofword.empty()){
            return true;
        }
        char guess = table[t];
        if (tableofword.find(guess)!= tableofword.end()) {
            for(auto i:tableofword[guess]){
                result[i] = table[t];
            }
            tableofword.erase(table[t]);
            
        } else{
            count++;
            t++;
            missed.push_back(guess);
        }
        cout << endl;
        
    }
    return false;
}



void hangman_2(){
    clock_t t1,t2;
    t1 = clock();
    int total =0;
    int right = 0;
    string name;
    cout << "Please input the directory of the file"<<endl;
    cin >> name;
    ifstream infile(name);
    //ifstream infile("/Users/lunzhang/Desktop/words_50000.txt");
    //change this to the directory of the txt file
    string s;
    while (infile>>s) {
        total +=1;
        if (helper(s)) {
            right+=1;
        }
        
    }
    t2 = clock();
    float diff ((float)t2-(float)t1);
    float seconds = diff/CLOCKS_PER_SEC;
    cout <<"Number of words tested:" <<total<<endl;;
    cout <<"Number of words guessed correctly:"<<right<<endl;;
    cout <<"Correct Guesses (%)"<<(double) right/total*100<<"%"<<endl;
    cout <<"Time to run: "<<seconds<<"seconds"<<endl;
    
    
    return;
}