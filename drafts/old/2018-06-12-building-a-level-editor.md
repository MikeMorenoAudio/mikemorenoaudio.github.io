---
layout: default
---

Let's go over how to build a (basic) level editor. The editor should be able to 

- Read a text file
- Create a level from a text file
- Return it as something usable to the developer

Thankfully, most of this is made fairly trivial so let's get to it.
Note that some of what I'm showing will need a *slight* bit of modification to get it working in your game.

## The Editor

I'll share the entire level editor code and then we'll go through it line by line

```
import pygame
import tile

spritesheet = pygame.image.load('spritesheet.png')
class Editor():

    """A dictionary containing attributes about each tile
       For example
       'X' : [True,  image]
       
       'X' is the representation of the tile in the text file
        True Is whether the tile is solid or not
        image is the surface of the image if you have one
    """
    tiles = {'X' : [True,  spritesheet.subsurface(166,245,50,50)],
             'O' : [True,  spritesheet.subsurface(509,217,50,50)],
             '#' : [False, spritesheet.subsurface(466,68,50,50)]}

    def __init__(self, _file):
        self.level = open(_file,'r')
        self.level_data = [line for line in self.level]
        self.created_level = pygame.sprite.Group() 
        self.make_level()

    def make_level(self):
        """Appends our Tile objects to  our created_level sprite group"""
        print(self.level_data)
        # Go through each individual tile and check it against our tiles dict
        for y, tiles in enumerate(self.level_data):
            for x, _tile in enumerate(tiles):
                for tile_icon, attributes in Editor.tiles.items():
                    if _tile == tile_icon:
                        obj = tile.Tile(x * 50,
                                        y * 50,
                                        50,
                                        50,
                                        Editor.tiles[_tile][0],
                                        Editor.tiles[_tile][1])
                        self.created_level.add(obj)
```

As we can see the editor just reads a file and returns a pygame.sprite.Group (self.created_level) of objects back to us.
With that out of the way, let's get into the nitty gritty.

#### Tiles and the Tiles Dictionary

The tiles dictionary  is one of the most important things here. Without this, it wouldn't work. In this dictionary are the characters that the editor should create objects from along with their attibutes.

To better understand it, we'll need to look at the Tile class

```
class Tile(entity.Entity):

    def __init__(self, x, y, width, height, solid, image=None):
        entity.Entity.__init__(self, x, y, width, height, image)
        self.solid = solid 
```
As we can see, it's very simple. Infact, half of it is just making sure we call and inherit from the right places! (You don't need to worry about the entity class. We're only looking at the editor for now)
The line we care about is
```
self.solid = solid
```

This just means that if it's solid, when a character walks into it, they will stop. If it's not solid (i.e. a floor, ocean etc...)
they will happily pass through it.

Back to the dictionary...
```
    tiles = {'X' : [True,  spritesheet.subsurface(166,245,50,50)],
             'O' : [True,  spritesheet.subsurface(509,217,50,50)],
             '#' : [False, spritesheet.subsurface(466,68,50,50)]}
```
The ASCII characters in the key of the tiles are what the level editor will read and convert into objects.
The value is a list of attributes that gets passed along when we create an object

value[0] = Whether a sprite is solid or not
value[1] = The pygame.Surface of the image that the object should use

**That's it!**

That means that when we pass a text file that looks like this


XXXXXXXXXX
X###X####O#
X###X####XX
X###X###XXX
X######XXXX
XXXXXXXXXX


We get this in return

(image: http://i.imgur.com/PZF7s9h.png)

## init

```
    def __init__(self, _file):
        self.level = open(_file,'r')
        self.level_data = [line for line in self.level]
        self.created_level = pygame.sprite.Group() 
        self.make_level()

```
The init method of the Editor takes a file to read the level data from (_file) and then gives us all of the data in that file (self.level_data). 

It also contains a pygame.sprite.Group (self.created_level) that we'll be adding our sprites too. Finally, it makes a call to make_level() to fill created_level with some usable values.

All that's left to tackle now, is big momma, the cream of the crop, the boss, you get the idea...

## make_level()

```
    def make_level(self):
        """Appends our Tile objects to  our created_level sprite group"""
        # Go through each individual tile and check it against our tiles dict
        for y, tiles in enumerate(self.level_data):
            for x, _tile in enumerate(tiles):
                for tile_icon, attributes in Editor.tiles.items():
                    if _tile == tile_icon:
                        obj = tile.Tile(x * 50,
                                        y * 50,
                                        50,
                                        50,
                                        Editor.tiles[_tile][0],
                                        Editor.tiles[_tile][1])
                        self.created_level.add(obj)
```

make_level() is as basic as you can get in terms of what it's doing. First we go through the tiles in self.level_data. In this case tiles are actually just characters like 'X', 'O', and '#'
```
        for y, tiles in enumerate(self.level_data):
```

We use enumerate so that we can also have an indices. This is later used to place them evenly spaced (you don't have to do this but I did it as the quickest way of getting what I needed).

Next, we go through each individual tile in the tiles that we just retrieved from self.level_data
```
        for x, _tile in enumerate(tiles):
```

and **then** we go through the key and value of the tiles dictionary. This is a particularly important step, so pay attention!
```
            for tile_icon, attributes in Editor.tiles.items():
                    if _tile == tile_icon:
                        obj = tile.Tile(x * 50,                    # X position
                                        y * 50                     # Y position
                                        50,                        # Width
                                        50,                        # Height
                                        Editor.tiles[_tile][0],    # Is solid
                                        Editor.tiles[_tile][1])    # pygame Surface
                        self.created_level.add(obj)      
```
We go through all the tile_icons in the tiles dictionary, if the tile in the dictionary matches the one we have in our text file of level data, then we can make an object out of it, and add it to our self.created_level sprite group!

Once we've done all that,  we have a nice sprite.Group full of sprites!
```
<Group(64 sprites)>
```

Then, we just pass this sprite group to whatever we need for it to be rendered on to the screen. That's it!

I know it's been a bit of a whirlwind and I apologise for the few amounts of custom code that bare no use for you guys but hopefully this proved useful in some capacity.

Let me know if you have questions!

# Go forth and create!
