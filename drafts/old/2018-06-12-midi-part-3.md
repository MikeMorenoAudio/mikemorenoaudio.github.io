Title: Building A Midi Parser Part 3

----

Text: 

We've covered a lot of ground recently but we still have a lot to cover. Here's a small list of what I'd like to have done.

- Grab the tempo of a MIDI file
- Get each tracks length
- Get the time signature
- Get note event information
- Get key signature information

Now obviously, there's a difference between what I'd like to have done and what I can do. Getting some of this stuff I imagine is going to be a nightmare. Nonetheless we'll plough on.

## Debugging

In your absence I've coded a few helper functions to speed up debugging and testing, nothing too complicated but I'll share it since I have shared everything else up to this point.

The first thing is a hacky list comprehension which grabs every midi file in the current directory, this saves me manually typing in every file name:
```
midi_file_list = [file for file in os.listdir() if file.endswith('.mid') or file.endswith('.Mid')]
```
The next thing is a debug method within our Midi class:
```
    def debug(self):
        """Prints all available information about the MIDI file"""
        for event in TEXT_EVENT.keys():
            print(event)
            print (self.get_text_event(event))
            print('='*30)
```
As you can see, it just iterates through every possible event in the TEXT_EVENT dictionary and neatly prints the results. Since I was doing this quite a lot before, it made since to make it a function (for the time being).

I also have the Midi class calling our debug method as soon as we create an instance of that class:
```
    def __init__(self,filename):

        self.filename = filename
        self.midi = open(self.filename,'rb')
        self.debug()
```
Lastly, I made a function which traverses all the MIDI files and then debugs them:
```
def test():

    for file in midi_file_list:
        print(file)
        print('-'*30)
        a = Midi(file)
        print('='*40)
        print('#'*40)
        print('='*40)
```
Now, for any information, all I have to do is type 'test()', and I'm greeted with information on as many midi files as are in that folder at that time.
The majority of these functions will be removed once I have everything working but right now, we're going to need them.

## Fetching Key Signatures

Now that we have that out of the way, let's carry on with parsing this MIDI.

On the top of my to-do list right now is getting the tempo, and the key signature of a track. Since I'm still reading up and scratching my head over the whole tempo thing, we'll go with the latter. The key signature is denoted by the following bytes:
```
'FF 59 02 sf mi'
```
- sf is the number of (s)harps or (f)lats in the key.
For example if 'sf' was set to '-1', there'd be one flat in the key signature which would be F major. 'sf = -3' would be 3 flats in the key signature (Eb major).
It follows this pattern all the way down to -7 (7 flats).

For sharps, we go the opposite way, sf = 1 denotes that there will be 1 sharp in the key signature which would be G major/Eminor.
Again, this goes all the way up to 7 sharps.
Therefore the total range is -7 to 7.

The next byte is 'mi'. I think this stands for minor but that's just a guess. if mi is set to 0, then it is a major key. If it is set to 1 , then it's a minor key

So...
FF 59 02 01 00
Would mean 1 sharp in a major key(G major).
The minor equivalent would be:
FF 59 02 01 01
Which says 1 sharp in a minor key

Parsing this shouldn't be too tricky but I've seriously been considering coding some more helper functions for the lower level byte/hex stuff.
For now, we'll carry on as we are, see where we end up, deeply regret it, swear loudly and then admit defeat.

Thankfully it looks like our get_text_event() function will be able to handle this! We just need to add in the key signature value into our dictionary and it should return the expected results. This is what our dictionary now looks like:
```
TEXT_EVENT = {'comment'   :b'\xff\x01',
              'copyright' :b'\xff\x02',
              'track'     :b'\xff\x03',
              'instrument':b'\xff\x04',
              'lyric'     :b'\xff\x05',
              'key'       :b'\xff\x59'
              } 
```
The last value is our key signature and as you can see, it ignores the amount of sharps and flats and also whether it's major or minor. Now that we've done this, we should test it out and see what we get.
```
test()
```
And here are a few outputs of the key signatures I've gotten so far:
```
[b'\x02\x00']
[b'\x00\x00']
[b'\xfc\x00']
[b'\x03\x00']
```
Okay, so it looks like it's working, although they all seem to be in major and not minor but that's not our fault. Let's run through each output in this list to nail the point home.
```
[b'\x02\x00']
```
This is the key of D major.
We have 2 sharps ('\x02') and it's in the major key denoted by 0 ('\x00').
(I know for a fact that this is right because I purposefully downloaded some D major songs to confirm if the function was working.)

Our next key is C major:
```
[b'\x00\x00']
```

When you're getting key signatures, you're going to see this key a lot for a number of reasons.

1. The majority of songs are written in it
2. If you don't provide a key signature, some software inconveniently marks it as C major (probably because that's the best bet) by default.

Either way, this messes with our key signatures a bit but we can't really avoid it. You'll have to use your intuition on whether you think a song is in C major like it says or if the signature is wrong. If software doesn't mark it as C major, then there will be no key signature event and you'll simply receive no information back whatsoever which is arguably more useful than getting the wrong key.

Next we'll look at a more unusual example:
```
[b'\xfc\x00']
```
This byte string denotes the number 252 which at first seems completely wrong.
Given the fact that I said the range of key signatures is between -7 to 7 you're probably wondering why the hell a number as big as 252 is in there.
I can only hazard a reasonably educated guess about why, and here's my opinion.
Since there's no notation of a negative number in MIDI, they start from the highest number and count backwards, so where 0 is equal to 0 sharps or flats, 255 is equal to -1 flat.
Knowing that, if we go further down we get the following sequence of numbers:
FF = 255 = -1
FE = 254 = -2
FD = 253 = -3
FC = 252 = -4
FB = 251 = -5
FA = 250 = -6
F9 = 249 = -7
The number in our byte string is 252 which corresponds to -4 which means 4 flats. Thankfully this pairs up well with the sample track I used!

The string b'\xfc\x00' was taken from Pharell's 'happy' which is in F minor or Ab major which has...4 FLATS. On that assumption we can say that this is how MIDI key signatures are denoted.

Lastly, we have a nice easy sample in A major:
[b'\x03\x00']
## MayKiNG itt l3gibul

Now that we can extract the keys, we should probably start working on converting them into a neater format since no one really wants to be reading Ab major as 'xff\x59\xfc\x00'.

Let's work on a function that will do this for us. we'll have to create a dictionary of major and minor keys to reference and then we'll be off.
Here's our dictionary of major/minor key mappings :
```
KEY  = {0:['C','A'],
         1:['G','E'],
         2:['D','B'],
         3:['A','F#'],
         4:['E','C#'],
         5:['B','Ab'],
         6:['F#','X'],
         7:['Db','X'],
         255:['F','D'],
         254:['Bb','G'],
         253:['Eb','C'],
         252:['Ab','F'],
         251:['Db','X'],
         250:['Gb','X']}

TONALITY = {0:'Major',
            1:'Minor'}
```
These are our tables and I'll explain briefly what's going on. The number in KEY represents the number of sharps or flats, and then the letters on the other side correspond to its major or minor equivalent. This will make more sense once you see the function to change the bytes into a legible format. Below is our function.
```
def get_key(self):

    try:
        key_bytes = self.get_text_event('key')
        sf = key_bytes[0][0]
        mi = key_bytes[0][1]
        key = KEY[sf][mi],TONALITY[mi]
        return key
    except IndexError: return 'No key information'
```
Let's go through this line by line and see what's going on.

We'll use the Pharell key as an example:
```
'xff\x59\xfc\x00'
```
First we do some error-catching. For the songs that have no key information, they throw us an IndexError, so it's important to catch this so we can carry on fetching the rest of the MIDI data anyway.

secondly we set the variable 'key_bytes' to get_text_event('key'). This means that we're setting 'key_bytes' to the byte string that denotes key. This byte string look like this:
'\xfc\x00'
These 2 bytes represent the number of sharps/flats and whether it is major or minor.
Next, we create a variable 'sf' which takes the integer value of the first byte of key_bytes:
'\xfc'
As an integer this byte would be 252.
And lastly, we do the same for mi. We take the second byte of key_bytes:
'\x00'
and assign it to mi.

After this we then reference these in our dictionary for a nicely formatted key!
key = KEY[sf][mi],TONALITY[mi]
return key
Here we are referencing our KEY dictionary and our TONALITY dictionary and then returning the result.
So, let's test this on a few cases once more just to be sure.
```
test()
Output:
========================================
########################################
========================================
pok.mid
 ------------------------------
time
[b'\x04\x02\x18\x08']
==============================
comment
No event found.
==============================
lyric
No event found.
==============================
key
[b'\x02\x00']
==============================
track
[b'Acoustic Grand Piano', b'Instrument2']
==============================
instrument
No event found.
==============================
copyright
No event found.
==============================
('D', 'Major')
========================================
########################################
========================================


========================================
########################################
========================================
pharell.mid
 ------------------------------
time
[b'\x04\x02\x18\x08']
==============================
comment
[b' Spea', b'@KMIDI KARAOKE FILE', b'@IGenerated with Karakan version 6.2', b'@LENGL', b'@TPharrell Williams - Happy(2013)', b'@TKAR by Estrada 31st December 2013', b'\\It', b' might', b' seem', b' cra', b'zy', b'/What', b' I\x92m', b' about', b' to', b' say', b'/Sun', b'shine', b" she's", b' here', b'/You', b' can', b' take', b' a', b' break', b"/I'm", b' a', b' hot', b' air', b' bal', b'loon', b'/That', b' could', b' go', b' to', b' space', b'/With', b' the', b' air', b'/Like', b' I', b" don't", b' care', b'/Ba', b'by', b' by', ....]
==============================
lyric
No event found.
==============================
key
[b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00', b'\xfc\x00']
==============================
track
[b'Soft karaoke', b'Words', b'Pharrell Williams - Happy 2013', b'From The Movie "Despicable Me 2"', b'Chart Positions: UK/NL/FRA No.1 US No.2 BEL No.4', b'Sequenced by Geoffrey Carter 31st December 2013', b'Electric Bass(Pick)', b'Electric Bass(Finger)', b'Electric Bass(Finger)', b'Hand Claps(Fast)', b'Hand Claps', b'Percussion', b'Lead 3(Calliope)']
==============================
instrument
No event found.
==============================
copyright
No event found.
==============================
('Ab', 'Major')
========================================
########################################
========================================

========================================
########################################
========================================
mz_f.mid
 ------------------------------
time
[b'\x06\x03\x0c\x08']
==============================
comment
[b'Amadeus Mozart', b'Herausgegeben am 1.6.2006\n', b'Update am 29.7.13\n', b'Dauer: 9:50 Minuten\n', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523']
==============================
lyric
No event found.
==============================
key
[b'\xff\x00']
==============================
track
[b'Klaviersonate Nr. 12 KV 332 No. 3', b'Piano right', b'Piano left', b'Pedal', b'Mozart: Sonate KV 332', b'Copyright \xa9 2006 by Bernd Kr\xfcger', b'http://www.piano-midi.de', b'Edition: 2013-07-28', b'Spur 8', b'Spur 9']
==============================
instrument
No event found.
==============================
copyright
[b'Copyright \xa9 2006 von Bernd Kr\xfcger. ']
==============================
('F', 'Major')
========================================
########################################
========================================

========================================
########################################
========================================
mz_a.mid
 ------------------------------
time
[b'\x06\x03\x0c\x08', b'\x06\x02\x18\x08', b'\x04\x02\x18\x08']
==============================
comment
[b'Amadeus Mozart', b'Fertiggestellt am  1.1.2006\n', b'Update am 6.7.3013\n', b'Dauer: 13:52 Minuten\n', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523', b'bdca426d104a26ac9dcb070447587523']
==============================
lyric
No event found.
==============================
key
[b'\x03\x00', b'\x00\x00', b'\x03\x00']
==============================
track
[b'Klaviersonate Nr. 11 KV 331', b'Piano right', b'Piano left', b'Pedal', b'Mozart: Sonate KV 331', b'Copyright \xa9 2005 by Bernd Kr\xfcger', b'http://www.piano-midi.de', b'Edition: 2013-07-06', b'Spur 8', b'Spur 9']
==============================
instrument
No event found.
==============================
copyright
[b'Copyright \xa9 2005 von Bernd Kr\xfcger. ']
==============================
('A', 'Major')
========================================
########################################
========================================
```
As you can see, we're starting to be able to extract quite a lot of information from all of our tracks. For your sake, I trimmed this output and only showed you 4 tracks out of about 30.  Thankfully, all is in working order and the keys get correctly represented!
You may have noticed that in some tracks, there are multiple keys. This can either be 1 of 2 things.

    There can be a modulation so the key signature changes half-way through, giving us a new key signature.


    Each key signature can be the key signature of each individual track. 


Obviously we don't need to know that each track is playing in the same key unless you're analysing some avant-garde string quartet but it's safe to say you're not. Our get_key() function only returns the first key it sees, this is because the majority of the key information you're given is redundant so can largely be ignored. We may come back to this later so see if we can get a list of all modulations that happen in a song, but for now, I'd call that a success!

We'll take a short break and get back to extracting data in part 4.