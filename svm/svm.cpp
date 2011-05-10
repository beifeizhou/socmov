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

vector <string> data[5];
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
		count[4] = 31; file_name[4] = "languages spoken.txt";
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
		VB a = init(count[index]);
		freopen(file_name[index].c_str(), "r", stdin);
		string s, A = attribute[index];
		
		f(i, count[index])
		{
			//getline(cin, s); cout << "GO " << index << " : " << s << endl;
			s = data[index][i];
			if(A == s) a[i] = 1;
		}
		
		append(a);
	}
	
	void int_in()
	{
		//puts("int_in");
		VB a = init(count[INTERESTED_IN]);
		//freopen(file_name[INTERESTED_IN].c_str(), "r", stdin);
		string s;
		f(i, count[INTERESTED_IN])
		{
			s = data[INTERESTED_IN][i]; //cin >> s;
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
		//freopen(file_name[LANGUAGES_SPOKEN].c_str(), "r", stdin);
		string s;
		f(i, count[LANGUAGES_SPOKEN])
		{
			s = data[LANGUAGES_SPOKEN][i]; //cin >> s;
			f(j, (int)languages_spoken.size())
				if(languages_spoken[j] == s)
					a[i] = 1;
		}
		
		append(a);
	}
	
	void print()
	{
		//freopen("out.txt", "w", stdout);
		append(education_history);
		f(i, (int)ret.size()) printf("%d:%d ", i + 1, ret[i] ? 1 : 0);
		int l = ret.size();
		printf("%d:%d %d:%d\n", l, work_history, l + 1, age);
	}
};

int main()
{
	//puts("gender\nRelationship status\nCountry\nInterested in\nLanguages spoken\neducation history(grad school, college, high school)\nwork history\nage");
	//puts("gender\nRelationship status\nInterested in\nLanguages spoken\neducation history(grad school, college, high school)\nwork history\nage");
	//freopen("in.txt", "r", stdin);
	
	data[0].pb("male"); data[0].pb("female"); 
	data[1].pb("Single"); data[1].pb("In a relationship"); data[1].pb("Engaged"); data[1].pb("Married"); data[1].pb("It's complicated"); data[1].pb("In an open relationship"); data[1].pb("Widowed"); data[1].pb("Separated"); data[1].pb("Divorced");
	data[3].pb("Men"); data[3].pb("Women");
	data[4].pb("Mandarin"); data[4].pb("English"); data[4].pb("Spanish"); data[4].pb("Hindi"); data[4].pb("Russian"); data[4].pb("Arabic"); data[4].pb("Portuguese");data[4].pb("Bengali"); data[4].pb("French"); data[4].pb("Malay"); data[4].pb("Indonesian"); data[4].pb("German"); data[4].pb("Japanese"); data[4].pb("Farsi"); data[4].pb("Urdu"); data[4].pb("Punjabi"); data[4].pb("Wu"); data[4].pb("Vietnamese"); data[4].pb("Japanese"); data[4].pb("Tamil"); data[4].pb("Korean"); data[4].pb("Turkish"); data[4].pb("Telugu"); data[4].pb("Marathi"); data[4].pb("Italian"); data[4].pb("Thai"); data[4].pb("Burmese"); data[4].pb("Cantonese"); data[4].pb("Kannada"); data[4].pb("Gujarati"); data[4].pb("Polish");
	
	string gender, relationship_status, country, in, la, s;
	vector <string> interested_in, languages_spoken;
	int work_history, age, tmp;
	VB education_history(3);
	
	getline(cin, gender);
	getline(cin, relationship_status);
	//getline(cin, country);
	getline(cin, in);
	getline(cin, la);
	/*cout << "SVM GENDER : " << gender << endl;
	cout << "SVM REL STAT : " << relationship_status << endl;
	cout << "SVM INT IN : " << in << endl;
	cout << "SVM LANG : " << la << endl;*/
	f(i, 3) 
	{
		s(tmp); //cout << "TEMP : " << tmp << endl;
		education_history[i] = tmp;
	}
	s(work_history); //cout << "SVM WORK : " << work_history << endl;
	s(age); //cout << "SVM AGE : " << age << endl;
	
	stringstream ss; ss << in;
	while(ss >> s) interested_in.pb(s);
	ss.clear(); ss << la;
	while(ss >> s) languages_spoken.pb(s);
	
	svm obj(gender, relationship_status, country, interested_in, languages_spoken, education_history, work_history, age);
	f(i, 2) obj.go(i);
	obj.int_in();
	obj.language();
	obj.print();
	
	return 0;
}
