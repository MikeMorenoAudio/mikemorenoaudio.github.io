---
layout: default
tags: portfolio
---
# Kessler I (2018)

![Kessler I](/assets/images/2019-08-06-kessler-i.jpg)

> "Kessler I" from the "Kessler Syndrome" series
> By Ernesto Walker

> Sculpture / Sound Installation (850 x 400 x 200 cm)
> Exhibited at Monterrey’s Museum of Contemporary Art

Kessler Syndrome is a series of sculptures that reflects on the current state of telecommunications and their effects on how we exchange information.

In 2018 Ernesto Walker contacted me to create a Pure Data patch for his sculpture that could automatically identify and record voices on the exhibition room so they could be played back on a radio transmitter.

The first tests of voice activity detection (VAD) were successful in a controlled environment with a combination of volume threshold using the `[env~]` object and zeroCrossing threshold using the `[zeroCrossing~]` object from William Brent’s timbreID library.

There were plenty of obstacles at the museum given the room’s reverberation, hums and incidental noises. The most prominent issue was the constant hum made by the sculpture’s computer passed through vibration. This was solved by analyzing the background noise and using a series of high-pass and notch filters on the respective frequencies. The reverberation issue was somewhat solved with the use of a noise gate and expander.

## References

* Alexandros Drymonitis, ["Miscellaneous Abstractions"](https://github.com/alexdrymonitis/miscellaneous_abstractions/)
* Ernesto Walker, ["Kessler I"](http://www.ernestowalker.com/I_E/KesslerSyndrome.html)
* William Brent, ["timbreID"](https://github.com/wbrent/timbreID)
* Wikipedia, ["Voice Activity Detection"](https://en.wikipedia.org/wiki/Voice_activity_detection)
