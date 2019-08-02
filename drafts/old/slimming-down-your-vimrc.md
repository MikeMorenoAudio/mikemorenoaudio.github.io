---
layout: default
tags: programming
---

## Intro

I frequently purge my `init.vim` trying to get it smaller and smaller.  I like to rely on native vim.
If you're one of these people, read on and maybe you will learn something :D

## Remove unneccessary plugins

## Learn vim

I had a few functions like this in my vimrc

```
Show file command stuff here
```

I forced myself to get used to the native way and now it's just as fast and I know more about vim.
You'd probably be surprised at the amount of stuff this tip will help you get rid of.


## Remove settings defined elsewhere*

```
:verbose set expandtab=4?
```

Will reveal what last set this value. If it's it's anything apart from `.vimrc` (or init.vim) I remove it.  Someone else has done the work for me :)

* If you are removing these, be confident that it won't change or that you have no desire for them to change.
For example I removed `set cscopedb` because it's set in the `gen_tags` plugin. If I ever remove that plugin,
I will need to put the `set` back in. This is a trade-off, keep them in if you want better stability without plugins or
remove them and rely on what's already being set.
