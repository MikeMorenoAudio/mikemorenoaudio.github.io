---
layout: default
tags: programming
---

# Recognise the powers of the shell

A few days ago, an issue was raised on my SQL linter [sql-lint](https://github.com/joereynolds/sql-lint).
The request was simple:

> When I specify a directory, lint over the `.sql` files in that directory.

I will add this in (because features (don't hold me to this)) but I think it's worth pointing out that
you can achieve this in Linux with the built-in tools.

The end result is:

```
find . -iname "*.sql" | xargs -L1 sql-lint -f
```

This to me at least, the one writing all the code, is much cleaner than a couple hundred lines of Typescript, several edge cases, and the inevitable bugs.

If this user was aware of this they probably would have never requested the
feature.

Funnily enough, I've demonstrated this as a tip on one of my other (more popular)
repositories and I've not once been asked for this feature to be built-in. Maybe
awareness is all a person needs.
