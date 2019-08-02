---
layout: default
---

Mr Figs is a turn-based puzzle game based on (link: https://en.wikipedia.org/wiki/Bomberman text: Bomberman).

The player must thoughtfully blast their way through various different levels to reach the end goal of that level!

Here's a gif of the latest gameplay using the newest set of tiles:

![](http://i.imgur.com/0BBv5GG.gif)

## Tools

The following tools are used in Mr Figs

- [Python](https://www.python.org/) 
    - The Python programming language is what the majority of my games are programmed in. I can't see this changing in the foreseeable future but if it does, it will likely be to C# or Js. Note : I currently use Python 3.4.
- [Pygame](http://www.pygame.org/)
    - Pygame is a bunch of modules on top of Python that help with writing games. It's surprisingly low-level and you actually have to do a lot of work yourself (for better or worse),
- [Tiled](http://www.mapeditor.org/)
    - Tiled is the map editor of choice for Mr Figs. It is used for all level design and is extremely rapid compared to other hand rolled methods.

#### More on Tiled

Here are a few gifs/screenshots of Tiled just so others working on the game can get a feel for the workflow of a level.

It's a very simple flow that can be outlined as follows

- Open up Tiled and create a new project.
    - Orientation : Orthogonal
    - Tile Layer Format : CSV
    - Tile Render Order : Right Down

#### Open up Tiled and create a new project

![](http://i.imgur.com/dscASxY.gif)

#### Add a new tileset (in this case, this would be your spritesheet)

![](http://i.imgur.com/wLhWEN5.gif)

#### Make your level. It's drag and drop, very simple.

![](http://i.imgur.com/l0zV6Gi.gif)

#### File -> Export -> LevelX.csv

![](http://i.imgur.com/9279vIS.gif)

#### Send it to me!

{{email}} the assets. Don't forget to also {{email}} the stylesheet itself otherwise Tiled won't find it!



## Art

#### Assets

![](http://i.imgur.com/S36AcdX.png)

This is the original spritesheet for the game. As you can see the focus was on large pixelated graphics. This spritesheet was obtained from opengameart user [BacioiuC](http://opengameart.org/content/miw-assets-strategy-war-game) and then resized by me to 50x50 pixels with some of my poor graphics on top.

You'll note that in that spritesheet (above), there are 3 versions of each sheet.

1. Grass
2. Desert
3. Snow

Similar themes will be present in Mr Figs.
(Also note that I've only actually worked on the desert tiles hence why there are more sprites for that selection)

#### Requirements

These are the minimal requirements of the game in its current state.

- Tilesheets for the following areas
    - Grass 
    - Desert
    - Cave
    - Snow/Ice
    - Castle

Each area must have at minimum, the following tiles

- A ground tile
- A solid object (rock, log,  whatever)
- A destructable object (tree, old wall etc...)
- A threatening object (spikes, traps etc...)


#### Ground tiles

A ground tile is just the tile on the ground (duh), you can't collide with it and you can't destroy it. No animation should be necessary for this although it'd be nice if we could avoid the 'tiling' effect.

#### Solid objects

Similar to the ground tile except you can collide with it. It's impossible to pass a solid object. Again, a few variations of the solid object would be good!

#### Destructable objects

Similar to solid objects except they can be destroyed. These **may** need animating to show there destruction. i.e. if we destroy a brick wall, it should collapse. 
#### Threatening objects

These are different from the rest and will more than likely **have** to be animated. These can be solid or not and also destructable or not. When you collide with it (depending on whatever state it's in) you'll die.

##### Animated Sprites

These tiles currently only have a crude drawing by me, or no animation at all. The following are what will need to be animated.

Each sprite should ideally conists of 6-8 frames of animation in order to make the animation effect as smooth as possible.

Main Character:

- An actual sprite rather than the smiley face I've drawn...
- walking animations in all 4 directions (up, down, left, right)
- a static image for each direction that he could be facing
- A death animation. i.e. when a bomb hits him, an animation should play to indicate this.

Spikes:
At current I have implemented my own very crude animation consisting of 3 frames. Spike down, spike halfway up, and spike up. As specified, this should be 6-8 frames going from the spike fully down all the way to the spike up and then back again.

Bomb:

The bomb itself will need minimum animation (maybe just some enlarging and minimizing to give a 'pulsing' efect') but the particles for the bombs will need animating (flames, sparks, or something similar).

## Audio

#### References

##### Beach

[Pokemon route 1](https://www.youtube.com/watch?v=uXv7DjdasHI)

##### Grass

##### Desert


##### Castle

##### Cave


##### Snow
