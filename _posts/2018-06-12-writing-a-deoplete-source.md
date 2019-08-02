---
layout: default
tags: programming
---

[Deoplete](https://github.com/Shougo/deoplete.nvim) is a completion engine for [Neovim](https://github.com/neovim/neovim) and [Vim8](https://github.com/vim/vim).

You can write your own completion sources for it so that it can complete anything and everything you had in mind.

We'll walkthrough creating a (very) simple completion source for [vim-minisnip](https://github.com/joereynolds/vim-minisnip), a lightweight snippet manager.

By the end of the article you'll have a source capable of listing your created vim-minisnip snippets.
Check this asciicast for an example of what we'll have at the end.

<script type="text/javascript" src="https://asciinema.org/a/iDJMTBZfmTftp34SuWoPHpGAR.js" id="asciicast-iDJMTBZfmTftp34SuWoPHpGAR" async></script>
## Python

Deoplete sources are written in Python but you can offload the majority of the work to Vimscript (if you're a sadist).
In our example, we go with a 100% Python solution, no Vimscript :D

## Prep

We'll be using [vim-plug](https://github.com/junegunn/vim-plug) to pull in [vim-minisnip](https://github.com/joereynolds/vim-minisnip) and the Deoplete completion engine. Feel free to use an alternative that you're comfortable with (Pathogen, Vundle, Dein etc...). If you've never used any I recommend vim-plug.

(You can also work locally if you want)

Assuming you're going with vim-plug and you already have Deoplete up and running, add vim-minisnip and your Deoplete source to your plugins:

```
Plug 'joereynolds/vim-minisnip'
Plug 'me/my-deoplete-minisnip' 
```

(Note: The original vim-minisnip is unmaintained so I forked it and maintain it, my fork has a few improvements and bug fixes over the original)

Now it's time to get to the meat of the work...

## Creating The Source File

Deoplete looks in a specific directory for the file
In our case it's `rplugin/python3/deoplete/sources/minisnip.py` 

In my case, the absolute path is 
`/home/joe/.config/nvim/plugged/deoplete-minisnip/rplugin/python3/deoplete/sources/minisnip.py`.
### The Code

### Imports

All sources need to extend a `Base` class, so we need to import Deoplete's base class.
Since vim-minisnip relies on files for snippets, we also need a way of reading a directory  so we import the `os` module, and then we're done.

```
import os
from .base import Base
```

### The Class

Call your class `Source` and extend it from `Base` and that's it

```
class Source(Base):
```

### The Methods

There's only two methods in our class, the `__init__` and Deoplete's `gather_candidates`.

Let's go through our `__init__`

#### Init

```
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'minisnip'
        self.mark = '[minisnip]'
        self.min_pattern_length = 0
        self.minisnip_dir = self.vim.eval('g:minisnip_dir')
        self.snippets = os.listdir(self.minisnip_dir)
```

This is almost the bare minimum required so I'll explain each attribute.

`self.name` - Every source requires a name.

`self.mark` - This is what shows up next to the item in the completion menu, you should probably keep this short (I think minisnip might be too long personally).

`self.min_pattern_length` - This is how many characters need to be typed before completion pops up. Since snippets are short by nature, I remove the need altogether. The default is 2 which is too long for my snippets which are things such as `if`, `vd` etc...

`self.minisnip_dir` - This is the minisnip_directory set by minisnip. If none is entered in your vimrc, it looks in `~/.vim/minisnip`. Note the use of `self.vim.eval` this basically calls vim and returns the result.

`self.snippets` - This is a list of all the snippets in our `self.minisnip_dir`.

Now, we'll take a look at our final (and most important) method, `gather_candidates`.

#### Gather Candidates

`gather_candidates` is what returns the items for completion, it must return an array.

You can test this yourself by doing something as simple as
```
    def gather_candidates(self, context):
        return ['Hello from Python!']
```

Now, when you run vim with your plugin enabled you'll see it right in front of you
(image: completion.png)

Of course, you probably want it to be intelligent and semi-useful so let's work out the kinks.

When the `gather_candidates` function is called, it is passed a `context`. The context is injected in automatically by Deoplete and contains some useful information on the current filetype, and other stuff that wouldn't be accessible from Python on it's own.

With that in mind, we grab the filetype (`context['filetype']`). The reason we do this is because minisnip's snippets have the filetype name in them. The filename of a snippet is generally in the form of `_filetype_your_snippet_name`

Here are a few of mine: 
```
_javascript_cl
_javascript.jsx_fnc
_javascript.jsx_test
_php_$
_php_ae
_php_as
_php_vd
_racket_fnc
_racket_let
_sql_add_endpoint
_sql_select
_sql_selwhe
_sql_update
```
With the filename in mind, all we really want to grab is everything after the filetype and the '_'.
So we do this (which I realise is more complicated than it needs to be but life gets in my way :( )

```
filetype = '_' + context['filetype'] + '_'
cleaned = [snippet.split(filetype)[1] for snippet in self.snippets if filetype in snippet]
```

This will return a list of all snippets after the `_filetype_` part of the name.
In the end, our example snippets above would return

```
cl
fnc
test
$
ae
as
vd
fnc
let
add_endpoint
select
selwhe
update
```
Thankfully, vim-minisnip is also filetype aware so it won't show you sql snippets in a php file or vice versa which is nice. You can force it to be on for every file type but I prefer the context aware snippets.

Finally, after successfully extracting the snippet name from the snippet, we just need to return it in a format that Deoplete expects. That can be done like so
```
return [{'word': snippet} for snippet in cleaned]
```

Deoplete uses a dictionary and the `'word'` key you see above. In this case, we return one dictionary for every snippet.

With all of that in mind, our `gather_candidates` function ends up looking like this.
```
    def gather_candidates(self, context):
        """Returns all snippets in the users
        vim minisnip directory"""
        filetype =  '_' + context['filetype'] + '_'
        cleaned = [snippet.split(filetype)[1] for snippet in self.snippets if filetype in snippet]
        return [{'word': snippet} for snippet in cleaned]
```

# That's all folks

I've only scratched the surface of Deoplete, there is a ton that you can do that I haven't covered. see `:help deoplete` for more infomation.

Putting all of what we've done together, we get 20 lines of Python that provide context aware snippet completion. Woo! :D

```
import os
from .base import Base

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'minisnip'
        self.mark = '[minisnip]'
        self.min_pattern_length = 0
        self.minisnip_dir = self.vim.eval('g:minisnip_dir')
        self.snippets = os.listdir(self.minisnip_dir)

    def gather_candidates(self, context):
        """Returns all snippets in the users
        vim minisnip directory"""
        filetype = '_' + context['filetype'] + '_'
        cleaned = [snippet.split(filetype)[1] for snippet in self.snippets if filetype in snippet]
        return [{'word': snippet} for snippet in cleaned]
```

## References

Deoplete:
https://github.com/Shougo/deoplete.nvim

My fork of vim-minisnip:
https://github.com/joereynolds/vim-minisnip

Deoplete-minisnip:
https://github.com/joereynolds/deoplete-minisnip

Some simple sources I learned from:

https://github.com/fszymanski/deoplete-emoji
https://github.com/ozelentok/deoplete-gtags
