# python trait的定义

trait为Python对象的属性增加了类型定义的功能，此外还提供了如下的额外功能：

- 初始化：每个trait属性都定义有自己的缺省值，这个缺省值用来初始化属性
- 验证：基于trait的属性都有明确的类型定义，只有满足定义的值才能赋值给属性
- 委托：trait属性的值可以委托给其他对象的属性
- 监听：trait属性的值的改变可以触发指定的函数的运行
- 可视化：拥有trait属性的对象可以很方便地提供一个用户界面交互式地改变trait属性的值

## About Traits

Traits are classes which contain methods that can be used to extend other classes, similar to mixins, with exception that traits do not useinheritance. Instead, traits are composed into other classes. That is;methods, properties and internal state are copied to master object.

The point is to improve code reusability by dividing code into simplebuilding blocks that can be then combined into actual classes.

There is also a wikipedia article about [Traits](http://en.wikipedia.org/wiki/Traits_class).

## Motivation

Traits are meant to be small pieces of behavior (functions or classes) used to extend other objects in a flexible, dynamic manner. Being small and independententities, they are easy to understand, maintain and test. Traits also give analternative approach in Python to handle diamond inheritance cases due to fact that no inheritance is happening at all (not saying multiple inheritance is an issue in Python).

The dynamic nature of traits enables some interesting use cases that are unreachable for conventional inheritance; Any changes made to class or instanceare applied immediately, and they affect whole application. In practice, this means it is possible to add new functionality to any class or instance and it can be from your own module, some 3rd party module (e.g Django) or even Python’s own internal classes (e.g. collections.OrderedDict).

For example, there is feature you would need from framework someone else has written. Only thing to do is to write traits for those classes that needs to be updated and extend them. After extending the classes, framework will behave based on those extended classes. Or if there is need to alter the behavior only some specific situation (or you just want to be careful), instances of classes can be extended only.

Other example would be a situation, where you discover a bug in 3rd party framework. Now you can create own solution safely, while waiting for the official patch to appear. Updating the framework code won’t override your extensions as they are applied dynamically. Your changes are only removed when you don’t need them anymore.