---
layout: default
tags: misc
---

#### [animals.txt](/assets/data/animals.txt)
2081 animals. Again, scraped by myself with similar methods to extracting all the pokemon.

#### [countries.txt](/assets/data/countries.txt)
An alphabetized list of 196 countries.

#### [enable1.txt](/assets/data/enable1.txt)
The trusty enable1.txt. This seems to be the most common file that will pop up on the internet if you search for a wordlist.

#### [ffvii.txt](/assets/data/ffvii.txt)
List of all the monsters (and bosses!) from the great Final Fantasy VII.

#### [planets.txt](/assets/data/planets.txt)
A list of 19,000 minor planet names, from Aberghaiz to Zyskin!

#### [plants.txt](/assets/data/planets.txt)
620 families of plants.

#### [plantsgenera.txt](/assets/data/plantgenera.txt)
14,000 + plant genera

#### [pokemon.txt](/assets/data/pokemon.txt)
Complete list of all pokemon up to the current series (whatever that is) scraped by yours truly.

Here's the main part of the code :
```
pokemon = $('.wikitable').find('td:nth-child(2)');
$.each($(pokemon), function(){ 
    console.log($(this).find('a').attr('title')); 
});
```
jQuery  is magic, I swear...

#### [royalnavyships.txt](/assets/data/royalnavyships.txt)
A list of all British navy ships scraped from Wikipedia.

#### [synonyms.txt](/assets/data/synonyms.txt)
I found this backed up on a hard-drive from a while ago, I'm completely unaware of its origins.
I have no idea what it is but looking at it, it looks like a list of words in the following scheme:

**Word : Classification**

Could be useful to some people?

#### [wordlist.txt](/assets/data/wordlist.txt)
This originated from the AutoHotKey community and basically serves as a much bigger enable1.txt
