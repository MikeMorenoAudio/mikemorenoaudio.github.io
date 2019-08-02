---
layout: default
tags: programming
---

Sometimes Vim can slow down when you start to push it to being something more than just a text editor.
These are some of the optimisations I've read/seen compiled into a handy list :D

## Profiling

If you've got a noticeably slow Vim and don't even know where to start, here's a good guide.
https://stackoverflow.com/questions/12213597/how-to-see-which-plugins-are-making-vim-slow

## Fixing

> Syntax highlighting can be **really** slow on long lines. Solution:

```
set synmaxcol=120 "Only highlight the first 120 columns.
```

> No. Syntax highlighting is **REALLY** slow. Solution:

You'll need to dig in a bit for this one.

First do
```
:syntime on
```

Make a load of slow movements in vim and then

```
:syntime report
```

From there,  try and whittle down the issue. Slowest patterns are at the top.

> Match paren is slowing down my Vim. Solution:

```
"The default timeout is 500, lots of us have powerful machines, so set the timeout to a smaller value.
let g:matchparen_timeout = 20
let g:matchparen_insert_timeout = 20
```

Or disable it altogether 

```
let loaded_matchparen = 1
```

> Scrolling is sluggish. Solution

```
"cursor line is ridiculously slow for something seemingly simple. Remove it entirely if you have it enabled
set nocursorline

"Set lazyredraw so we're not constantly redrawing the screen
set lazyredraw
```

> Startup time is slow

- `vim --startuptime` and fix the issues.
- Make sure any plugins you have are using the `autoload` directory so they're loaded only when needed.
- Make sure you're clearing your autocmds with `autocmd!`

### Plugins 

#### ap/vim-css-color

The `parse_screen` function is quite slow. Be weary of this when using this plugin.

#### tpope/vim-fugitive

fugitive#statusline is evaluated hundreds of times (I'm assuming to detect a branch change). Again, be mindful.

## References

A lot of this was pieced from various Reddit and StackOverflow posts.
Here are the ones I could find:

https://stackoverflow.com/questions/12213597/how-to-see-which-plugins-are-making-vim-slow
