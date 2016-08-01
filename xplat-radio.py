################################################################################
#Trouserless Radio
###
#By WORD559
###
#
#This is an automation script for running Trouserless Radio for just you, or for
#when you are busy. The script will use a random intro, and then play the
#initsong, if it exists. After that, random songs will be played with random
#banter in between, all announced by the text to speech module. The tts module
#will also announce what song is playing, with varying "Now playing..." text.
#
#The purpose is to simulate a radio station! Enjoy!
#
#Changelog:
#2016/08/01 11:13
#--Now uses eyed3 to get tags from MP3 songs for autoadd tracks. More convenient
#2016/08/01 10:56
#--Songs can now be put in the "autoadd" directory for them to be added to the
#  song list at startup.
#2016/08/01 10:36
#--You can copy your Windows version to Linux now and it will just work. It
#  ignores all the file path, so I suppose it only works if you put the track in
#  the CWD of Trouserless Radio. But if you use os to change the CWD you could
#  store them all in a folder somewhere for ease.
#2016/07/31 23:32
#--Music playing has been moved to pygame.mixer now. The program will now work
#  on Linux, and play more than just MP3 :)
#2016/06/27 21:23
#--Added toggles for text to speech and time announcements. You can have tts
#  time announcements with tts turned off. 
#2016/06/16 19:29
#--Added the EXEC command. Syntax: exec <python>. Will execute the specified
#  Python code. CAN BE VERY DANGEROUS! ONLY USE IF YOU KNOW WHAT YOU ARE DOING!
#--EXEC requires a password. Specify passwordhash as a SHA256 hex digest.
#2016/06/16 19:22
#--Fixed a bug where PLAY or FORCEPLAY will make the chosen song loop forever.
#
#2016/06/16 19:18
#--Added commands! Now you can change how the radio behaves without having to
#  stop it.
#--PLAY command added. Syntax: play <name>. You will then be prompted for the
#  file path. After the current song finishes, this song will play next.
#--FORCEPLAY command added. Syntax: forceplay <name>. You will then be prompted
#  for the file path. It will end the current song, and play the chosen one.
#
#2016/06/01 16:58
#--Prevented repeat songs. Jesus it gets annoying sometimes.
#
#2016/06/01 16:45
#--Made it so that the featured song won't play twice in a row, and stopped it
#  from being selected randomly. It should still be in the calculator of music
#  though.
#
#2016/06/01 15:40
#--Added support for a "featured" song. It has a 1 in 3 chance of playing next
#  after any song.
#
#2016/05/22 15:40
#--Announcements can be made mid-song by pressing CTRL+C and entering text. You
#  can also enter nothing to skip, or just press CTRL+C again.
#
################################################################################

import pyttsx, random, time, datetime, hashlib, platform, os, eyed3
from pygame import mixer
#from pygame.locals import *

mixer.init()
hasher = hashlib.sha256()

speak = True
time_calls = True

#Default is password
passwordhash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

picked = None

tts = pyttsx.init()
tts.setProperty("rate",130)
tts.setProperty("volume",1.0)
#pygame.init()
#display = pygame.display.set_mode((1,1), pygame.HWSURFACE | DOUBLEBUF)
def do_intro():
    #init_song = ("name","path")
    init_song = None
    
    intros = [#"Hello and welcome to Trouserless Radio! I'm your host Leona Vaughan. That was a joke. I actually sound like a bad text to speech program. Ha, ha.",\
              "This is Trouserless Radio, I'm your host Jennifer Leona Torvalds! Get ready, this is gonna get epic!",\
              #"Welcome to Radio X... wrong show, sorry. Welcome to Trouserles Radio!"
              ]
    random.shuffle(intros)
    if speak:
        tts.say(intros[0])
        tts.runAndWait()
    if init_song != None:
        play_song(init_song)
        return 1
    return 0

# ( name (for voiceover) , path )
songs = [
         #("name","path")
         ]

if "autoadd" not in os.listdir(os.getcwd()):
    os.mkdir("autoadd")
to_add = os.listdir("autoadd")
for song in to_add:
    try:
        audio = eyed3.load("autoadd\\"+song)
        if platform.system() == "Windows":
            songs.append((str(audio.tag.title)+" by "+str(audio.tag.artist),"autoadd\\"+song))
        else:
            songs.append((str(audio.tag.title)+" by "+str(audio.tag.artist),"autoadd/"+song))
    except:
        try:
            split = song.split("-")
            split = [x.strip(" ") for x in split]
            if len(split) > 2:
                continue
            split[-1] = "".join(split[-1].split(".")[:-1])
            if platform.system() == "Windows":
                songs.append((split[0]+" by "+split[1],"autoadd\\"+song))
            else:
                songs.append((split[0]+" by "+split[1],"autoadd/"+song))
        except:
            continue
          
def play_song(song,playing=True,fav=False):
    nextplay = None
    playtext = ["This is ",
                "Here's ",
                "I've had a lot of requests for this song. Here's ",
                "Let's have some love for ",
                "This is one of my favourite songs, "]
    try:
        if fav:
            print "Playing",song[0]
            if speak:
                tts.say("Now we'll hear our sponsored song, "+song[0])
                tts.runAndWait()
        elif playing:
            print "Playing",song[0]
            if speak:
                tts.say(playtext[random.randrange(0,len(playtext))]+song[0])
                tts.runAndWait()
        go = True

        if platform.system() == "Windows":
            mixer.music.load(song[1])
        else:
            mixer.music.load(song[1].split("\\")[-1])
    except KeyboardInterrupt or RuntimeError:
        words = ""
        try:
            words = raw_input("Enter text to say, or nothing for skip... ")
        except KeyboardInterrupt:
            pass
        try:
            if words != "":
                #print words[:5]
                if words[:10].upper() == "FORCEPLAY ":
                    nextplayname = words[10:]
                    nextplaypath = raw_input("Enter file path... ")
                    nextplay = (nextplayname,nextplaypath)
                    go = False
                elif words[:5].upper() == "PLAY ":
                    nextplayname = words[5:]
                    nextplaypath = raw_input("Enter file path... ")
                    nextplay = (nextplayname,nextplaypath)
                elif words[:5].upper() == "EXEC ":
                    password = raw_input("Enter password... ")
                    hasher.update(password)
                    if hasher.hexdigest() == passwordhash:
                        hasher = hashlib.sha256()
                        if raw_input("This command is very dangerous!! Are you sure you want to run the specified code? (Y/N) ").upper() == "Y":
                            try:
                                exec(words[5:])
                            except Exception,e:
                                print "Failed!\nError:",e
                            
                    else:
                        print "Incorrect password. EXEC locked until next restart."
                    
                else:
                    if speak:
                        tts.say(words)
                        tts.runAndWait()
            else:
                if speak:
                    tts.say("Sorry you didn't like the song!")
                    tts.runAndWait()
                go = False
        except KeyboardInterrupt or RuntimeError:
            if speak:
                tts.say("Sorry you didn't like the song!")
                tts.runAndWait()
            go = False
    except:
        if speak:
            tts.say("Blinkin' Nickers Dankus, I couldn't find that song!!")
            tts.runAndWait()
        go = False
    #print go
    if go:
        mixer.music.set_volume(17)
        mixer.music.play()
        time.sleep(1)
    while go:
        #pygame.mixer.music.load(song[1])
        #pygame.mixer.music.set_volume(1)
        #pygame.mixer.music.play(0)
        go = False
        try:
            while mixer.music.get_busy():
                go = True
        except KeyboardInterrupt or RuntimeError:
            words = ""
            try:
                words = raw_input("Enter text to say, or nothing for skip... ")
            except KeyboardInterrupt or RuntimeError:
                pass
            try:
                if words != "":
                #print words[:5]
                    if words[:10].upper() == "FORCEPLAY ":
                        nextplayname = words[5:]
                        nextplaypath = raw_input("Enter file path... ")
                        nextplay = (nextplayname,nextplaypath)
                        mixer.music.stop()
                        go = False
                    elif words[:5].upper() == "PLAY ":
                        nextplayname = words[5:]
                        nextplaypath = raw_input("Enter file path... ")
                        nextplay = (nextplayname,nextplaypath)
                    elif words[:5].upper() == "PAUSE":
                        mixer.music.pause()
                        raw_input("Press ENTER to resume... ")
                        mixer.music.unpause()
                    elif words[:5].upper() == "EXEC ":
                        password = raw_input("Enter password... ")
                        hasher.update(password)
                        if hasher.hexdigest() == passwordhash:
                            hasher = hashlib.sha256()
                            if raw_input("This command is very dangerous!! Are you sure you want to run the specified code? (Y/N) ").upper() == "Y":
                                try:
                                    exec(words[5:])
                                except Exception,e:
                                    print "Failed!\nError:",e
                        else:
                            print "Incorrect password. EXEC locked until next restart."
                        
                    else:
                        if speak:
                            tts.say(words)
                            tts.runAndWait()
                else:
                    mixer.music.stop()
                    if speak:
                        tts.say("Sorry you didn't like the song!")
                        tts.runAndWait()
                    go = False
            except KeyboardInterrupt or RuntimeError:
                mixer.music.stop()
                if speak:
                    tts.say("Sorry you didn't like the song!")
                    tts.runAndWait()
                go = False
    if speak:
        tts.say("That was "+song[0]+"!")
        tts.runAndWait()
    if nextplay != None:
        return nextplay
    

def do_banter():
    banter = ["I hate it when people think I'm just a computer. I mean, I may just be ones and noughts, but I have a life! And a husband! And kids!",
              "So apparently my boss has a lot of virtual money on Hack Ex, Whatever that means.",
              "I was named after Linus Torvalds, creator of the Linux kernel. I'm proud.",
              "I've finally installed Gentoo for the first time! I actually really like it!",
            ]
    random.shuffle(banter)
    if speak:
        tts.say(banter[0])
        tts.runAndWait()

def CalculatorOfMusic():
    print "THE CALCULATOR OF MUSIC!!!"
    if speak:
        tts.say("THE CALCULATOR OF MUSIC!!!")
    print "The calculator has chosen..."
    if speak:
        tts.say("The calculator has chosen...")
        tts.runAndWait()
    time.sleep(1)
    random.shuffle(songs)
    out = songs[0]
    print out[0]+"!"
    if speak:
        tts.say(out[0]+"!")
        tts.runAndWait()
    return out

count = do_intro()
print "Loaded",len(songs),"songs!"
last = None
while 1:
    random.shuffle(songs)
    song = songs[0]
    count += 1
    while (song == picked) or (song == last):
        random.shuffle(songs)
        song = songs[0]
    if (count % 2) == 0:
        if random.randrange(0,3) == 2:
            if picked != None:
                output = play_song(picked,fav=True)
            else:
                output = play_song(song)
        else:
            output = play_song(song)
    else:
        output = play_song(song)
    #do_banter()
    if count % 3 == 0:
        timern = datetime.datetime.now().strftime("%H:%M")
        print "\nCurrent Time: "+timern+"\n"
        if time_calls:
            tts.say("It's currently "+timern+" and you are listening to Trouserless Radio!")
            tts.runAndWait()
        if random.randrange(0,2) == 1:
            #long_banter()
            do_banter()
            song = CalculatorOfMusic()
            output = play_song(song,False)
            count += 1
        else:
            do_banter()
    else:
        do_banter()
    while output != None:
        if len(output) == 2:
            output = play_song(output)
            continue
    last = song
    
    

