有关Traits本质的思考
===

## 1. Traits定义

Traits是一种语言特征，表示一组方法可以用于扩展一个类的功能。

## 2. 简单的理解

Traits的字面意思是特性。面向对象的时候，很多情况下，很多对象拥有相同的属性，或者有着同名且逻辑概念相同的方法名。我们如果可以在编写代码的时候能够用同样的代码操作拥有着同一特性的对象，则可以达到简化代码的目的。

传统的做法会让有相同特性的对象从有着共同基类的不同派生类例化，然后多继承会出现许许多多的问题。一些语言设计者会抛弃很多抽象的功能，于是有了接口，以及Mixin。

本质上，Traits和继承并无直接关系，在于扩展、代码复用。

> [当函数，类或者一些封装的通用算法中的某些部分会因为数据类型不同而导致处理或逻辑不同（而我们又不希望因为数据类型的差异而修改算法本身的封装时），traits会是一种很好的解决方案。](http://blog.csdn.net/my_business/article/details/7891687)

## 3. 从一个简单的模板入手

[source](./c++/src/cpp_test1.cpp)

```C++
#include <iostream>
using namespace std;
template <typename T>
struct is_void
{
    static const bool value = false;
};

template <>
struct is_void<void>
{
    static const bool value = true;
};

int main()
{
    std::cout << is_void<int>::value << endl;

    std::cout << is_void<void>::value << endl;
    return 0;
}
```

这个例子里面，


## 3. C++的STL中的Traits

C++中，容器的实现和迭代器的实现是分开的。



## 2. 







