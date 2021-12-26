# **Advanced Topic**

## **Recursion**

Definition: **Recursion function** is a function implemented recursion method of programming
that call itself in the body of function one or multiple times and need to satify conditions of recurstion.

```
Termination condition: A recursive function has to fulfil an important condition to be used in a program: it has to terminate. A recursive function terminates, if with every recursive call the solution of the problem is downsized and moves towards a base case. A base case is a case, where the problem can be solved without further recursion. A recursion can end up in an infinite loop, if the base case is not met in the calls.
```
Source: [Recursive Function](https://python-course.eu/advanced-python/recursive-functions.php)


Useage:

- Remember to meet termination condition or will be in infinity loop.

- Increase the time by using memory rembember configuration

- Alway testing the running time of fucntion with `timeit`
  
Application:
    
  - Fibonacci Numbers
  
  - Fractorinal [n!]
