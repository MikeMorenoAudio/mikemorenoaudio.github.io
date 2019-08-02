--- 
layout: default 
tags: [music, programming]
---

# \#2
![pure data patch 2](https://i.imgur.com/05KukDb.jpg)

A slightly more musical patch this time.

This one's based around a modulated square wave (`phasor~ 110`, `phasor~ 111`) in A.

The melody is based around a random selection of notes in an A minor chord with an Eb thrown in for dissonance (`A C E Eb`). Each note from the chord is then delayed (`delwrite~`), low-passed (`lop~`) and sent to the left output.

The 'snare' and 'hi-hat' are filtered white noise. A low-pass (`lop~`) of 5k is applied to the snare, a high-pass (`hip~`) of 6k is passed to the hi-hat.

Next time, envelope generators with the `line~` object experimenting with some data and converting it into
something musical. Either that or some more drums.
