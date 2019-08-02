---
layout: default
---

Long time no see!
I've entirely moved on from vanilla R5RS over to Chicken Scheme and I am now much more sane. My environment for this setup just involves Atom for editing text (along with a Scheme syntax package) and the Chicken compiler. Sadly I use windows at home and getting gcc to work correctly is a royal pain so running my programs usually involves testing them interactively. No .exes for me :(

Anyway, The chicken scheme library is great and definitely gives me the impression that it's suited to real world tasks instead of just education.

# Daily Programmer

I've had a long absence and this weekend had a large spurt of interest in Scheme again so I did a few of the easier [/r/dailyprogrammer](http://www.reddit.com/r/dailyprogrammer) challenges to get myself re-acquainted. These have been more helpful in learning the library that comes with Chicken Scheme rather than Scheme itself, but anyway, let's step through a few of the challenges and talk through some code

# Challenge 1

#### Challenge
> Your job is to create a program that lists all places within the range of 0-100 in spoken English, excluding the placing (X) of your winning pup. A reader should see a neatly formatted list of placements from 0-100 in spoken English, excluding your dog's placement.
Here's an example in the case of a 1st place finish;
0th, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th, 11st, 12nd, 13rd, 14th, 15th, 16th, 17th, 18th, 19th, 20th ...etc

(Note the exclusion of the 1st)

#### Result

    ;not exactly elegant...
    (define number-suffix '(
      (1 . "st")
      (2 . "nd")
      (3 . "rd")
      (0 . "th")
      (4 . "th")
      (5 . "th")
      (6 . "th")
      (7 . "th")
      (8 . "th")
      (9 . "th")))
    
    ;loop 'times' times and omit 'position' from the output
    (define loop
      (lambda (times position)
        (cond
          ((= times position) (loop (sub1 times) position))
          (else
            (display
              (string-append
                (number->string times)
                (get-suffix (last-digit times)) "\n"))
            (if (> times 1)
              (loop (sub1 times) position))))))
    
    (define get-suffix
      (lambda (key)
        (cdr (assq (char->number key) number-suffix))))
    
    ; 10934 -> 4
    ; 503 -> 3
    (define last-digit
      (lambda (digit)
        (string-ref
          (number->string digit)
          (- (string-length (number->string digit)) 1))))
    
    ; #\0 -> 0
    ; #\4 -> 4
    (define char->number
      (lambda (char)
        (- (char->integer char) 48)))
    
    (loop 100 6)

[Challenge link](https://www.reddit.com/r/dailyprogrammer/comments/4jom3a/20160516_challenge_267_easy_all_the_places_your/)

# Challenge 2

#### Challenge
remove vowels and return vowels

#### Result
# Challenge 3
#### Challenge

#### Result
pangram

# Challenge 4
#### Challenge

#### Result
date parsing

Apologise about the long hiatus, the reality is that this is probably going to happen so updates are on an ad-hoc basis.

# Questions
