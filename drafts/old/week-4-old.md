---
layout: default
---

It's been a few weeks since I last posted. Mainly because, I had nose surgery and I can now breathe, wahoo!

Anyway...

# Project

I've found a project that I can work on in my spare time so that I get a little more out of this than just completing programming challenges.

The project is basically a command line interface for various music theory type things.

I thought of the idea a while ago and decided to either do it in C or Scheme. I went with Scheme in the end because I know doing any sort of string processing in C is rather painful. 


```
(define test '(#\t #\e #\s #\t #\i #\n #\g))

;Returns a lists elements up to char
(define list-till
  (lambda (ls char)
      (display ls)
      (newline)
    (cond
      ((eq? char (car ls)) (car ls))
      ((eq? (memv char ls) #f) '())
      (else 
        (cons (car ls) (list-till (cdr ls) char))))))
```
