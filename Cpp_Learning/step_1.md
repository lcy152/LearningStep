# Learning and talking

* Lambda,操作符,虚函数与多态,模板语法

## Chapter 1

#### 1. Lambda 表达式

C++ 11 中的 Lambda 表达式用于定义并创建匿名的函数对象，以简化编程工作。(闭包)
~~~~
    [函数对象参数] (操作符重载函数参数) mutable 或 exception 声明 -> 返回值类型 {函数体}
~~~~

#####  函数对象参数
标识一个 Lambda 表达式的开始，这部分必须存在，不能省略。函数对象参数是传递给编译器自动生成的函数对象类的构造函数的。函数对象参数只能使用那些到定义 Lambda 为止时 Lambda 所在作用范围内可见的局部变量(包括 Lambda 所在类的 this)。函数对象参数有以下形式：

~~~~
    空。没有任何函数对象参数。
    =。函数体内可以使用 Lambda 所在范围内所有可见的局部变量（包括 Lambda 所在类的 this），并且是值传递方式（相
    当于编译器自动为我们按值传递了所有局部变量）。
    &。函数体内可以使用 Lambda 所在范围内所有可见的局部变量（包括 Lambda 所在类的 this），并且是引用传递方式
    （相当于是编译器自动为我们按引用传递了所有局部变量）。
    this。函数体内可以使用 Lambda 所在类中的成员变量。
    a。将 a 按值进行传递。按值进行传递时，函数体内不能修改传递进来的 a 的拷贝，因为默认情况下函数是 const 的，要
    修改传递进来的拷贝，可以添加 mutable 修饰符。
    &a。将 a 按引用进行传递。
    a，&b。将 a 按值传递，b 按引用进行传递。
    =，&a，&b。除 a 和 b 按引用进行传递外，其他参数都按值进行传递。
    &，a，b。除 a 和 b 按值进行传递外，其他参数都按引用进行传递。
~~~~

#####  操作符重载函数参数:
~~~~
    标识重载的 () 操作符的参数，没有参数时，这部分可以省略。参数可以通过按值（如: (a, b)）和按引用 (如: (&a, &b)) 两种方式进行传递。
~~~~

#####  返回值类型:
~~~~
    标识函数返回值的类型，当返回值为 void，或者函数体中只有一处 return 的地方（此时编译器可以自动推断出返回值类型）时，这部分可以省略。
~~~~






#### 2. 操作符

1. . -> :: :
~~~~
    A.B 则 A 为对象或者结构体.
    A->B 则A 为指针，-> 是成员提取，A->B 是提取 A 中的成员 B，A 只能是指向类、结构、联合的指针.
    :: 是作用域运算符，A::B 表示作用域 A 中的名称 B，A 可以是名字空间、类、结构.
    ：一般用来表示继承.
~~~~





#### 3. 虚函数与多态
1. 实现继承时,在父类型赋值子类型的时候,调用方法时调用的是父类型的方法,所以需要虚函数,这样调用的是子类型的方法.虚函数只能借助于指针或者引用来达到多态的效果。
2. 不用虚函数也可以用引用实现
3. 纯虚函数是要求子类必须实现该方法,派生类仅仅只是继承函数的接口.包含纯虚函数的类是抽象类，抽象类不能定义实例.
~~~~
    int main(){
        People p("王志刚", 23);
        Teacher t("赵宏佳", 45, 8200);
    
        People &rp = p;
        People &rt = t;
    
        rp.display();
        rt.display();
        return 0;
    }
~~~~





#### 4. 模板语法

写法一:
~~~~
    template <class identifier> function_declaration;
    template <typename identifier> function_declaration;
~~~~
写法二(其实是一种写法,只是换行了):
~~~~
    // class
    template <typename T>
    inline T const& Max (T const& a, T const& b) 
    { 
        return a < b ? b:a; 
    }
    /* 
        增加了 inline 关键字的函数称为“内联函数”。内联函数和普通函数的区别在于：当编译器处理调用内联函数的语句时，不会将该语句编译成函数调用的指令，而是直接将整个函数体的代码插人调用语句处，就像整个函数体在调用处被重写了一遍一样。
        有了内联函数，就能像调用一个函数那样方便地重复使用一段代码，而不需要付出执行函数调用的额外开销。很显然，使用内联函数会使最终可执行程序的体积增加。以时间换取空间，或增加空间消耗来节省时间，这是计算机学科中常用的方法。
    */

    // function
    template <class T>
    class Stack { 
        private: 
            vector<T> elems;     // 元素 
        public: 
            void push(T const&);  // 入栈
            void pop();               // 出栈
            T top() const;            // 返回栈顶元素
            bool empty() const{       // 如果为空则返回真。
                return elems.empty(); 
            } 
    }; 
    template <class T>
    void Stack<T>::push (T const& elem) 
    { 
        // 追加传入元素的副本
        elems.push_back(elem);    
    }
    ...
~~~~

##### 函数模板(类似于Java泛型)
~~~~
    template <typename identifier> function_declaration;
~~~~

例:
~~~~
    #include <stdio.h>
    #include "method.h"
    template<typename  T> void swap(T& t1, T& t2) {
        T tmpT;
        tmpT = t1;
        t1 = t2;
        t2 = tmpT;
    }
    int main() {
        //模板方法 
        int num1 = 1, num2 = 2;
        swap<int>(num1, num2);
        printf("num1:%d, num2:%d\n", num1, num2);  
        return 0;
    }
~~~~

##### 类模板
~~~~
    template <class identifier> function_declaration;
~~~~

类模板--栈(例):
statck.h
~~~~
    template <class T> class Stack {
        public:
            Stack();
            ~Stack();
            void push(T t);
            T pop();
            bool isEmpty();
        private:
            T *m_pT;        
            int m_maxSize;
            int m_size;
    };
~~~~

stack.cpp
~~~~
    #include "stack.cpp"
    template <class  T>  Stack<T>::Stack(){
        m_maxSize = 100;      
        m_size = 0;
        m_pT = new T[m_maxSize];
    }
    template <class T>  Stack<T>::~Stack() {
        delete [] m_pT ;
    }
    template <class T> void Stack<T>::push(T t) {
        m_size++;
        m_pT[m_size - 1] = t;
        
    }
    template <class T> T Stack<T>::pop() {
        T t = m_pT[m_size - 1];
        m_size--;
        return t;
    }
    template <class T> bool Stack<T>::isEmpty() {
        return m_size == 0;
    }
~~~~

main.cpp
~~~~
    #include <stdio.h>
    #include "stack.h"
    int main() {
        Stack<int> intStack;
        intStack.push(1);
        intStack.push(2);
        intStack.push(3);
        
        while (!intStack.isEmpty()) {
            printf("num:%d\n", intStack.pop());
        }
        return 0;
    }
~~~~

##### 模板参数
~~~~
    template<class T, T def_val> class Stack{...}
~~~~

类模板--栈(例):
statck.h
~~~~
    template <class T,int maxsize = 100> class Stack {
        public:
            Stack();
            ~Stack();
            void push(T t);
            T pop();
            bool isEmpty();
        private:
            T *m_pT;        
            int m_maxSize;
            int m_size;
    };
~~~~

stack.cpp
~~~~
    #include "stack.cpp"
    template <class T,int maxsize> Stack<T, maxsize>::Stack(){
        m_maxSize = maxsize;      
        m_size = 0;
        m_pT = new T[m_maxSize];
    }
    template <class T,int maxsize>  Stack<T, maxsize>::~Stack() {
        delete [] m_pT ;
    }
            
    template <class T,int maxsize> void Stack<T, maxsize>::push(T t) {
        m_size++;
        m_pT[m_size - 1] = t;
        
    }
    template <class T,int maxsize> T Stack<T, maxsize>::pop() {
        T t = m_pT[m_size - 1];
        m_size--;
        return t;
    }
    template <class T,int maxsize> bool Stack<T, maxsize>::isEmpty() {
        return m_size == 0;
    }
~~~~

main.cpp
~~~~
    #include <stdio.h>
    #include "stack.h"
    int main() {
        int maxsize = 1024;
        Stack<int,1024> intStack;
        for (int i = 0; i < maxsize; i++) {
            intStack.push(i);
        }
        while (!intStack.isEmpty()) {
            printf("num:%d\n", intStack.pop());
        }
        return 0;
    }
~~~~

##### 模板专门化
~~~~
    template<class T> void swap(T& t1, T& t2);
~~~~

##### 模板类型转换
~~~~
    template<class T> void swap(T& t1, T& t2);
~~~~

##### 其他
一个类没有模板参数，但是成员函数有模板参数，是可行的:
~~~~
    // 甚至可以把Util的equal声明为static
    class Util {
        public:
            template <class T> static bool equal(T t1, T t2) {
                return t1 == t2;
            }
    };

    int main() {
        int a = 1, b = 2;
        Util::equal<int>(1, 2);
        return 0;
    }
~~~~






#### 5. 引用与指针

##### 精简版
~~~~
    指针：变量，独立，可变，可空，替身，无类型检查；
    引用：别名，依赖，不变，非空，本体，有类型检查；
~~~~
##### 完整版
~~~~
    1. 概念

　　指针从本质上讲是一个变量，变量的值是另一个变量的地址，指针在逻辑上是独立的，它可以被改变的，包括指针变量的值（所指向的地址）和指针变量的值对应的内存中的数据（所指向地址中所存放的数据）。

　　引用从本质上讲是一个别名，是另一个变量的同义词，它在逻辑上不是独立的，它的存在具有依附性，所以引用必须在一开始就被初始化（先有这个变量，这个实物，这个实物才能有别名），而且其引用的对象在其整个生命周期中不能被改变，即自始至终只能依附于同一个变量（初始化的时候代表的是谁的别名，就一直是谁的别名，不能变）。

2. C++中的指针参数传递和引用参数传递

　　指针参数传递本质上是值传递，它所传递的是一个地址值。值传递过程中，被调函数的形式参数作为被调函数的局部变量处理，会在栈中开辟内存空间以存放由主调函数传递进来的实参值，从而形成了实参的一个副本（替身）。值传递的特点是，被调函数对形式参数的任何操作都是作为局部变量进行的，不会影响主调函数的实参变量的值（形参指针变了，实参指针不会变）。

　　引用参数传递过程中，被调函数的形式参数也作为局部变量在栈中开辟了内存空间，但是这时存放的是由主调函数放进来的实参变量的地址。被调函数对形参（本体）的任何操作都被处理成间接寻址，即通过栈中存放的地址访问主调函数中的实参变量（根据别名找到主调函数中的本体）。因此，被调函数对形参的任何操作都会影响主调函数中的实参变量。

　　引用传递和指针传递是不同的，虽然他们都是在被调函数栈空间上的一个局部变量，但是任何对于引用参数的处理都会通过一个间接寻址的方式操作到主调函数中的相关变量。而对于指针传递的参数，如果改变被调函数中的指针地址，它将应用不到主调函数的相关变量。如果想通过指针参数传递来改变主调函数中的相关变量（地址），那就得使用指向指针的指针或者指针引用。

　　从编译的角度来讲，程序在编译时分别将指针和引用添加到符号表上，符号表中记录的是变量名及变量所对应地址。指针变量在符号表上对应的地址值为指针变量的地址值，而引用在符号表上对应的地址值为引用对象的地址值（与实参名字不同，地址相同）。符号表生成之后就不会再改，因此指针可以改变其指向的对象（指针变量中的值可以改），而引用对象则不能修改。

3. 总结

相同点：

　　都是地址的概念

不同点：

　　指针是一个实体（替身）；引用只是一个别名（本体的另一个名字）

　　引用只能在定义时被初始化一次，之后不可改变，即“从一而终”；指针可以修改，即“见异思迁”；

　　引用不能为空（有本体，才有别名）；指针可以为空；

　　sizeof 引用，得到的是所指向变量的大小；sizeof 指针，得到的是指针的大小；

　　指针 ++，是指指针的地址自增；引用++是指所指变量自增；

　　引用是类型安全的，引用过程会进行类型检查；指针不会进行安全检查；
~~~~

##### 智能指针shared_ptr
~~~~
    1 shared_ptr仅提供-> 、*和==运算符，没有+、-、++、--、[]等运算符.

    2 当我们创建 shared_ptr 对象而不分配任何值时，它就是空的；普通指针不分配空间的时候相当于一个野指针，指向垃圾空间，且无法判断指向的是否是有用数据.

    3 采用引用计数,当引用为0是自动垃圾回收.

    4 不要使用同一个原始指针构造shared_ptr.不要用栈中的指针构造shared_ptr对象.shared_ptr 默认的构造函数中使用的是delete来删除关联的指针，所以构造的时候也必须使用new出来的堆空间的指针。示例：
        #include<iostream>
        #include<memory>
        int main()
        {
            int x = 12;
            std::shared_ptr<int> ptr(&x);
            return 0;
        }
    当shared_ptr对象超出作用域调用析构函数delete 指针&x时会出错.

    5 建议使用make_shared.而不是使用默认构造函数创建std::shared_ptr<int> ptr(&x).
    std::shared_ptr<int> ptr_1 = make_shared<int>();
    std::shared_ptr<int> ptr_2 (ptr_1);
~~~~

##### 智能指针weak_ptr
~~~~
    1 shared_ptr在循环引用的时候会出现计数不为零的问题,导致内存泄漏.
    2 weak_ptr是弱智能指针对象，它不控制所指向对象生存期的智能指针，它指向由一个shared_ptr管理的智能指针。将一个weak_ptr绑定到一shared_ptr对象，不会改变shared_ptr的引用计数。一旦最后一个所指向对象的shared_ptr被销毁，所指向的对象就会被释放，即使此时有weak_ptr指向该对象，所指向的对象依然被释放。

~~~~



