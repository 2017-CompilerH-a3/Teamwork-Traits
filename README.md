## 1. 课题：

Trait。

Trait是一种语言特征，表示一组方法可以用于扩展一个类的功能。

## 2. 关于Trait的背景

> 多继承是好的，但是没有好的办法去做到多继承。

单继承的语言中类无法同时从两个基类继承属性或方法，而多继承却又因菱形继承、成员冲突等各种问题令人望而却步。绝大多数语言都不得不或多或少放弃掉多继承里面的一些特性，进而提出了弱化的概念。Java提出了接口。有的设计者认为继承不一定是好的代码复用的做法，提出了mixin。当然，Trait也是一种解决方案。Trait可以被看为有默认实现的接口。



### Trait的特点

* Trait提供一系列方法来执行行为。
* 每个方法作为行为的参数。
* Trait不指定状态变量，并且Trait提供的方法不直接访问状态变量。（即不能定义与使用成员变量）
* 类和Trait可以由其他Trait构成，但是构成的顺序无关。相冲突的方法必须被明确解决。
* Trait不影响构成的类的语义。
* Trait不影响构成的Trait的语义。

### Trait的优点

Trait能让类既可以看作方法的平展的集合，也能看作由许多Trait构成的整体。看作方法的集合使类的含义容易被理解，不同Trait的整合提供了复用。Trait整合了这两个特点，使得Trait在构造类的同时对类的含义没有影响。

与接口相比，Trait不强制要求使用者给出实现。与mixin相比，Trait是扁平型，且能在字节码级别看到有关信息，比mixin更加易用、有效安全。


### Trait的缺陷

* 没有完全解决命名冲突，使用别名的方式只是缩小了该问题的范围
* 虽然Trait基于单继承，但是还是会有Diamond Problem。例如，X使用了TraitY1和Y2，而Y1和Y2使用了Trait Z，则Trait Z的方法foo会被X得到两次。
* Trait特性太具体且不正交，现有语言基本很少会单独支持这个特性，且基本都可以通过语言本身就能模拟出来。



### 继承的问题

* 单继承：表达能力不足
* 多继承：当一个类可以沿不同路径继承自一个基类时，存在语义不明
* Mixin继承：由于结构是线性的并且处理冲突的方式有限，当在其中一个mixin中增加一个新的方法时，可能会重载在链上前面的mixin的一个同名的方法，而程序员并不知情。
* Trait：当方法出现冲突时，类的方法优先级高于Trait，Trait的方法优先级高于父类。


## 3. 与其他几个概念的不同


I. 与Java的接口不同之处：

interface 是定义接口，将逻辑交给其他程序员实现。Trait是自己实现逻辑，供其他人使用。

接口的约束是前置的，是定义初始就必须实现的, 他可以约束方法的实现却无法约束方法的调用, Trait 是一种后置的调用, 他已经实现了方法, 关键的是, 他只对调用了自身的类产生约束, 而对没有调用自身的类不产生影响, 同时他是可复用的。

也就是说，Java的接口是你要求其他人实现而定义出来的，是必须去实现每一个功能；而Trait，包括mixin，是你已经写完代码后给其他人使用，是某个对象可以去重新实现而不是必要。

II. 与Mixin的区别

* Mixin可能更多的是指动态语言，它是在执行到某个点的时候，将代码插入到其中来达到代码复用的效果。Trait更多的是编译过程中，通过一些静态手段赋值代码到类中使得其拥有Trait中的一些功能以达到代码复用的目的；

* “Mixins may contain state, (traditional) Trait don't.” 即mixin可以有成员变量而最开始的Traits是不能的。但是现在事实上Scala中Trait已经可以保存成员变量了。 

* “Mixins use "implicit conflict resolution", Trait use "explicit conflict resolution"”。 mixin碰到冲突会隐式的进行重写，后面覆盖前面的；而Trait有明确的优先级。

* “Mixins depends on linearization, Traits are flattened.” mixin是线性的，往类里追加的，后来的覆盖之前的；而Trait是扁平的。

在Mixin的实现中，比如Ruby，一个类中专门有维护mixin链。每次mixin一个module，就在链里头插那个module。查找方法时会沿着这个链一个一个查找，直到找到第一个匹配的就返回，所以会出现程序员给一个mixin新增方法时可能不知不觉就覆盖其他mixin方法。Mixin不会在编译时混入，所以比如往A mixin B，在A里是看不到B里面的细节的。只有运行后，解释器把具体的代码挂载到被混入类里，然后再使用。

而Trait则会与具体指令码对应，即A use Trait B的话，A里面能看的到B里面的代码细节。由于Trait是扁平型且编译时，所以编译器对不同Trait里面的同名方法会有发觉。



## 4. Trait在不同语言中的应用

### I. PHP Scala中的Trait

以php为例。

php现已经有关键字trait，可以在内声明成员变量(新支持的)和方法；在对应的需要用的类里面使用use关键字即可。当出现同名冲突后，需要使用insteadof等来指定使用哪一个，这样就解决了菱形继承的冲突问题。

[More](./php/doc/traits.md)

### II. 有关C++ STL的Type Trait

C++的traits不是语言特性，而是一种翻译时语用技巧。本质而言是对类本身进行操作，能通过比如模板与特化等萃取出需要的信息来进行操作。静态类型语言通常不会暴露类型系统方面的信息给用户进行编程，类型系统毕竟是一等环境，如果随便暴露给用户改就不静态了；有的时候在写模板的时候却需要知道某一个类型具体的性质（比如是否是数组，是否是指针）。在模板展开后，类型是确定的，但是却在编写模板时没办法获取这些信息。这个时候可以通过用模板构造指导推导，来获取编译时符号表中的信息来完成要求。

C++ STL内的trait啊或者说模板啊，更多的可以被看为弱化了的宏(比如Rust的卫生宏)，因为沉重的历史包袱而设计成如此，所以才需要这么麻烦的写法。

C++本身允许多继承，也可以通过虚基类来避免多继承的一些问题，是不需要上述的Trait特性来对类进行扩展以模拟多继承的效果。

[More](./c++/doc/traits.md)


### III. Python中的hasTrait

trait为Python对象的属性增加了类型定义的功能，此外还提供了如下的额外功能：

* 初始化：每个trait属性都定义有自己的缺省值，这个缺省值用来初始化属性

* 验证：基于trait的属性都有明确的类型定义，只有满足定义的值才能赋值给属性

* 委托：trait属性的值可以委托给其他对象的属性

* 监听：trait属性的值的改变可以触发指定的函数的运行

* 可视化：拥有trait属性的对象可以很方便地提供一个用户界面交互式地改变trait属性的值

为了匹配自己的语言特点，不同的语言对Trait的实现互不相同，Python的HasTrait使用了委托的方式。

HasTrait的特点：

由于HasTrait相互独立且代码量少，所以容易理解、维护和检测。并且HasTrait提供了一种解决菱形继承的方案，因为实际上Trait没有使用继承。


[More](./python/doc/python.md)
