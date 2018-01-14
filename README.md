All about Trait
===

索引与大纲

[背景](#background)
* 代码复用问题与不同解决方案

[Trait定义](#defination)
* Trait定义，以及被要求满足的特性
	
[Trait与其他的比较与优缺点](#analyze)
* 与继承、接口、mixin的联系与区别
* 优点与缺点
	
[Trait概念的扩展：(重要!)](#extend)
* Trait概念的扩展
* PHP C++ Python中的Trait
* C++中的type trait与其他概念的联系
* 各个语言的实现方法

[Q&A](#qa)
	
[总结](#summary)

---

<p id="background"></p>
	
## 1. 背景

> 多继承是好的，但是没有好的办法去做到多继承。

项目开发、代码编写中有一个关键，那就是代码复用。继承可以解决其中的问题。然而，单继承的描述能力不够，而多重继承的话有内存分布、命名冲突、代码维护困难等诸多问题。不同语言给出了不同的解决方案，对多重继承有不同程度的舍弃与替代。有接口，mixin，以及Trait。

<p id="defination"></p>

## 2. Trait定义

Trait是一种语言特征，表示一组方法可以用于扩展一个类的功能。

在使用时，先使用trait关键字定义一套方法，给出默认实现；然后其他类直接use这个trait即可，可决定是否重写。

在提出Trait的论文中，Trait被要求有以下的特征：

* 每个方法作为行为的参数。

* Trait不指定状态变量，并且Trait提供的方法不直接访问状态变量。（即不能定义与使用成员变量）

* 类和Trait可以由其他Trait构成，但是构成的顺序无关。相冲突的方法必须被明确解决。

* Trait不影响构成的类的语义。

* Trait不影响构成的Trait的语义。

关于第二点，现在的支持Trait的语言也开始允许声明使用变量了。

第三条的意思是，不同Trait有同名方法，或者菱形继承，必须显式给出解决方案。其他的同名，有默认优先级：子类方法高于Trait方法高于父类方法。

第四条第五条的意思是，你不能因为use了一个Trait，导致类的本意发生了变化。比如A原本继承B，现在A多use Trait C，A必须保留其原来的性质，比如是B子类的性质，空间布局不能被破坏掉。


<p id="analyze"></p>

## 3. Trait的大致理解与其他概念的比较

* Trait与继承

	Trait本质和继承没关系，二者有相同点，就是代码复用。每次继承，无论创建父类还是派生子类，都需要新的类，而类还有另一个角色，是要能创建生成对象。(这段在Trait论文里面有写：《Traits Composable Units of Behaviour》)

	因为当类的数量一多，保不准就有其他程序员使用了不该使用的基类，所以当我们并不需要类的全部功能，不需要能创建对象，这个时候可以使用Trait。

* Trait与Interface接口

	Interface本身并不是代码复用，而是为了解决多重继承的缺失的问题而被提出来的。接口不允许有默认实现，而Trait是代码复用，肯定要有默认实现。

	逻辑上来讲，接口和Trait概念完全不一样。接口是不同对象面对同一逻辑要给出自己的特性与实现；而Trait是不同类可以拥有某项共性，也可以给出自己的特性。

<p id="a1"></p>

* Trait与Mixin

	* Mixin更多的是指动态语言，它是在执行到某个点的时候，将代码插入到其中来达到代码复用的效果。Trait更多的是编译过程中，通过一些静态手段赋值代码到类中使得其拥有Trait中的一些功能以达到代码复用的目的。当然，如果是动态语言来模拟Trait特性，那肯定是执行时才会发生。

	* “Mixins may contain state, (traditional) Trait don't.” 即mixin可以有成员变量而最开始的Traits是不能的。

	* “Mixins use "implicit conflict resolution", Trait use "explicit conflict resolution"”。 mixin碰到冲突会隐式的进行重写，后面覆盖前面的；而Trait有明确的优先级。

	* “Mixins depends on linearization, Traits are flattened.” mixin是线性的，往类里追加的，后来的覆盖之前的；而Trait是扁平的。

	在Mixin的实现中，比如Ruby，一个类中专门有维护mixin链。每次mixin一个module，就在链里头插那个module。查找方法时会沿着这个链一个一个查找，直到找到第一个匹配的就返回，所以会出现程序员给一个mixin新增方法时可能不知不觉就覆盖其他mixin方法。Mixin不会在编译时混入，所以比如往A mixin B，在A里是看不到B里面的细节的。只有运行后，解释器把具体的代码挂载到被混入类里，然后再使用。

	而Trait则会与具体指令码对应，即A use Trait B的话，A里面能看的到B里面的代码细节。由于Trait是扁平型且编译时，所以编译器对不同Trait里面的同名方法会有发觉。


## 4. Trait的优缺点

* 优点：

	Trait能让类既可以看作方法的平展的集合，也能看作由许多Trait构成的整体。看作方法的集合使类的含义容易被理解，不同Trait的整合提供了复用。Trait整合了这两个特点，使得Trait在构造类的同时对类的含义没有影响。

	与接口相比，Trait不强制要求使用者给出实现。与mixin相比，Trait是扁平型，且能在字节码级别看到有关信息，比mixin更加易用、有效安全。


* 缺陷：

	没有完全解决命名冲突。虽然Trait基于单继承，但是还是会有Diamond Problem。例如，X使用了TraitY1和Y2，而Y1和Y2使用了Trait Z，则Trait Z的方法foo会被X得到两次。于是，还是需要显式解决同名问题。

	**Trait特性太具体且不正交，现有通用语言基本很少会单独支持这个特性，且基本都可以通过语言本身就能模拟出来。也许正因为这个原因，真正纯正支持Trait的语言可能只有PHP Scala之类的语言。**

<br><br><br>

---

<p id="extend"></p>

## 5. Trait概念的扩展

Wikipedia里面给出的定义如上所述，但是在给出的支持这种特性的语言却有许多，基本包括当今所有能看的到的语言。但是，显式有trait关键字的且常见的，细数也就只有PHP Scala。

之前说过，trait特性不正交，许多语言并没有trait关键字、没有trait语义，但是，基本都可以用已有的特性达到实现。下面按照主流的语言一并列出来，来看每一个语言的具体情况。

* PHP的Trait
	* 传统意义的Trait，没新的内容。 [More](./php/doc/traits.md)

* [C++ Type Trait(下文)](#cpptrait)
	* C++有抽象类及虚继承，没必要有Trait。
	* type_trait与传统Trait无关，但本质都是代码复用。

* [Python hasTrait(下文)](#pythontrait)
	* Python有多继承没Trait，但可以通过多继承+@property+getter+setter之类，可以实现。

* [Ruby Mixin -> Trait(下文)](#ruby)
	* Ruby有Mixin没多重继承与Trait，但因为Ruby魔幻的语法特性，可以用extend等小trick来达成基本一样的语法与功能。

* Java 带默认实现的接口
	* 基本能取代Trait。
	
* C# 无接口的默认实现，无多重继承，无mixin；无能为力。


<br><br>

<p id="cpptrait"></p>

### I. C++ Type Trait

C++本身允许多继承，也可以通过虚基类来避免多继承的一些问题，是不需要上述的Trait特性来对类进行扩展以模拟多继承的效果。

虚基类(抽象类)的内存布局，已经超出Trait的范围。

然而，Wiki里面提到了C++ STL里面的type_traits，这又是什么呢？

C++的type traits不是语言特性，而是一种翻译时语用技巧，也就是说从逻辑上讲和之前的Trait没关系。但是，trait本质而言是代码复用。STL的type trait则是一种对类本身进行操作，能通过比如模板与特化等萃取出需要的信息来进行操作。静态类型语言通常不会暴露类型系统方面的信息给用户进行编程，类型系统毕竟是一等环境，如果随便暴露给用户改就不静态了；有的时候在写模板的时候却需要知道某一个类型具体的性质（比如是否是数组，是否是指针）。在模板展开后，类型是确定的，但是却在编写模板时没办法获取这些信息。这个时候可以通过用模板构造指导推导，来获取编译时符号表中的信息来完成要求。

这一点在STL的实现里尤其重要，因为STL的容器和算法是分开实现的，如何从原生指针、迭代器等不同的数据类型、类对象萃取出指针的特性，是必须考虑的问题。

```C++
template <typename T>
struct my_is_void
{
    static const bool value = false;
};
template <>
struct my_is_void<void>
{
    static const bool value = true;
};

template<class T>
T* make_array(size_t size) {
	static_assert( !my_is_void<T>::value );
	return new T[size];
}
```

假设我们要写个通用的创建数组的函数，然而我们不能创建void的数组。C++在没有typeid之前，我们也不可以直接typeid(T)==typeid(void)，就算有，这也是运行时决定，不可被优化。虽然上述程序可以通过对make_array来进行是否是void的特化，不过如果有很多个模板函数，使用my_is_void会方便很多。

库里面还有其他的例子，判断是否是其他类型、稍微复杂些的程序。另外，STL里面也有关于迭代器、原生指针的萃取，此处就不讨论复杂的情况，来聊聊本质。  [有关其他的萃取的文档与代码](./c++/doc/traits.md)

其实，C++内的模板，更多的可以被看为是一种弱化了的卫生宏，因为沉重的历史包袱而设计成如此，所以才需要这么麻烦的写法。这一点上，Rust可能就会好多了。

不同对象有可能是有相同逻辑却不同名的方法，没法直接一个模板解决；每个不同种类的类型是肯定需要特化的，但是比起每个泛型算法都特化一次，不如一开始就用一个相同的接口，特化后从不同类型萃取出信息放在接口内，然后泛型算法直接操作接口就可以了。

这里要多提一下Concept，某种程度上Concept的实现离不开type_trait。C++11还是没有通过Concept特性，只能在语言层面来模拟(SFINAE,Substitution Failure Is Not An Error)，便也是在萃取失败后要报错，不等到模板展开后再报错。STL里面专门有一个处理错误的Filter，就是用来处理此的。

据说C++之父都没有想到能有这种写法。

<br><br><br>

---

<p id="pythontrait"></p>

### II. Python hasTrait

Python原生支持多继承，有按照广度或者深度优先搜索的方法。想要模拟Trait也很简单。

思路：因为Python可以动态修改类与其成员，单独写个trait相关函数来完成类的优先度判定，并同时使用比如字典等数据结构来进行平展继承即可。Python提供的py2trait、py3trait相关的库便是如此。Python语法不那么够自由，所以需要显示对类调用其他的方法来混入其他的逻辑上的Trait。

Python还有个库，hasTrait，最初用于数据科学，扩展出了以下的功能：

初始化：每个trait属性都定义有自己的缺省值，这个缺省值用来初始化属性

验证：基于trait的属性都有明确的类型定义，只有满足定义的值才能赋值给属性

委托：trait属性的值可以委托给其他对象的属性

监听：trait属性的值的改变可以触发指定的函数的运行

可视化：拥有trait属性的对象可以很方便地提供一个用户界面交互式地改变trait属性的值

示例代码给的是直接对Trait的使用。 [More](./python/doc/python.md)

**看上去只是一些赋值、函数调用与委托，和Trait有什么关系呢？**

**我们假想，我们已经写了一部分代码了，现在要对某个类增加功能，增加的功能在第三方库(看成Trait)，那么可以简单几句后，把变量委托出去交给三方库维护，不就直接扩展功能了嘛。**

实现上，最重要的功能是委托、监听。利用@property与getter setter(使得基本的引用与赋值能变成函数调用，操作更多的对象)，以及Python的继承，加上修改类成员，以达到Trait的特性。

<br><br><br>

---

<p id="ruby"></p>

### III. Ruby Mixin -> Trait

Ruby不支持多重继承，但是支持Mixin。与Python相同，Ruby可以动态对类与成员进行修改。Wiki里引用了一个Ruby程序员写的，如何使用Mixin来避免Mixin的那些问题。大概是因为Ruby语法非常自由且魔幻，虽然实现的方法比较丑陋，要处理各种冲突，不过通过一些extend能做到写出来后和直接使用trait基本一样的代码。

思路：module个需要被mixin的元对象，然后所有需要被当成trait的class需要extend这个module，然后会把trait内定义的各种方法导入到module内。其他类要使用trait的时候，直接将对应trait内之前混入的module维护的方法字典拆出来，并且同时处理一下冲突即可。与直接trait关键字声明相比，就真的只是trait id与extend Trait，还有就是class A use B与Function(A,B)的区别。

<br><br><br>

---

<p id="qa"></p>

## 6. Q&A

* Q: 与Mixin的区别

* A: [上去](#a1)

* Q: Trait的内存布局结构？

* A: 主流语言基本没有实现Trait的特性，因为都可以通过其他方式做的到。具体的实现方法[上面](#extend)都有讲到。有作实现的Scala，做法是把trait直接拷贝到类中，就好像是这个类本身一样。

---

<p id="summary"></p>

## 7. 总结

* Trait处理代码复用，解决了原始的多继承与Mixin的部分缺陷。

* C++的type_trait与Trait无关，但都是代码复用。C++ typetrait是STL与Concept实现的基础。

* Trait的特性不正交，基本的通用语言基本都可以模拟出Trait。