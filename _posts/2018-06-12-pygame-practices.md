---
layout: default
tags: programming
---

## Intro

So the resources for (link:http://pygame.org text:Pygame) (online and in book form) are a bit lackluster in terms of code quality.
Yes, they get the job done but if you build a foundation from some of the examples online, you'll be drowning in redundant code before the day is over.

This article hopes to highlight a few decent practices that all pygamers should get to grips with.
Some of this stuff will be basic and obvious, but we'll quickly ramp up.

*most examples have been taken from my newest game (link:https://github.com/joereynolds/Mr-Figs/ text:mr-figs), a turn-based puzzle-game based on Bomberman.*
## Stuff you should be doing

#### Inheriting from pygame.sprite.Sprite

I've seen several codebases that roll their own sprite system but there's a basic one built (link:https://www.pygame.org/docs/ref/sprite.html text:right into pygame!)
inheriting from it gives you access to...

- Collision detection
- Sprite groups (very useful!)
- Layering
- and a few other things that are nice to have

```
class Actor(pygame.sprite.Sprite):
```
Do it.

#### Using rects with your sprites

Sprites aren't nearly as useful if you don't use (link:https://www.pygame.org/docs/ref/rect.html text:rects). Pygame's rects allow for collision detection, resizing, growing/shrinking, clamping, and a few other nice to haves.

It's really simple to start using rects, this should get you started
```
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.rect = self.image.get_rect()
```

#### Using sprite groups (and layered updates)

Sprites groups are exactly that, a grouping of sprites. Rather than keeping track of each individual sprite you can group them logically.

For example, if you have 100 enemies on the screen and they're in a group, you can do this
```
enemy_group.draw(surface)
```
If they're not a in group, you'll have to do this  ):
```
for enemy in my_enemy_array:
    enemy.draw(surface)
```
I don't use groups too liberally personally. I mean, I *only* use sprite groups, but I don't go crazy with 10 + different groups. I usually have a Sprite Group per level.

#### Convert()ing surfaces
The Pygame docs even say it themselves
```
This [convert()] is always the fastest format for blitting. 
It is a good idea to convert all Surfaces before they are blitted many times.
```
So remember
```
self.image = pygame.Surface([50,50]).convert()
```
Or if you need alpha transparency
```
self.image = pygame.Surface([50,50]).convert_alpha()
```
#### Learning the tools of the trade

##### Tiled
(image: http://www.mapeditor.org/img/tiled-logo-white.png link: http://www.mapeditor.org/)
Take the time to research some decent tools that might be available before you embark on your game.
There's one tool I swear by, and that's (link:http://www.mapeditor.org/ text:Tiled). Tiled is a map editor for 2d games and the levels get exported to program neutral data formats so it doesn't matter what language you program in, Tiled *will* work for you.

Tiled exports down to its own native format called '.tmx' which is basically XML. In order to parse it, I highly recommend (link:https://github.com/bitcraft/PyTMX text:PyTMX). It saves you rolling your own version and it does everything you were probably going to program anyway.

Not only does Tiled help you make levels quicker, it also helps separate the actual level data (i.e. what goes where) from the rest of your program.

Here's a few lines to get you started

Loading the map
```
import pytmx
tmxdata = pytmx.TiledMap("map.tmx")
```
Going through the map
```
for layer in tmxdata:
    for tile in layer.tiles():
        # do stuff with your tiles
```
Accessing custom properties
```
for layer in tmxdata:
    for tile in layer.tiles():
        if tile['solid']:
            #collision handling!
```

##### Pylint
(image:http://www.pylint.org/pylint4.svg link:http://www.pylint.org)
A linter is a program that spots code smells in your code. It looks for things like
- lines that are too long
- code that could be refactored
- bad style
- and lots more

The first time you use it, it'll hurt your feelings, here's why
```
Global evaluation
 --------------------
Your code has been rated at -0.27/10 (previous run: -0.27/10, +0.00)
```
The more you use one, the more conformant your code is. This means that when another developer works on your stuff, they'll be delighted to see that all of your code scored 10/10 during linting :D

It's even better when you can automate the linting process. For example, as soon as I save a .py file, Pylint runs on the file I was just editing. This is very handy when I'm being especially nitpicky. Here's what that looks like (I'm running Vim)
```
:autocmd BufWritePost *.py !pylint <afile>
```
All that says, is when we write to the file (BufWritePost), on a python file (*.py), run pylint and feed our current file as the argument to it.

You get a whoooole load of info back from pylint so you may want to supply it some arguments so that it gives you a bit less information.

#### Thinking granularly
The more granular your code is,  the less intertwined it is with everything else.

Here's a snippet of code to show you what I mean:
```
def __init__(self, x, y, width, height, level, image=None):
    ...
    self.input_handler = player_input_handler.PlayerInputHandler(self)
    self.collision_handler = collision_handler.PlayerCollisionHandler(self, self.level)        
    ...
```
Doing this, if I decide ( for some reason ) to be able to control 5 players all at once, I can just give them the (link:https://github.com/joereynolds/Mr-Figs/blob/master/src/input_handlers/player_input_handler.py text:PlayerInputHandler) and (link:https://github.com/joereynolds/Mr-Figs/blob/master/src/collision_handler.py text:PlayerCollisionHandler) class!

I don't have to write collision and input logic all over again for a very similar use case.
You'll find that the more granular you go, generally, the more maintainable the codebase will become.

#### Separate your views from your logic

This is something that I've taken from the web world. It makes the entire process a lot easier. Not only does it split up the domains, it also allows someone else to work on one part of your code whilst you work on another.

For example, if you had it split out into logic, and view, you could have a super amaze-balls UI designer
working on how it all should look and then **you** could be working on the logic side of the actual game!

Here are some examples of logic to give you an idea
- Input handling
- Collision handling
-  A 'player' class 
- A 'gun' class

Here are some examples of 'views' 
- How buttons should be layed out on a window
- What icons are present on the window
- What colour the icons are
- What text is present on buttons

I don't know of many frameworks for Pygame that go about separating these two so you *may* have to do a bit of experimenting to see what works best.

I've taken the approach of XML for my views and then usual Python for all my logic.
For example, this is what my start menus now look like
```
<?xml version="1.0" encoding="UTF-8"?>
<container>
    <components>
        <component x='350' y='100' width='100' height='50' type="gui_base.Clickable" name="start-game">
            <text>START GAME</text>
        </component>
        <component x='350' y='200' width='100' height='50' type="gui_base.Clickable" name="exit-game">
            <text>EXIT GAME</text>
        </component>
        <component x='350' y='300' width='100' height='50' type="gui_base.Clickable" name="settings">
            <text>SETTINGS</text>
        </component>
        <component x='350' y='400' width='100' height='50' type="gui_base.Clickable" name="level-select">
            <text>LEVEL SELECT</text>
        </component>
    </components>
</container>
```
Not the cleanest but it's much better than having all of that mixed in with my actual logic!
There's no reason this couldn't even be done in Tiled rather than rolling your own format!

I will also say (again...heh) that Tiled is great at removing display information from the core of your game.

#### Config files
Whilst not Pygame related, config files are a great way to keep important information accessible to all of your program. The only important thing to do here is to not put unnecessary information in your file. Here's what the config file for mr-figs looks like
```
"""Global configuration options for the game"""
# Directories
spritesheet_location = '../data/newtiledsheet.png'
layout_location = 'scenes\layouts\\'
level_location = '..\\levels\\tmx\\'
```
and that's it. The reason these are in a config file, is, wait for it... They're configurable!
If you decide that you want to move all of the levels of the game elsewhere, just change the 'level_location' variable to reflect that.

Of course, be careful what you put in your config file. You don't want to be putting these sort of things in
```
enemy_colour = ((255,0,0))
enemy_health = 100
```
Those sort of things should go in their related classes.

If you really wanted to take it further with your config file, you could separate it out into a readable YAML or TXT file so that non-pythonistas can read and understand it too.

#### Reading the docs.

There are some good gems in (link:https://www.pygame.org/docs/ text:Pygame's documentation), that you may be unaware of if you only follow tutorials. One of my favourites is the transform module which allows for scale and rotation of sprites. 

Not only that, but most pages in the documentation have some good technical ramblings which will help you understand what's going on at a deeper level.

#### Resources

Here are some decent resources I recommend. Some won't be Pygame, or even Python based but they're general enough for you to port over to your code

- (link:https://github.com/Mekire/pygame-samples text:Mek's repo) - A great repo full of small examples of code
- (link:https://github.com/joereynolds/Mr-Figs text:Mr Figs) - The repo to Mr Figs.
- (link:http://gameprogrammingpatterns.com/contents.html text:Game Programming Patterns) - A book on some design patterns particularly suitable for game development
- (link:https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller text:MVC) - Wikipedia's definition of MVC. i.e. the logic/view stuff I was going on about
