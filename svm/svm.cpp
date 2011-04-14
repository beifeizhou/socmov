#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <cassert>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <sstream>
#define f(i, n)             for(int i = 0; i < n; i++)
#define s(n)				scanf("%d",&n)
#define sc(n)               scanf("%s", &n)   
#define pb					push_back 
#define VB					vector <bool>
using namespace std;

class svm
{
	public:
	static const int n = 5, GENDER = 0, RELATIONSHIP_STATUS = 1, COUNTRY = 2, INTERESTED_IN = 3, LANGUAGES_SPOKEN = 4;
	static const int GRAD_SCHOOL = 0, COLLEGE = 1, HIGH_SCHOOL = 2;
	int count[n], work_history, age;
	string attribute[n], file_name[n];
	vector <string> languages_spoken, interested_in;
	VB ret, education_history;
	
	svm(){}
	svm(string gender, string relationship_status, string country, vector <string> i, vector <string> l, VB e, int w, int a)
	{
		attribute[0] = gender;
		attribute[1] = relationship_status;
		attribute[2] = country;
		interested_in = i;
		languages_spoken = l;
		education_history = e;
		work_history = w;
		age = a;
		
		count[0] = 2; file_name[0] = "gender.txt";
		count[1] = 9; file_name[1] = "relationship status.txt";
		count[2] = 257; file_name[2] = "country.txt";
		count[3] = 2; file_name[3] = "interested in.txt";
		count[4] = 11; file_name[4] = "languages spoken.txt";
	}
	
	VB init(int size)
	{
		VB ret;
		f(i, size) ret.pb(0);
		return ret;
	}
	
	
	void append(vector <bool> a)
	{
		f(i, (int)a.size()) ret.push_back(a[i]);
	}
	
	void go(int index)
	{
		//cout << "GO " << index << endl;
		VB a = init(count[index]);
		freopen(file_name[index].c_str(), "r", stdin);
		string s, A = attribute[index];
		
		f(i, count[index])
		{
			getline(cin, s); 
			if(A == s) a[i] = 1;
		}
		
		append(a);
	}
	
	void int_in()
	{
		//puts("int_in");
		VB a = init(count[INTERESTED_IN]);
		freopen(file_name[INTERESTED_IN].c_str(), "r", stdin);
		string s;
		f(i, count[INTERESTED_IN])
		{
			cin >> s;
			f(j, (int)interested_in.size())
				if(interested_in[j] == s)
					a[i] = 1;
		}
		
		append(a);
	}
	
	void language()
	{
		//puts("language");
		VB a = init(count[LANGUAGES_SPOKEN]);
		freopen(file_name[LANGUAGES_SPOKEN].c_str(), "r", stdin);
		string s;
		f(i, count[LANGUAGES_SPOKEN])
		{
			cin >> s;
			f(j, (int)languages_spoken.size())
				if(languages_spoken[j] == s)
					a[i] = 1;
		}
		
		append(a);
	}
	
	void print()
	{
		freopen("out.txt", "w", stdout);
		append(education_history);
		f(i, (int)ret.size()) printf("%d:%d ", i + 1, ret[i] ? 1 : 0);
		int l = ret.size();
		printf("%d:%d %d:%d\n", l, work_history, l + 1, age);
	}
};

int main()
{
	puts("gender\nRelationship status\nCountry\nInterested in\nLanguages spoken\neducation history(grad school, college, high school)\nwork history\nage");
	//freopen("in.txt", "r", stdin);
	string gender, relationship_status, country, in, la, s;
	vector <string> interested_in, languages_spoken;
	int work_history, age, tmp;
	VB education_history(3);
	
	getline(cin, gender);
	getline(cin, relationship_status);
	getline(cin, country);
	getline(cin, in);
	getline(cin, la);
	f(i, 3) 
	{
		s(tmp);
		education_history[i] = tmp;
	}
	s(work_history);
	s(age);
	
	stringstream ss; ss << in;
	while(ss >> s) interested_in.pb(s);
	ss.clear(); ss << la;
	while(ss >> s) languages_spoken.pb(s);
	
	svm obj(gender, relationship_status, country, interested_in, languages_spoken, education_history, work_history, age);
	f(i, 3) obj.go(i);
	obj.int_in();
	obj.language();
	obj.print();
	
	return 0;
}
