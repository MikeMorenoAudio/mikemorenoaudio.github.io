---
layout: default
---

We'll be talking about modular inputs today, to me this means

- Any player can have their own custom keybindings
- Menus can have different keybindings per scene
- You can share different inputs with different components (i.e. A player can for whatever reason, also have the menu's inputs)

In order to do that, we need to...

## Abstract the inputs

Traditionally, you probably will have written code that looks like the following

```
for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key == K_UP:
            snake.move(UP)
        elif event.key == K_DOWN:
            snake.move(DOWN)
        elif event.key == K_LEFT:
            snake.move(LEFT)
        elif event.key == K_RIGHT:
            snake.move(RIGHT)
```

Now, there's nothing inherently wrong with this approach if it's a basic single player game, but when your games start to get a bit more involved, you might want to think about breaking it out.

For instance:
What if we have a 2nd player? Do we now have `snake2.move(RIGHT)` put on all of these conditions too?
How do we make sure that menus are easily navigable, are we going to need an `if` for every keypress?

The first concept we need to get grok is that input handling should be abstracted and not contained within the game's main loop.
The main loop should look as simple as:

```
while not self.done:
    scene.process_input()
    scene.update()
    scene.render()
    pygame.display.flip()
```

We can solve the problem of abstraction quite easily. Read on!

### Player Inputs

First we move that input handling in the `main()` function into its own input handler class.

```
import pygame

class PlayerInputHandler():
    """Handles all input processing for players."""

    keys = {
        pygame.K_UP:'up',
        pygame.K_DOWN:'down',
        pygame.K_LEFT:'left',
        pygame.K_RIGHT:'right',
        pygame.K_SPACE:'space',
    }

    def __init__(self, player):
        self.player = player

    def process_input(self, event):
        for key, action in PlayerInputHandler.keys.items():
            if event.key == key:
                self.player.event_update(action) #Process your action how you like in your player's class
```

And then we can instantiate it in the Actor/Player class (or dependency injection if you prefer)

```
import input_handlers.player_input_handler as player_input_handler

class Actor(pygame.sprite.Sprite):

    def __init__(self):
        self.input_handler = player_input_handler.PlayerInputHandler(self)
```

Now, in our main loop, all we need to do is

```
def process_input(self):
    for event in pygame.event.get():
        self.input_handler.process_input(event)
```
Notice that we're iterating over out events **outside** of the input_handler. This is so we can later have multiple input handlers
and not needlessly iterate over the events many times. They all receive the same events.

Note that we could actually go further and make the input handler fully configurable if we wished:

```
import pygame

class PlayerInputHandler():

    def __init__(self, player, up, down, left, right):
        self.player = player
        self.keys =    {
        up: 'up',
        down: 'down',
        left: 'left',
        right: 'right',
        space: 'space',
    }

    def process_input(self, event):
        for key, action in self.keys.items():
            if event.key == key:
                self.player.event_update(action) #Process your action how you like in your player's class
```

You should decide which one you want, a slightly more modular yet bloated class which allows you to customise keybindings, or a rigid class that does one thing and one thing only.

### Menus

The next problem we want to solve is context sensitive keybindings.
i.e. How can the hotkey 'p' mean 'play' on one screen and 'pause' on another?

Well, I've already given the answer, abstraction!
Except this time it goes a bit further.

Let's say you have 2 scenes: a Menu, and a Level.

In the menu you press P to Play the game, and in the level you press P to Pause the game.
In this case, what we need to do is create an input handler per scene and then pass that input handler through to the scene's class.

Let's go through the input handlers first since we're already familiar with them.

#### Main Menu Input Handling

The main menu will need its own input handler so that it's completely isolated from any other keypresses.

```
import pygame


class StartMenuInput():
    """Handles all inputs for the game itself
    anything related to menu navigation etc...
    is kept in here."""

    def __init__(self, start_menu):
        """
        self.keys is a list of keybindings for each scene
            pygame.K_p: 'level-1',
        Simply means that when we press 's' we will be taken to level-1
        """

        self.start_menu = start_menu

        self.keys = {
            pygame.K_p: 'level-1'
        }

    def process_input(self, event):
        if event.type == pygame.KEYDOWN:
            for key in self.keys.keys():
                if event.key == key:
                    self.start_menu.switch_to_scene(self.keys[key])
```

Then, we need to pass this to our scene class (I'm making the assumption here that every scene is a class in your codebase).

```
import input_handlers.start_menu_input_handler as input_handler

class StartMenu():
    """Initial start menu at the start of the game"""

    def __init__(self):
        self.start_menu_input_handler = input_handler.StartMenuInput(self)
        
```

#### Level Input Handling

The actual game will also need its own input handler

```
import pygame


class InputHandler():
    """Handles all inputs for the game itself
    anything related to menu navigation etc...
    is kept in here. All player input is handler
    via the PlayerInputHandler class"""

    def __init__(self,  level):
        self.level = level

        self.keys = {
            pygame.K_p: 'escape-menu',
        }

    def process_input(self, event):
        if event.type == pygame.KEYDOWN:
            for key in self.keys.keys():
                if event.key == key:
                    self.start_menu.switch_to_scene(self.keys[key])
```

You'll notice that once you've done this, it looks identical to your menu class. If patterns start to emerge like they have here, I'd suggest deriving both of these from a base class that share this functionality.

Here's our scene for our level

```
import input_handlers.input_handler as input_handler


class LevelBase():
    """All levels use this class as the base level.
    So far (probably because it's huge), there has
    been no need to extend this class."""

    def __init__(self, file, next_level):
        self.input_handler =  input_handler.InputHandler(self)
```

Here's a question for you now though...
If the input handling for the level is all contained in that level input handler, how are we going to update our player input handler?
I thought we could only process one at a time?
Well, We just pass both of our input handlers to an abstracted `process_input()` which will call both

```
def process_input(self, event):
    """Processes input for everything. Note that
    in certain cases we are only processing input if a key has
    been pressed. No need to process something unless needed"""
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.KEYDOWN:
        self.player_input_handler.process_input(event)
        self.level_input_handler.process_input(event)
```

## Final words

The abstractions I've mentioned above are useful, but only **if** you need them. They come at the cost of redundancy, more files, more code and more things to remember.
Simple and easy to understand code wins every time.

I have implemented all of the patterns mentioned in my own game [Mr-Figs](https://github.com/joereynolds/Mr-Figs/). If you're struggling to understand this article from the slim code examples, just browse the source code of my game :)

## References
- [Mr-Figs](https://github.com/joereynolds/Mr-Figs/)
    - To see this in a semi-complete state, you can check out my game, , a turn-based Bomberman inspired puzzler. It implements all of the patterns above.
- [Game programming patterns](http://gameprogrammingpatterns.com/)
    - An excellent book on game design patterns. This article is basically an expansion and pygame centric version of his Components chapter.

----

Tags: programming
