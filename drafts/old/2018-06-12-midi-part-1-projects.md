Title: Building A Midi Parser Part 1

----

Text: 

Over the past few months I've gotten tired of doing 'toy' programming projects so have started working on more useful and substantial things. The first one was a scraper app for my Kindle PaperWhite which essentially turns multiple HTML documents into one.

This next one will be a MIDI parser, I'm going to document the process since there is very little information on this online, so let's begin.

## Why

I saw a post over at opengameart recently discussing the lack of metadata in all their files which makes categorisation hard. Although this probably won't benefit those guys, I'd like to think that the metadata that we'll be able to extract from these MIDI files is important to someone.

## Metadata?

So I've probably lost about 95% of my musical audience already by talking about 'parsing', 'scraping' and 'metadata' so let's go through some terms...

Parsing - This is essentially grabbing the data you want from a certain source. For example you could 'parse' an HTML document for e-mails which would take all the e-mails out of a HTML document for you. (Don't parse HTML yourself...)

Metadata - All files contain metadata, it's like a form of passport or ID for a file. It says what kind of file it is, when it was created, copyright notices of that file and more. The majority of this information isn't available just by clicking on the file (not because it's hidden but because it's not usually useful to the general population.If it was available at the click of a button I wouldn't have to write my own! ).

So when I say I'm parsing a MIDI file for metadata I'm just saying "I'm looking in this file for some useful information".

To me this useful information is the following;

- Track Name
- Tempo
- Lyrics
- Copyright Notice
- Number of Tracks

Parsing the file
There is a ton of info to be gotten from a MIDI file. Unfortunately not all MIDI files have all the information you'd like. I've seen files that are filled to the brim with info about the lyrics, who sang it, what headphones were used etc...
And then on the other hand I've seen MIDI which only specifies the number of MIDI tracks (this is a mandatory specification so they didn't really include anything).

So how do we get all this information?

It's (kind of) simple but very fiddly.

## Parsing MIDI Metadata

A file is just bytes underneath. And for a MIDI file the first 4 bytes indicate whether a MIDI file is indeed a MIDI file.

Let's examine the MThd header/chunk to see what I'm talking about. (This is the first chunk that appears in a MIDI file)

First, we want to get the first X amount of bytes, in MIDI's case it is the first 14 bytes that show the MThd chunk. So we'll do that!
```
class Midi():

    def __init__(self,filename):

        self.filename = filename
        self.midi = open(self.filename,'rb')
        
    def mthd_chunk(self):
        """Returns the Mthd chunk and its headers"""
        self.midi.seek(0)
        midi_header = self.midi.read(14)
        return midi_header
```

This is the code we'll use for any midi file we want to use. I'm using Python 3.3. and have chosen an OO approach because OO is the way and you know it.


Let's try these methods out on a file to see if it worked.

```
>>> midi_file = Midi('ff91.mid')  #Creating the MIDI object
>>> midi_file.mthd_chunk()        #Getting the MThd header and chunk
b'MThd\x00\x00\x00\x06\x00\x01\x00\x11\x00\xc0'
```

So this is our MThd chunk, looks pretty nifty ey?
Well actually it doesn't.

If I explain what's here though, it begins to make a bit more sense.
The first 4 bytes 'MThd' tell us that this IS a MIDI file no matter what. So already this is kind of useful. I guess we should make some code that test whether a file is a MIDI file so that we know we're working on the right stuff.

So, let's get going:
```
    def is_midi_file(self):
        """Returns True if the file is a midi file"""
        self.midi.seek(0)
        mthd_id = self.midi.read(4)
        mthd = b'MThd'
        
        if mthd_id == mthd:
            return True
        else: return 'Not valid midi file'
```
It's not pretty, but it works. Let's test what we've learnt so far on a few more cases, we should test on as many sources as we can to make sure our code is up to the test of horribly malformed files and metadata.


What I'll be doing is testing on 6 or so MIDI files, getting all of their MThd chunks and also testing to see whether they are indeed MIDI files.
```
for midi_file in midi_file_list:
    print(midi_file)
    mid = Midi(midi_file)
    mid.mthd_chunk()
    mid.is_midi_file()
    print('='*50)
```
And here is our output:
```
midi.mid
b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x01\xe0'
True
==============================================
beatles.mid
b'MThd\x00\x00\x00\x06\x00\x01\x00\x17\x00\xc0'
True
==============================================
pharell.mid
b'MThd\x00\x00\x00\x06\x00\x01\x00\x0e\x03\xc0'
True
==============================================
ff91.mid
b'MThd\x00\x00\x00\x06\x00\x01\x00\x11\x00\xc0'
True
==============================================
ff92.mid
b'MThd\x00\x00\x00\x06\x00\x01\x00%\x01\xe0'
True
==============================================
ff93.mid
b'MThd\x00\x00\x00\x06\x00\x00\x00\x01\x01\xe0'
True
==============================================
doggeh.jpg
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01'
'Not valid midi file'
==============================================
```
It works!

The first line is the files name.
The second line is the first 14 bytes which in MIDI's case is the MThd chunk
The last line tells us if this is a valid MIDI file.

You can probably see that the last file is actually a .jpeg file, I used this just to make sure our code can detect a valid MIDI file or not. There's no point in testing whether something is a MIDI file if all you're going to feed it is MIDI files!

Okay great, I've explained the first 4 bytes ('MThd') and what they do, so what's next?

Let's go through the next few bytes:
```
b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x01\xe0'
```
After MThd, we get this weird string of '\x00\x00\x00\x06\'. This is in every single MIDI file, it can be ignored, it just tells us the length of the MThd header which is ALWAYS 6.

The next two bytes are important to us, in this case, the next two bytes are '\x00\x01'. This is the 'format type' of a MIDI file. The format type tells us how the tracks are playing, are they all on a single track, or are they all separate instruments on their own tracks?

    '\x00\x00' - This tells us that the MIDI track is one single track, nothing more, nothing less.
    '\x00\x01' - This tells us that the MIDI track is one or more independent separate tracks.
    '\x00\x02' - This tells us that there are one or more sequentially independent tracks, this never really caught on so I'd be surprised if you see this in any MIDI files.


Let's code up some stuff to show us the format of a MIDI file easily.


First we want to create a dictionary/lookup table of values that specify the format types of a MIDI file.
```
FORMAT_TYPE =  {0:'One single multi-channel track',
                1:'One or more simultaneous individual tracks',
                2:'One or more sequentially independent tracks'}
```
Next we want to use this in our code to extract the format type from the MIDI file.
```
    def format_type(self):
        """Returns the format type of the midi file"""
        chunk = self.mthd_chunk()
        return FORMAT_TYPE[chunk[9]]
```
That's some pretty concise code so let me explain. We are setting the variable 'chunk' to the first 14 bytes of our MIDI file, then we are fetching the 9th byte (counting from 0) from 'chunk' which is our format type and then passing this to our dictionary of format types so it can return something useful.


Let's test it out!
```
midi.mid
'One or more simultaneous individual tracks'
========================================
beatles.mid
'One or more simultaneous individual tracks'
========================================
pharell.mid
'One or more simultaneous individual tracks'
========================================
ff91.mid
'One or more simultaneous individual tracks'
========================================
ff92.mid
'One or more simultaneous individual tracks'
========================================
ff93.mid
'One single multi-channel track'
========================================
```
So far so good, it'd be neat if we could find out more than just whether there is one or more tracks. It'd be nice if we could get an exact number of tracks, so let's do that. Let's look at our MThd chunk again.
b'MThd\x00\x00\x00\x06\x00\x01\x00\x02\x01\xe0'

So far we've covered

    MThd - Identifies whether a file is a MIDI track or not.
    \x00\x00\x00\x06 - The length of the MThd chunk.
    \x00\x01 - The format type


Next up is '\x00\x02'. These two bytes are straight after our format type bytes (\x00\x01). These two bytes tell us the number of tracks in a MIDI file. Hooray! USEFUL INFORMATION! SWEET JESUS WE'VE HIT THE JACKPOT HERE JOHNNY.


Extracting this is just the same as extracting our format, except instead of extracting the 9th byte, we get the 11th byte like so:
```
    def mtrk_count(self):
        """Returns the number of mtrk chunks in the midi file"""
        a = self.mthd_chunk()
        mtrk_chunks = a[11]
        return mtrk_chunks
```
Let's test this with our format type and see if it all makes sense.
```
for midi_file in midi_file_list:
    print(midi_file)
    mid = Midi(midi_file)
    print('TRACK COUNT:',mid.mtrk_count())
    mid.format_type()
    print('='*40)
```
Output:
```
midi.mid
TRACK COUNT: 2
'One or more simultaneous individual tracks'
========================================
beatles.mid
TRACK COUNT: 23
'One or more simultaneous individual tracks'
========================================
pharell.mid
TRACK COUNT: 14
'One or more simultaneous individual tracks'
========================================
ff91.mid
TRACK COUNT: 17
'One or more simultaneous individual tracks'
========================================
ff92.mid
TRACK COUNT: 37
'One or more simultaneous individual tracks'
========================================
ff93.mid
TRACK COUNT: 1
'One single multi-channel track'
========================================
```
It works!
The MIDI file with a track count greater than 1 coincides with the correct format type.

I think that's all for now, we've covered quite a lot, but at the same time only scratched the surfac, stay tuned for part 2!

## Further Reading

<http://www.midi.org/store/docsales.php>
<http://midi.mathewvp.com/aboutMidi.htm>
<http://www.fileformat.info/format/midi/corion.htm>
<http://www.somascape.org/midi/tech/mfile.html>
