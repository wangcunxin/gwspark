# -*- coding:utf-8 -*-

__author__ = 'kevin'


class Employee:
   '所有员工的基类'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary


class Person:
    'define a class to desc a person'
    name = "kevin"
    gender = "male"

    def __init__(self):
        pass

    def __del__(self):
        pass

    def __str__(self):
        pass

    def __cmp__(self, other):
        pass


class Man(Person):
    def __init__(self, age):
        Person.__init__(self)
        self.age = age

    def __str__(self):
        return "%s:%s" % (self.name, self.age)

    def __eq__(self, other):
        ret = True
        if self.name == other.name:
            if self.age == other.age:
                ret = True
        else:
            ret = False

        return ret

    def __cmp__(self, other):
        if self.age > other.age:
            return 1
        else:
            return -1


if __name__ == '__main__':
    p1 = Man(10)
    p1.__str__()
    p2 = Man(20)

    if (p1 >p2):
        print "p1>p2"
    elif (p1 < p2):
        print "p1<p2"
    else:
        print "p1==p2"

    p3 = Man(15)

    men = [p1,p2,p3]
    list.sort(men)
    for man in men:
        print man.__str__()

    print "Employee.__doc__:", Person.__doc__
    print "Employee.__name__:", Employee.__name__
    print "Employee.__module__:", Employee.__module__
    print "Employee.__bases__:", Employee.__bases__
    print "Employee.__dict__:", Employee.__dict__