# Trouserless Radio
Trouserless Radio, a Python-based, personal automated radio station.

##Setup
Trouserless Radio will only run on Python 2.7
###Windows
On Windows you will need to install pyttsx. This can be done using the following command:
```
pip install pyttsx
```
You will also need to install eyeD3:
```
pip install eyeD3
```
You will need to have `pip` installed first, see [this StackOverflow question](http://stackoverflow.com/questions/1449494/how-do-i-install-python-packages-on-windows) for details.

You will then need to install PyGame. This can be downloaded from [here](http://www.pygame.org/download.shtml)

The program can then be run either from the command line or Python IDLE.

###Linux
Linux users can use the handy shell scripts provided to use Trouserless Radio.
```
sudo bash setup.sh
./run.sh
```

Alternatively, if you want to do everything manually, you can do the following:

You will first need to install pygame:
```
apt-get install python-pygame
```

espeak is also required for pyttsx:
```
apt-get install espeak
```

Install pyttsx:
```
pip install pyttsx
```

And finally install eyed3:
```
pip install eyeD3
```

The program can then be run either from the command line or Python IDLE. 

###Configuring
####Songs
Songs can be added by two different methods:
* Adding the song to the `autoadd` folder created on the first run.
* Writing the song into the code.

If adding to the `autoadd` folder, the song must either:
- Have the naming structure "<song name> - <artist>.<ext>"
- Be an MP3 with Title and Artist set in the metadata.

The MP3 metadata will take precedence over the naming structure.

If writing the code in, find the line of code that begins `songs = [`. Make a new line and add the song as a tuple/list like so:
```
("<text to be spoken>","path/to/song")
```

This method allows you to use music stored anywhere on the system, instead of relocating all of you music to the `autoadd` folder.

####Initial Song
You can set the first song to be played by setting the variable `init_song` in the function `do_intro`. The contents of the variable is the same as for coded-in songs:
```
("<text to be spoken>","path/to/song")
```

####Preferred Song
If you would like a certain song to play more often than the others, you can set the variable `picked`. The contents of the variable is the same as for coded-in songs:
```
("<text to be spoken>","path/to/song")
```
After every other song, there is a 1 in 3 chance of the picked song being chosen.

####Intros and Intermittent "Banter"
To customise the intros, find the variable `intros` in `do_intro`. Simply add another string to the list to specify a new intro.

To customise the "banter" between songs, find the variable `banter` in `do_banter`. Simply add another string to the list to add more intermittent speech options.

####EXEC Password
To change the password to use the EXEC command, hash your password with the SHA256 algorithm and set the variable `passwordhash` to the hexdigest of your password.

##Commands
There are some commands available for use in the program. In order to use them, press `CTRL+C` (`KeyboardInterrupt`). From here, you can execute commands. Any text entered here that isn't a command will be spoken by TTS.

####PLAY
After entering this command, you will be prompted for a file path. The path you enter will be the song that is played next.

####FORCEPLAY
You will be prompted for a file path like in PLAY, except FORCEPLAY will stop the current song and then play the specified song.

####EXEC
Allows you to run Python code without stopping the station. **This can be dangerous.** The password must be entered in order to prevent any malicious users from using this command to delete data from your computer. The password must be entered correctly first time, else hasher is not reset and the EXEC command cannot be used until the next time the program is restarted. *I take no responsibility for any damage you do using this command.*

####PAUSE
Does what it says on the tin, really. Pauses the song until you press enter to resume.