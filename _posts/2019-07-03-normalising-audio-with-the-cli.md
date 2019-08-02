---
layout: default
tags: [music, programming]
---

# Normalising audio with the CLI

## Backstory

Recently I've been learning [Pure Data](https://puredata.info/), a visual
programming language for creating music. One of the things I consistently screw
up is correct signal control around volume. As a result, there are some
videos/patches I post of my Pure Data findings that have inconsistent volume
from patch to patch.

To hack around this (the correct way is to use Pure Data properly), I use a
combination of `sox` and `ffmpeg`, read on!

## Normalisation

The easiest way to normalise audio is with [SoX](http://sox.sourceforge.net/),
it just works™.

Let's say you have a quiet audio file with a tolerable signal-to-noise ratio,
you can do the following:

```
sox --norm my_file.wav my_normalised_file.wav
```

And that's it, you'll now have a normalised wav file.

## Changing file formats

What you might find is that a file format you want to normalise isn't
supported by SoX.  For example, SoX doesn't work with mp3's out of the box so
you need to transfer your file to a format that SoX does work with.

Enter `ffmpeg`...

`ffmpeg` is another life changing program that you should learn about. Changing
file formats is as simple as:

``` 
ffmpeg -i my_file.mp3 my_file.wav 
```

And now you have a wav file.

There are also dedicated tools for audio normalisation that I came across such
as [ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) but I find
`ffmpeg` and `sox` ubiquitous enough to not need another third party solution.

