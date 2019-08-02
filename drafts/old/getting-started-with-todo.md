---
layout: default
tags: programming
---

# Getting started with todo.txt 

Let's go through the workflow of having todo.txt working on all of your devices.
I originally used Google Keep but the 'contexts' and ease of tagging in todo.txt
made me curious and now I've switched over full time.


# Putting it all together

1. Download Dropbox

We need this if we plan to sync across more than one machine, I recommend
installing it on your phone if you plan on using todo.txt on mobile too.

There are alternatives to Dropbox for todo.txt if you want, in fact, you can
manage the syncing et al. yourself if you'd rather have full control (I wouldn't).

2. Clone down the todo repo of your choice

There's a few different ways you can manage your todos.

- With nothing.
  todo.txt is just a text file, so you're welcome to manually edit it.

- With the CLI.
  https://github.com/todotxt/todo.txt-cli
  There is a wrapper for todo.txt to be used entirely through commands, I tried
  it but I prefer just editing it manually.

  ```
  make
  make install
  make test
  ```
(All should pass)

- With a GUI    
  [QTodotxt]() is a decent cross platform GUI for the todo.txt format.


I use a hybrid approach of editing the file manually and using the GUI.
When I use the GUI it is purely to look at the tasks as they're easier to
process visually rather than from the terminal.

3. Edit the `~/.todo/config` file to work with the dropbox directory
(In my case I'm also using Simpletask so I can use it on mobile hence the
directory structure below)


```
mkdir ~/.todo

echo "
export TODO_DIR="$HOME/Dropbox/Apps/Simpletask"
export TODO_FILE="$TODO_DIR/todo.txt"
export DONE_FILE="$TODO_DIR/done.txt"
export REPORT_FILE="$TODO_DIR/report.txt"
export TMP_FILE="/tmp/todo.tmp"
export TODOTXT_DEFAULT_ACTION=ls
" > ~/.todo/config
```

4. Download Simpletask Dropbox/Cloudless

This is the mobile app that will read your todo.txt in the cloud.
It's also a nice UI wrapper around the list itself so you can add, delete,
filter and do other stuff to your lists.

# Caveats

Google Keep is easier, much easier. 
While todo.txt does 'just work', getting it cross platform and across devices is
a mish mash of different applications that are not smoothly integrated.

