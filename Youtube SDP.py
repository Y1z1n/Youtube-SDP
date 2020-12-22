from os import remove, environ, path, system
from time import sleep
from threading import Thread
try:
    import pytube, json
    from moviepy.editor import VideoFileClip
    from youtubesearchpython import SearchVideos
except Exception as msg:
    print("[*] Installing requirments - Try re-start the script after the procces finishing")
    system("pip install git+https://github.com/nficano/pytube")
    system("pip install moviepy")
    system("pip install youtube-search-python")
    system("cls || clear")
# import Mp3_player
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
genres = []
minlimit = int(input("Enter the maximum minutes you want the downloaded videos to have [NUMBERS ONLY] ->"))
while True:
    Output = input("Enter a word for your genre-music ->> ")
    if Output == "exit"or Output == "quit":
        break
    else:
        genres.append(Output)
def Search(genres):
    searchresult = []
    for genre in genres:
        print("Searching for all your videos and filtring it | this will take a while")
        search = SearchVideos(genre, offset = 1, mode = "json", max_results = 20)
        searchresult.append(str(search.result()))
    return searchresult
def GetLinks():
    global genres
    search = Search(genres)
    songs = []
    for searches in search:
        for x in json.loads(searches)['search_result']:
            songs.append(x['link'])
    return songs
threads = []
songsfilter = []
def GetLength(song):
    global minlimit
    try:
        videolength = str(pytube.YouTube(song).length)
        print(song + " | " + "LIVE" if videolength == "0" else song + " | "+  videolength)
        if int(videolength) / 60 <= minlimit and int(videolength) != 0:
            songsfilter.append(song)
        sleep(2)
    except:
        sleep(5)
songs = GetLinks()
print(len(songs))
for index,_ in enumerate(range(int(input(f"Threads (Recommended: {len(songs) / 2 + 5}) ->> ")))):
    t = Thread(target=GetLength, args=(songs[index],), daemon=True)
    threads.append(t)
    t.start()
for i in threads:
    i.join()
print(f"Number of vids After filtring the minutes : {len(songsfilter)}")
def filtercopies():
    global songsfilter
    songsfilter2 = []
    for song in songsfilter:
        try:
            songsfilter2.index(song)
        except ValueError:
            songsfilter2.append(song)
    # print(songsfilter2, len(songsfilter2))
    return songsfilter2
songsfilter2 = filtercopies()
def convert_to_mp3(filename):
    clip = VideoFileClip(filename, verbose=False)
    clip.audio.write_audiofile(filename[:-4] + ".mp3",progress_bar=False,)
    del clip.reader
    del clip
def Download(url):
    yt = pytube.YouTube(url)
    yt.streams.filter().first().download()
    convert_to_mp3(yt.streams.get_by_itag(18).default_filename)
    filename = yt.streams.get_by_itag(18).default_filename
    return filename
def DelMp4(filename):
    remove(filename)
print(f"Number of vids After filtring the copies : {len(songsfilter2)}")
# for downloadingsong in songsfilter2:
#     filename = Download(downloadingsong)
#     DelMp4(filename)

####UNDER TESTING#####
for downloadingsong in songsfilter2:
    t = Thread(target=Download, args=(downloadingsong,), daemon=True)
    threads.append(t)
    t.start()
for i in threads:
    i.join()
filenames = []
for downloadingsong in songsfilter2:
    name = pytube.YouTube(downloadingsong).streams.get_by_itag(18).default_filename
    DelMp4(name)
    filenames.append(name[:-4] + ".mp3")
fuck_you_JSON = {
    "Creator":{
        "id":"1",
        "Instagram": "Y1z1n.programs",
        "name":"Yazan"
    },
    "Data":{
        "List": filenames
    }
}
with open("settings.json", "r") as f:
        olddata = json.loads(f.read())
        print(olddata)
        with open("settings.json", "w") as ff:
            json.dump(fuck_you_JSON, ff)
if input("Do you want to start ? [y/n]").lower() == "y":
    print("Then run mp3_player.py :>")