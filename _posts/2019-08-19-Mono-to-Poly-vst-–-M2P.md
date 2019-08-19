---
layout: default
tags: [plugins, portfolio]
---
# M2P

**Mono to Poly (M2P)** turns monophonic synthesizers to polyphonic using pitch shifters and MIDI data.

Most synths have MIDI to keep track of what notes you are playing.
So by receiving that MIDI data you can harmonize in real-time the notes that aren’t playing, thus making your synth polyphonic with M2P.

<center><p><h2><a href="https://patchstorage.com/m2p/"> Download M2P 1.1 at Patchstorage </a></h2></p></center>

## Video Demo

<p><div class="video-container"><iframe width="853" height="480" src="https://www.youtube.com/embed/7d3IagGN50E" frameborder="0" allowfullscreen></iframe></div></p>

## Installation Guide
To install please read the instructions on [how to install a Camomile plugin](https://github.com/pierreguillot/Camomile/wiki/How-to-install-plugins).

## Ableton Live Routing

M2P is an instrument plugin, so we need two tracks in to make it work:
* One MIDI track receiving MIDI output from your synth
* One Audio track receiving the Audio output from your synth.

After that we need to route the audio from our synth to M2P like this:

![Ableton Live Routing](/assets/images/2019-08-19-Ableton-M2P.png)

It is also important to be sure both tracks have the Monitor option at In.

Finally, M2P needs to have the same Note Priority parameter as your synth.

For example, the Korg Monologue has Last Note Priority so we set M2P’s Note Priority to Last.

![M2P GUI](/assets/images/2019-08-19-M2P-GUI.png)

And that’s it! Enjoy real-time polyphony!

<iframe src="https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2FholaWave%2Fvideos%2F299898077356474%2F&show_text=0&width=267" width="267" height="476" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allowFullScreen="true"></iframe>
