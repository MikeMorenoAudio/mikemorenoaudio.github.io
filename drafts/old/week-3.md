---
layout: default
---

I took a short break from challenges this week as I for some reason got roped into fooling around with some web stuff outside of the Scheme world. That didn't stop me messing around with Scheme though.

I noticed that Scheme is pretty much entirely based on the list (from my reading so far), and I got curious about other built-in data structures. 

# Dictionaries

A dictionary is just a container of key-value pairs. They are supported in Scheme but are called 'association lists'. Even though they're supported, I don't think they're actually implemented to get the main benefits of a dictionary (average constant search time) but still, they're useful even without the speed.

> Associations are useful for storing information (values) associated with certain objects (keys).

I implemented a few 'helper' functions just to get to grips with association lists and improper pairs.

```
(define dict '(("name" . "Joe") ("Job" . "Developer") ("Age" . 25)))

;returns the value from a dict given its key
(define dict-value
  (lambda (key dict)
    (cdr (assq key dict))))

;return all keys from a dictionary
(define dict-keys
  (lambda (dict)
    (cond
      ((null? dict) '())
      (else (cons (caar dict) (dict-keys (cdr dict)))))))

;Same as keys but for values because why not?
(define dict-values
  (lambda (dict)
    (cond
      ((null? dict) '())
      (else (cons (cdar dict) (dict-values (cdr dict)))))))
```

These helpers got me better acquainted with recursive procedures and also the many varieties of ```cdr``` and ```car```.


# Stacks

There was a challenge in TSPL3 involving stacks that I set out to do

> Modify the stack object to allow the two messages ref and set!. (stack 'ref i) should return the ith element from the top of the stack; (stack 'ref 0) should be equivalent to (stack 'top). (stack 'set! i v) should change the ith element from the top of the stack to v.

First I'll show the stack 'object' that I have at the moment

```
(define make-stack
  (lambda()
    (let ((ls '()))
      (lambda (msg . args)
        (cond
          ((eqv? msg 'empty?) (null? ls))
          ((eqv? msg 'push)
            (set! ls (cons (car args) ls)))
          ((eqv? msg 'top) (car ls))
          ((eqv? msg 'pop)
            (set! ls (cdr ls)))
          ((eqv? msg 'show)
            ls)
          (else "undefined operation"))))))
```

At the moment, this to me looks fairly magical so I'm going to need to read about closures a lot more to get this to sink in. I added in a ```show``` command for convenience.

The first challenge  was fairly easy, it was just a list-ref so I  added in 
```
((eqv? msg 'ref)
  (list-ref ls (car args)))
```

The last one was only slightly harder, again, it was just getting to grips with reading ```cadr``` and the other forms.
```
((eqv? msg 'set!)
  (set-car! (list-tail ls (car args)) (cadr args)))
```

# Chicken Scheme!

Aside from the above, I'm moving on from R5RS over to Chicken Scheme solely because the R5RS library is just **too** small for me. There's no 'random' library or any 'date/time' procedures. The lack of these is limiting the amount of fun I can get from Scheme and I really don't want Scheme to leave a sour taste in my mouth D:

From now on it's Vim and the Chicken Scheme compiler all the way, we'll see how it goes!

I'll also stop doing weekly updates and just update when I feel like, weekly is far too frequent and takes more work than I initially thought.

# Questions

As always, here are some things I asked myself through this challenge and week.

- How do I get the nth item of a list?
    -  use list-ref 
```(list-ref '(1 2 4) 0) => 1```
- What's the difference between ```list-ref``` and ```list-tail```, they seem to do the same thing?
    - They don't do the same thing. Whereas ```list-ref``` brings back the nth-item, ```list-tail``` brings back the list-item and everything following that.
```(list-ref '(10 1 23 64 95) 2) => 23```
```(list-tail '(10 1 23 64 95) 2) => (23 64 95)```
- Are there dictionaries in scheme?
   - Yes! Except, they're called association lists and look like this
    ```'((1 . 2) (3 . 4))```
    There seems to be very few operations on association lists. There are 3 but they all do the same thing ```assq```, ```assv```, ```assoc```.
- Is there a 'split' procedure in Scheme that splits on char and brings back a new list?
    - Not in R5RS but there is in different implementations.
- How can I have an arbitrary amount of parameters for a procedure?
    - There are 2 ways, if it's a normal procedure, you can use dot notation
```(define (procedure . args))```
For anonymous functions (which I've used throughout so far), you do
```(lambda args ...)```
- Is there a 'pass' keyword in Scheme. As in, if the list is ```null?``` don't return anything?
   - I don't think so. People have said you can use ```(values)``` but that doesn't really seem to be what it's made for so I'm not sure I'm a fan of that idea.
- What's the difference between a proper and improper list?
    - See [here](http://stackoverflow.com/questions/16571182/confused-about-improper-lists-in-scheme) for a decent explanation, I can't explain it well enough.
- What the hell is the dot-syntax in an association list?
    - The dot syntax signifies an improper list.
