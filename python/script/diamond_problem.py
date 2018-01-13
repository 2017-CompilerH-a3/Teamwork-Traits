from traits.api import Delegate, HasTraits, Instance, Int, Str


class GrandParent(HasTraits):
    last_name = Str('Wang')


class Father(HasTraits):
    age = Int

    father = Instance(GrandParent)
    last_name = Delegate('father')

    def _age_changed(self, old, new):
        print 'Age changed from %s to %s ' % (old, new)


class Mother(HasTraits):
    age = Int
    first_name = Str('Zhang')

    father = Instance(GrandParent)
    last_name = Delegate('father')


class Son(HasTraits):
    hobby = Str('computer')

    father = Instance(Father)
    mother = Instance(Mother)

    last_name = Delegate('father')
    first_name = Delegate('mother')

gp = GrandParent()
f = Father()
m = Mother()
s = Son()

f.father = gp
m.father = gp


s.father = f
s.mother = m

#s.last_name = 'Ling'
#print gp.last_name, f.last_name

s.configure_traits()
