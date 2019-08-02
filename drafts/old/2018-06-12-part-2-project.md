Title: Part 2

----

Year: 

----

Text: 

As you can recall from the part 1, we gathered some useful information about our MIDI file, although not really enough to warrant any real use. We've extracted the number of tracks, how these tracks are played and their format types. Now we're going to get into the nitty gritty involving track names, lyrics and more.


First, let's recap by looking at the complete code we had from part 1
```
FORMAT_TYPE = {0:'One single multi-channel track',
                1:'One or more simultaneous individual tracks',
                2:'One or more sequentially independent tracks'}
```
```
class Midi():

    def __init__(self,filename):

        self.filename = filename
        self.midi = open(self.filename,'rb')
       
    def mthd_chunk(self):
        """Returns the MThd chunk and its headers"""
        self.midi.seek(0)
        midi_header = self.midi.read(14)#change this back to 18 later
        return midi_header
       
    def is_midi_file(self):
        """Returns True if the file is a midi file"""
        self.midi.seek(0)
        mthd_id = self.midi.read(4)
        mthd = b'MThd'
       
        if mthd_id == mthd:
            return True
        else: return 'Not valid midi file'
           
    def format_type(self):
        """Returns the format type of the midi file"""
        chunk = self.mthd_chunk()
        return FORMAT_TYPE[chunk[9]]

    def mtrk_count(self):
        """Returns the number of mtrk chunks in the midi file"""
        a = self.mthd_chunk()
        mtrk_chunks = a[11]
        return mtrk_chunks
```
Next up, we're going to try and get the track names of our MIDI files!
Now remember, it's up to the USER to input this data, they don't have to input all of this 'nice to have' data. They don't have to tell us anything, this code only really shines through on well created/documented MIDI files.

To extract the track names I'm going to do something I originally thought was a terrible idea...Regular *gasp* Expressions!

Usually regular expressions are frowned upon, quite often just from the sheer fear of them. In reality though, in small doses they are extremely useful and are often faster and more readable than various string methods duct taped to each other.
Getting Track Names

There are several ways you could get the track name, what you're essentially looking out for is a byte that looks like the following
```
\xff\x03
```
There are many variants of this byte that denote different things. The most common you will see is

'FF 01'. This basically means it is a comment in the MIDI file and although it can be used for ANY text, it's really best to use it only for comments because there are other byte formats for Orchestration, instrumentation etc...


Below is a small non-exhaustive list of the most useful (to me) versions of this byte string that I will be looking at:
```
FF 01 - A comment in a MIDI file

FF 02 - The copyright notice of the MIDI file

FF 03 - The track name

FF 04 - The instrument the track plays

FF 05 - Lyric
```
To start with we'll go for the easiest tasks of getting the first 3 out of this list, the lyrics will be particularly difficult to extract because they are broken up syllable by syllable (A parsing nightmare). Let's take a look at 'Pharells - Happy' MIDI file to show you what I mean
```
\xff\x01\x03\\It\x83`\xff\x01\x06 might\x83`\xff\x01\x05 seem\x87@\xff\x01\x04 cra\x87@\xff\x01\x02zy\x83`\xff\x01\x05/What\x83`\xff\x01\x04 I\x92m\x83`\xff\x01\x06 about\x83`\xff\x01\x03 to\x83`\xff\x01\x04 say\xcb\x00\xff\x01\x04/Sun\x83`\xff\x01\x05shine\x87@\xff\x01\x06 she's\x87@\xff\x01\x05 here\x8b \xff\x01\x04/You\x83`\xff\x01\x04
```
After each FF 01 event, there is one syllable of lyrics. Something like this can very quickly get tricky to parse but we'll plough on and tackle that problem at a later date.

For now, let's continue retrieving our track information.
First you need to have a look through your MIDI data for the 'track' byte which is FF 03.
Once you have found the track name byte (FF 03) there is a byte after that, that denotes how long the track name is. For example:
```
\xff\x03\x0cStartup-demo
```
Here we have our track name byte (\xff\x03) and after those two bytes, we have a byte that says how long the string of text 'Startup-demo' is. In this case '\x0c' is the number 12 which is exactly how long the string 'Startup-demo' is!

This information makes it sooooooo much easier for us to parse through this MIDI and what's even better is that this information is present in ALL text events, not just track names. It's present in the copyright notice, comments, lyrics, EVERYTHING!

Knowing this, we can start getting to work with parsing our data.

I've built a small function that retrieves the track name for us using regular expressions and it looks a little like this:
```
    def get_track_name(self):
        """Returns the name of the MIDI track, this can either be the name of
        the song, or the name of an individual track."""
        
        track_data = b'\xff\x03'
        midi_data = self.midi.read()
        track_list = []
        
        for match in re.finditer(track_data,midi_data):
            matchmidi = midi_data[match.end()]+1
            track_list.append(midi_data[match.end()+1: match.end()+matchmidi])

        self.midi.seek(0)
        return track_list if track_list else None
```
Let's go through this code line by line and see what's going on under the hood.
```
   track_data = b'\xff\x03'
```
First, we set track_data to b'\xff\x03'. This improves readability and just makes everything easier to digest
After that we create an empty list, this is where our tracks will be added (we could have used a list comprehension for this whole function but in the interest of sanity I've decided not to do that.)

Now the detail begins.

We're using re's 'finditer' method which finds all instances of a pattern in a string. In our case, we're finding all instances of b'\xff\x03' in our midi file.
```
   for match in re.finditer(track_data,midi_data):
```
a match in 'finditer' has several methods that return useful values
- match.start() returns the index of the beginning of the occurence of the pattern. So in our case match.start() would return the index of the beginning of b'\xff\x03'

- match.end() returns the index at the end of the pattern, this one is more useful to us for this function. With the information of when our track_data ends and the length of the text_event we can begin getting the information we want.
```
   matchmidi = midi_data[match.end()]+1
```
we're setting the variable 'matchmidi' to the index of match.end()+1. The reason for +1 is that this is the location of the length of the text event. So essentially, 'matchmidi' is being assigned the length of the text event.
```
   track_list.append(midi_data[match.end()+1: match.end()+matchmidi])
```
We are then appending our matched track to the list, it's quite simple to explain. We are adding the index of the midi file FROM the end of the match, up to the length of the text event. So for example if our match was at 4 and the length of our text event was 15, we would retrieve the index 4 to 15.

After all this is done we then 'seek' back to 0 so that our file can read from the start rather than just some arbitrary position and then return the tracklist if it's not empty. Hey presto!

Now, there's something I've noticed about this function, there's going to be a lot of code redundancy in it. For example, If I want to find a comment I'm going to have to copy and paste this entire function and then replace b'\xff\x03' with b'\xff\x01'. A large waste of time. In this case it may be more useful to create a more general function which returns what you ask it. For this, I'll be coding up something similar to our format_type function. First we need to create a dictionary of all the text events that can happen.
```
TEXT_EVENT = {'comment'   :b'\xff\x01',
              'copyright' :b'\xff\x02',
              'track'     :b'\xff\x03',
              'instrument':b'\xff\x04',
              'lyric'     :b'\xff\x05'}
```
And then we just have to make our function reference the TEXT_EVENT that we ask for.  Here is our newly revised and uber flexible function:
```
    def get_text_event(self,event):
        """Returns a text event from the TEXT_EVENT dictionary"""

        data = TEXT_EVENT[event]
        midi_data = self.midi.read()
        _list = []

        for match in re.finditer(data,midi_data):
            matchmidi = midi_data[match.end()]+1
            _list.append(midi_data[match.end()+1: match.end()+matchmidi])

        self.midi.seek(0)
        return _list if _list else None
```
Okay, so we've written a lot of code but we haven't really tested any of it out on some data so let's do that right now to give us some gratification.
```
>>> a = Midi('midi.mid')
>>> a.get_text_event('track')
[b'Startup-demo', b'Startup - demo']
>>> a.get_text_event('comment')
'No event found.'
```
It works! It found 2 track events but no comment events. Let's use a few more test cases just to be sure. My test cases of MIDI are getting quite large so I won't show the complete output because you'll be flooded with MIDI information.
```
for midi in gm:
    a = Midi(midi)
    print('='*40)
    print(midi)
    print('-'*40)
    print('TRACKLIST')
    a.get_text_event('track')
    print('-'*40)
    print('COMMENTS')
    a.get_text_event('comment')
    print('-'*40)
    print('COPYRIGHT')
    a.get_text_event('copyright')
    print('='*40)
```
And here's the output:
```
========================================
beatles.mid
 ----------------------------------------
TRACKLIST
[b'Guitar', b'Applause', b'Guitar', b'Piano', b'Bass', b'Melody (Harmonica)', b'Strings', b'Brass', b'Woodwinds', b'Percussion', b'More percussion', b'Low Brass', b'Melody (Muted Trumpet)', b'Melody (Trumpet)', b'A Day in the Life', b'  by the Beatles', b'Sequenced by:', b'  Wesley Ellinger', b'  Houston,TX',b'  08/02/95']
 ----------------------------------------
COMMENTS
'No event found.'
 ----------------------------------------
COPYRIGHT
'No event found.'
========================================



========================================
midi.mid
 ----------------------------------------
TRACKLIST
[b'Startup-demo', b'Startup - demo']
 ----------------------------------------
COMMENTS
'No event found.'
 ----------------------------------------
COPYRIGHT
'No event found.'
========================================



========================================
miley.mid
 ----------------------------------------
TRACKLIST
[b'Wrecking Ball - Miley Cyrus Oct 2013', b'From The Album "Bangerz"', b'Bright Acoustic', b'String Ensemble 2', b'Electric Piano 1', b'String Ensemble 1', b'Overdriven Guitar', b'Flute', b'Percussion', b'FX 1 (Rain)', b'Lead 3 (Calliope)']
 ----------------------------------------
COMMENTS
[b' Spea', b'win\n']
 ----------------------------------------
COPYRIGHT
[b'by erwin']
========================================
```
Great! Now that we can extract this sort of data things start getting useful. We'll tunnel more in-depth in our next part, but for now I think you and I could do with a break!

----

Tags: 