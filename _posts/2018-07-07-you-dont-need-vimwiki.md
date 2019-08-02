---
layout: default
tags: programming
---

# You (probably) don't need Vimwiki

Why are you using [Vimwiki](https://github.com/vimwiki/vimwiki)?
Probably to make notes, right?

Well did you know that you don't need a plugin for this?
Of course you did!

Let's go through some of Vimwiki's features and dispel them in place of vim alternatives.
Vimwiki states the following features:

## 1. Organise notes and ideas

When I used to use Vimwiki, I loved the ability to link files to each other but I have two letters for you; `gf`. `gf` allows you to edit the file under the cursor (assuming it's in your path). (see `:help gf`)

With a sensible directory structure, you can easily organise your notes and ideas. Take a look at [my repo](https://github.com/joereynolds/life) and come back here when you're done.  That repository is just a dumping ground of articles that I may or may not write at some point but the point is,
it's entirely navigable with vim.  
The directory structure is:

```
README.md   
docs/
  article-1.md
  article-2.md
  article-3.md
  article-4.md
  index.md
```

`README.md` is the 'entrypoint' that most devs would open up straight away and contains a link to our main page, `index.md`.

`index.md` is just a table of contents hyperlinking to all other articles and looks like this:

```
- article-1.md - A description of what article-1 is
- article-2.md - A description of what article-2 is
- article-3.md - A description of what article-3 is
- article-4.md - A description of what article-4 is
```

From here, you can easily browser articles by pressing `gf` to edit the file your cursor is on.

I usually use the jumplist (`<c-o>`, `<c-i>`, see `:help jumplist` for more) to go back and forth
between the article and index page.

## 2. Manage todo lists

I am a big todo list fan but that is one thing that I do not use vim for.

There's a few different kinds of TODO lists, and I treat them differently:

### TODOs in code

There are two approaches I take to this:

1) Make your TODO a github issue (The formal approach).

This allows everyone to see it and I find the best and easiest way to track
things. It's what I do with all of my projects. (Here's an [example](https://github.com/joereynolds/mort/issues))

If you're averse to issue tracking, you can still track them in a separate file
if that's what you're into.

```
grep -Ri todo . > todos
```

2) Scatter TODOs everywhere and consolidate afterwards (The informal approach).

If you have TODOs such as `// TODO make this polymorphic`, then the easiest
thing you can do to consolidate these is just grep for them in your project.

```
:grep todo
```
(Your mileage may vary depending on your grepprg, see `:help grepprg`)

### TODOs in life

I am a big fan of todo lists and mine are constantly changing.
So much so that having them in a versioned text file would be impractical, for this I use Google Keep.

If you're adamant on using Vim, I like a good old fashioned bulleted list and nothing more.

```
# TODO  
- Pay bills
- Write "You don't need Vimwiki article"
```

To me though, this just sounds awkward.

## 3. Write documentation

There are two thoughts that go through my mind with this one:

1) You can easily write documentation in any editor, 
   you don't need Vimwiki or anything else. 
   Infact, I'm not sure what Vimwiki brings to the table here (Ironically, there was nothing in their documentation).

2) I would prefer something built for this purpose such as [readthedocs](https://readthedocs.org/) 

## 4. Maintain a diary

Ok, Vimwiki wins here, I have no idea how you'd do this without too many lines of vimscript.

## 5. Export everything to HTML

Again, two points here:

1) The entire point of markdown is that it's easily editable and readable as is, 
   write your notes in markdown and you won't even need to render it to HTML.

2) If you want to render stuff to HTML, just use [pandoc](https://pandoc.org/) its entire purpose 
   is converting files from one format to another and will do what you need here.

   A mapping to convert the current markdown file to HTML could look like:

   ```
   nnoremap <leader>r :!pandoc % --to=html5 > %.html
   ```

## Other stuff    

### Tags

Vimwiki boasts that you can 'tag' pages, well, this is pretty easy depending on how you want to do it.

You could either tag pages on the index page, or on the post itself.
If we were to tag our index page, it might look like this
```
- article-1.md - A description of what article-1 is [programming]
- article-2.md - A description of what article-2 is [vim, programming]
- article-3.md - A description of what article-3 is [sql]
- article-4.md - A description of what article-4 is [programming]
```

Then you can just use `vimgrep` or `lvimgrep` to search for your tags.
In our case, looking for the `vim` tag would look like:

```
lvimgrep '\[vim.*\]' %
```

And now we have all pages tagged `vim` in our location list and we can `gf` to the article in that location list.

## This is too much work    

If you think all of what I've said is just the hard way around, then continue using Vimwiki.
