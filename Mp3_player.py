from os import listdir, path, environ, mkdir, getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
mixer.init()
import json, argparse
def out():
    exit()
def getplaylist():
    with open("settings.json", "r") as f:
        data = json.loads(f.read())['Data']['List']
        return data
xz = getplaylist()
count = 0
def Player():
    while True:
        print("Type p to pause, s to stop, n to next song")
        cmd = input(" ")
        if cmd == "p":
            mixer.music.pause()
            print("o to unpause, s to stop")
            cmd2 = input(" ")
            if cmd2 == "o":
                mixer.music.unpause()
            else:
                mixer.music.stop()
                return False
        elif cmd == "s":
            mixer.music.stop()
            return False
        else:
            return True
def Her():
    if xz:
        for song in xz:
            try:
                mixer.music.load(song)
                mixer.music.set_volume(0.7)
                print(f"Playing now {song}")    
                mixer.music.play()
                if Player():
                    continue
                else:
                    break
            except:
                pass
        print("Reached the end hope you enjoyed ;>")

    else:
        print("There is problem try downloading pygame libary (cmd command : pip3 install pygame)")
        input("Press anything to stop the program")
        exit()
Her()