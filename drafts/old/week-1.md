---
layout: default
---

So I've just completed the first challenge from dailyprogrammer. It's a pretty easy challenge but that didn't stop me WTF'ing all the way through.

# The challenge

The challenge itself was simple (embarrasingly simple)

"Write a program that will ask the users name, age, and reddit username.
Have it tell them the information back, in the format:
your name is (blank), you are (blank) years old, and your username is (blank)"

# Questions

Here are the questions I asked myself throughout
and the answers that I (think) are correct

- How do I display stuff?
    - Use the (display) procedure

- How do I read user input
    - Use (read). Note that I think newer schemes actually have something
      called (read-line) which casts the user input from a symbol to a string for you

- Why is the variable stored from (read) not a string? 
    - As mentioned before, it's returned as a symbol, you need to convert it yourself

- How can I convert symbols?
    - Use (symbol->string) to convert a symbol to a string 

- How do I concatenate strings
    - use (string-append)

- What is the scheme filetype extension so I can actually save my work? 
    - I'm using '.scm' though I could be wrong...

# My solution

```
(display "What is your name")
(define name (symbol->string (read)))

(display "What is your age")
(define age (number->string(read)))

(display "What is your username")
(define user (symbol->string(read)))

(display 
 (string-append 
  "Your name is " name
  " and you are " age " years old"
  " and your username is " user))
```

# Unanswered questions

- Why does (read) bring back a number if the input is a number? Why not a symbol?

- WTF is a symbol?

# Things I enjoyed

I like the naming conventions and consistency of the procedures.
You barely have to look at the documentation because your guess of
a procedure name usually *is* the procedure name.

For example, I had no idea how to convert a number to a string. I used
```
number->string
```
and hey presto!
