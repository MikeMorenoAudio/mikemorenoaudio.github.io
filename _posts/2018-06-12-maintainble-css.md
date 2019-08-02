---
layout: default
tags: programming
---

This article will glance over various ways of creating a design that you don't (or shouldn't) have to keep coming back to again and again to fix layout issues. 

# 1. Be consistent with margins

Use a consistent margin (top, right, bottom, left)but try not to mix them. The reason being is that if you're mixing margin styles, you can't easily predict how the spacings will behave (Also beware of margin collapsing).
Below we show a good example with `inline-block` elements i.e. They sit next to each other.

#### Good
```
button,
select {
    margin-left: 30px
}
```
#### Bad
```
button {
    margin-right: 20px;
    margin-left: 10px;
}

select {
    margin-right: 30px;
    margin-left: 10px;  /*Note that now we're actually getting pushed 30px (20px margin right on the button!)   */
}
```

See what I mean? If we use the same margin-direction for X and Y axis, then we're good. We're consistent and won't give ourselves problems!

# 2. Be general with your selectors.

#### This is bad
```
header ul li a {
    color: blue
}
```
If you know that every < a > tag in your header is a link, 
#### just do
```
header a {
    color: blue
}
```
Obviously if you need to be specific, then so be it. You should be asking yourself why though...

# 3. Use classes.

If you're targeting ID's everywhere, you're being way too specific. The specificity weighting of an id is 100 times greater than that of a normal element ([ref](https://www.smashingmagazine.com/2007/07/css-specificity-things-you-should-know/#how-to-measure-specificity)).

```
/*Has a weighting of 100*/
#label-homepage {
    color: green;
}

/* Has a weighting of 1*/
label {
    color: red
}
```
That means that in order to override our id style, we would have to do more specific stylings :(

# 4. Embrace Pseudo classes (if need be)

I shouldn't have to tell you to use these but here we are having this conversation (for some reason).
I've worked at places and seen this:

```
.footer-link {
    color: white;
    background: black;
}

.footer-link-first {
    color: black;
    background: white;
}
```
But most of that is redundant now. Really, to slim it down completely, we can do
```
footer a {
    color: white;
    background: black;
}

/*No extra classes!*/
footer a:first-child {
    color: black;
    background: white;
}
```

# 5. Get clever with CSS selectors

There is a great article (link:http://code.tutsplus.com/tutorials/the-30-css-selectors-you-must-memorize--net-16048 text:here) that goes through them better than I could.

Can you tell me why this

```
.parent .child + * {
    margin-top: 30px;
}
```
Is better than this?
```
.parent .child {
    margin-bottom: 30px;
}
```
It's quite simple really. When we have that final child in the parent, we're going to have a rogue 30px margin on the bottom that element.

With the first approach, we apply a margin top to every element but the first one. This could also be written with the :first-child selector but in a less clean way.

*Beware* : This article is about maintainability. If your colleagues can't understand it, it's not maintainable. If it's a solo project or you're working with other developers in the know, then be as creative as you want with selectors!

*Note*: If these tickle your pickle, you should read about [owl-selectors](https://css-tricks.com/lobotomized-owls/)

# 6. Use proper naming conventions

Okay so this probably won't help too much with maintainability but I thought I'd point it out.

#### Python has this
```
my_naming_style
```
#### Javascript has this
```
myNamingStyle
```
#### CSS has this
```
my-naming-style
```
There's no real reason to follow suit, but it's always a good thing. If you work with anyone else, they'll thank you for it.

# 7. Become one with flex

Flex is great when you know its applications. Again, I won't cover flex here, there's a great guide (link:https://css-tricks.com/snippets/css/a-guide-to-flexbox/ text:here) that covers most of what you need to know.

Flex allows us to not consider 'what ifs' like 'What if we add another item in our header? Would it overflow onto the next line?'. That's not a concern if we use flex as it handles it very gracefully.

To apply flex, you can just do
```
footer ul {
    display: flex;
}

footer li {
    flex: 1;   
}
```

This means that all < li >'s in the < ul > will have an equal amount of space to work with. You need to set a display type on your container as we have done in the < ul > and then you need to set the proportion of the element like we did in the < li >

Note that in any real world example, you should add all of the other vendors (-moz-, -ms- etc...) and be aware of browser compatibility.

# 8. HTML5

HTML5 gave us some great new selectors that I've already been showing you.

#### You no longer have to do
```
<div class="footer">
    Footer content here
</div>
```
#### You can do
```
<footer>
    footer content here
</footer>
```
Which is great because it saves us writing even more classes and is way more useful to browsers as they can better interpret the markup on the page!

# 9. Go up the tree

If you're applying an inherited property, place it up the tree as far as you can.

#### Instead of this
```
header {
    height: 200px;
}

header p {
    color: blue;
}
```
#### Do this
```
header {
    height: 200px;
    color: blue;
}
```

Move the color into the 'header' element. Then, everything under the header will have that color. 
Not all properties are inherited, there is a handy list (link:http://www.w3.org/TR/CSS21/propidx.html text:here) that shows recent(ish) ones. I would advise doing this wherever you can as it makes your CSS much more general, slimmer, and maintainable.

# 10. There's a tag for that

Like I mentioned with HTML5. Sometimes you just need to do a little bit of research and it'll save you writing a redundant class.
#### Don't do this
```
<p>The current time is <span class="time">16:45</span>.</p>
```
#### When you can do this
```
<p>The current time is <time>16:45</time>.</p>
```

Not only are you reducing your class count, you're always being way more semantic and meaningful to the browser.

# Questions & Corrections

I recently posted this on [reddit](https://www.reddit.com/r/web_design/comments/6v2moc/i_wrote_a_small_list_of_things_to_do_to_make_your/) and some of these tips caused a stir between certain people so I'll address them so if you think the same thing, hopefully I will have answered it for you. I'd also like to thank the people that commented on incorrect parts on the article, I have amended what I can, so thank you!

> What's up with the inconsistent spacing of colons, brackets and missing semicolons in an article about being consistent?

My bad, fixed!

> Why not scss, sass or less? I think it makes a lot of things easier. In combination with bem things get cleaner and easier to find.

For the record I do like SASS and LESS but they tend to promote(not on purpose) bad practices.

The worst one I see all the time is something like this
    
```
section {
    ul {
        li {
            a {
            }
        }
    }
}
```

Which compiles down to a horribly specific

`section ul li a`

When there's absolutely nothing wrong with

`section a`

Okay, if you *need* that specificity then so be it, but I think most of the times they can be avoided.

But yes, pre-processors are the future. I tend to use them sparingly however.

> /*Note that now we're actually getting pushed down 40px (10px margin botton on the header!) */
What about margin collapsing?

Thank you for pointing this out, that was an oversight on my part. I've updated that section to use `margin-right` and `margin-left` to avoid confusion.

> http://getbem.com/

True, bem solves a lot of these problems but they won't all be solved by bem. Consistency and using HTML5 is just general good advice regardless of your CSS methodology
