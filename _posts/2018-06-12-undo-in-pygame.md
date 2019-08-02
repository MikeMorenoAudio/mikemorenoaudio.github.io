---
layout: default
tags: programming
---

Today, I got well and truly nerd-sniped into creating a Bomberman-like puzzle game. Here's a very early (1 days work) gif to show you what's been implemented.

![undo in pygame animation](http://i.imgur.com/BLsrPFk.gif)

In that video I've included the topic of this talk...Undo functionality!

## It's actually pretty simple

Atleast, it's way simpler than I thought. Here are the parts you need to see to get an idea of how it works.

Since you're all eager beavers, here's the main undo functionality

```
def update(self, command):
    ...
    elif command == 'u':
        if self.move_stack:
            self.move(keys.opposites[self.move_stack.pop()]) #undo
    else:
        self.move(command)
        self.move_stack.append(command)
        ...
```

And here's how it gets updated
```
def process_input(self):
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        for k,v in keys.keys.items():
            if pressed_keys[k]:
                self.player_group.update(v)
```
Finally, here's how we reverse our actions.
It's kind of hacky but it works. It's just a dictionary giving us the opposite direction of the initially inputted command.
```
keys = {pygame.K_UP:'up',
        pygame.K_DOWN:'down',
        pygame.K_LEFT:'left',
        pygame.K_RIGHT:'right',
        pygame.K_SPACE:'space',
        pygame.K_u:'u'} 

opposites = {'up':'down',
             'down':'up',
             'left':'right',
             'right':'left'} 
```

## How it all works

Firstly, a player enters a command and this calls the players update method,
The players update method is just
```
def update(self, command):
```
Meaning that it takes a command does what it needs to do.
That means that in the line below, we're just feeding our player the keyboard inputs we give it.
```
for k,v in keys.keys.items():
    if pressed_keys[k]:
        self.player_group.update(v)
```
Every move that we give the player gets stored onto a stack.
```
self.move_stack.append(command)
```
Should we ever need to undo an action, we just pop the last item off the stack and get the opposite equivalent of it. Once we have the opposite version, we issue the 'move' method to the player with this opposite command.
```
self.move(keys.opposites[self.move_stack.pop()]) #undo
```

The player then happily goes about doing the reverse of our actions!

# Happy Pygaming :D
