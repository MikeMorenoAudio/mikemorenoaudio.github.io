---
layout: default
---

[last week](week-1) involved a simple daily programmer challenge that asked for user input.
Since then I've also dug a bit further into Scheme as that last week only really supplied me with 1-2 hours worth of scratching my head.

# Challenge 1

I've been making my way through various challenges from the [TSPL3 ](http://www.scheme.com/tspl3/) book.
One of them included the challenge for a 'shorter' function


> The procedure 'length' returns the length of its argument, which must be a list. For example, (length '(a b c)) is 3. 
> Using length, define the procedure shorter, which returns the shorter of two list arguments. 
> Have it return the first list if they have the same length.

# Solution

```
(define shorter
  (lambda (ls other-ls)
    (cond
      ((< (length ls) (length other-ls)) ls)
      ((> (length ls) (length other-ls)) other-ls)
      (ls))))
```

I'm starting to get a bit more comfortable with Scheme, in particular I am now finally grasping the placement of the parenthesis and in general getting a better feel for the syntax.

Apart from this challenge (which I managed to do on my lunchbreak at work) I've been going through another easy challenge from daily programmer. I don't think I'll be hitting the intermediate ones for a good few weeks. This is one of the most frustrating things for me personally as I see several harder problems and know how to solve them in a 'C like language', translating that to Scheme is non-trivial. It really does show how Lisp(s) are so different from the norm that I'm used to.

# Challenge 2

Doing these challenges has also made me aware of how much I rely on mutable state in other languages. For example, the [challenge on /r/dailyprogrammer](https://www.reddit.com/r/dailyprogrammer/comments/39ws1x/20150615_challenge_218_easy_todo_list_part_1/) states

> Add an item to the to-do list
> Delete a selected item from the to-do list
> And obviously, print out the list so I can see what to do!

This is extremely easy with mutable state. Just have an array that you add and remove from, but given that assignments are frowned upon in Scheme, I try not to use them. Infact I haven't used any set!'s just yet.  Kent Dybvig states

> In fact, most of the assignments that are either necessary or convenient in other languages are both unnecessary and inconvenient in Scheme

And since I'm only learning whatever people tell me about Scheme at this point, I think I'll learn from a reputable source. In the case of this challenge, I won't be going with one global list that can be altered but rather just a new list each item. 

# Solution

```
;todo  list

(define todo '("eat breakfast" "take a shower"))

;doesn't really need to be a procedure
;since it's just a wrapper for cons...
(define add-item
  (lambda (item ls)
    (cons item ls)))

(define show-list
  (lambda (ls)
    (cond
      ((null? ls) (newline))
      (else (display 
              (string-append(car ls) "\n"))
            (show-list (cdr ls))))))

(define delete-item
  (lambda (item ls)
    (cond
      ((null? ls) '())
      ((eqv? item (car ls)) (delete-item item (cdr ls)))
      (else (cons (car ls) (delete-item item (cdr ls)))))))
```

# Other Stuff

Apart from the above, I've also been doing some small tests on my own just to get better acquainted with the language.

One in particular is converting a number into a list i.e.
```
12345 => '(1 2 3 4 5)
```

I ended up making quite a few helper functions to help get through this. I was surprised that there was no ```char->number``` procedure but there was ```string->number``` and other similar procedures. So I made my own (hacky) version 

```
(define char->number
  (lambda (char)
    (- (char->integer char) 48)))
```

This would then allow me to do the following
- Convert the input 12345 to a string : 
```(number->string 12345) => "12345"```
- Convert the string to a list : 
```(string->list "12345") => '(#\1 #\2 #\3 #\4 #\5)```
- Convert the characters (one by one) into numbers 
```(char->number #\1) => 1 ```

Now that we have that functionality. We just need one more procedure that calls ```(char->number)``` over the given list and then we're done. This sounds like the perfect opportunity for ```map```, so I went with this:

```
(define number->list
  (lambda (n) 
    (map char->number(string->list (number->string n)))))
```

And it worked!

```(number->list 123456) => '(1 2 3 4 5 6)```
```(car(number->list 123456)) => 1```

# Questions

As with last time, here are some questions I asked myself throughout.

- How do I display a new line?
    - You can just use "\n" like everywhere else. There's also the (newline) procedure, I'm not sure of the difference between the two but I have noticed (atleast for me) that the (display) procedure prefers the "\n" version. 

- How do I make a comment?
   - Just use ';'

- How do I get the nth character of a string?
    - Use 'string-ref' i.e. 
        ```(string-ref "test" 0) -> #\t```

- How can I convert a character to a number?
    - You can't natively, I made a small fudge that sort of allows it. This only works for numbers 0-9 though because #\10 obviously isn't a char 

- Is there a 'map' procedure like in Python or PHP or most other languages? 
    - Yes!

# Unanswered Questions

These challenges made me question a few things. I also have a few other questions that I'd like to ask alongside this.

- Why would you use an 'if' when 'cond' seems so much cleaner?

- Is there a date, time, or date time library built into Scheme?

- Why are there two versions of new line? What's the difference? ("\n" and (newline))
