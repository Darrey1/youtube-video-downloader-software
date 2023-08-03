import os
from pytube import YouTube

# select folder to download
selectPath = input("Enter the path of the folder to save downloads: ")

selectPath = repr(selectPath)   # will make raw string
l=list(selectPath)
while "'" in l:
    l.remove("'")
selectPath = ''.join(l)

# if selected folder is not found
while os.path.isdir(selectPath)==False:
    selectPath = input("No such directory! Enter again: ") 
    selectPath = repr(selectPath)   # will make raw string
    l=list(selectPath)
    while "'" in l:
        l.remove("'")
    selectPath = ''.join(l)

no_of_downloads=0

while True:
    
    link = input("\nEnter the URL of the video: ")
    
    # if video is found
    try:
        mainVideo = YouTube(link)
        print("Fetching data...")
        print("\nTitle: ",mainVideo.title)
        download = input("Enter 'D' to download and 'N' to skip: ")
        
        # if wrong choice download or quit
        while download.upper() !='D' and download.upper() !='N':
            download = input("Wrong choice! enter either 'D' or 'N': ")
         
        # if download
        if download.upper() =='D':
            choice = input("Enter 1 to download audio only and 2 to download video: ")
            
            # if wrong choice audio or video
            while choice!='1' and choice!='2':
                choice = input("Wrong choice! enter either 1 or 2: ")
                    
            # if audio download
            if choice=='1':
                print("Loading all audio streams...")
                streams = mainVideo.streams.filter(only_audio=True)
                list_of_streams = list(streams)
                print("\nAll audio streams in the video:")
                for i in range(len(list_of_streams)):
                    print("index:",i+1,"  ",list_of_streams[i])
                choice_stream = input("Enter the stream index according to which stream you want to download: ")
                
                # if choice of stream is wrong
                while choice_stream.isnumeric()==False or int(choice_stream)<1 or int(choice_stream)>len(list_of_streams):
                    choice_stream = input("stream index is out of range! choose the correct stream: ")
                
                # if correct choice then download
                name_of_file = input("Enter the filename or press Enter to set filename default: ")
                if name_of_file=='':
                    l=list(mainVideo.title)
                    while '|' in l:
                        l.remove('|')
                    s = ''.join(l)
                    name_of_file = s+'.mp3'
                    markFilename='*'
                else:
                    markFilename = name_of_file
                    name_of_file = name_of_file+'.mp3'
                checkFile = selectPath +"\\"+ name_of_file                    
                if os.path.isfile(checkFile)==True:
                    print("File already exists")
                else:
                    print("Downloading...")
                    os.chdir(selectPath)
                    downloaded_file = streams[int(choice_stream)-1].download()
                    if markFilename=='*':
                        base, ext = os.path.splitext(downloaded_file)
                        new_file = base+'.mp3'
                        os.rename(downloaded_file, new_file)
                    else:
                        new_file = markFilename+'.mp3'
                        os.rename(downloaded_file, new_file)
                    no_of_downloads+=1
                    print("\n\nSuccessfully downloaded!")
                    print("File is stored at:",os.getcwd())
                    print(no_of_downloads,"files downloaded")
                  
            # if video download
            if choice=='2':
                print("Loading all video streams...")
                streams = mainVideo.streams.all()
                streams = mainVideo.streams.filter(progressive=True)
                #streams = mainVideo.streams.get_highest_resolution()
                list_of_streams = list(streams)
                print("\nAll video streams in the video:")
                for i in range(len(list_of_streams)):
                    print("index:",i+1,"  ",list_of_streams[i])
                #print(streams)
                choice_stream = input("Enter the stream index according to which stream you want to download: ")
                
                # if choice of stream is wrong
                while choice_stream.isnumeric()==False or int(choice_stream)<1 or int(choice_stream)>len(list_of_streams):
                    choice_stream = input("stream index is out of range! choose the correct stream: ")
                
                # if correct choice then download
                name_of_file = input("Enter the filename or press Enter to set filename default: ")
                if name_of_file=='':
                    l=list(mainVideo.title)
                    while '|' in l:
                        l.remove('|')
                    s = ''.join(l)
                    name_of_file = s+'.mp4'
                    markFilename='*'
                else:
                    markFilename = name_of_file
                    name_of_file = name_of_file+'.mp4'
                checkFile = selectPath +"\\"+ name_of_file                    
                if os.path.isfile(checkFile)==True:
                    print("File already exists")
                else:
                    print("Downloading...")
                    os.chdir(selectPath)
                    downloaded_file = streams[int(choice_stream)-1].download()
                    #downloaded_file = streams.download()
                    if markFilename!='*':
                        new_file = name_of_file
                        os.rename(downloaded_file, new_file)
                    no_of_downloads+=1
                    print("\nSuccessfully downloaded!")
                    print("File is stored at:",os.getcwd())    
                    print(no_of_downloads,"files downloaded")
        
    # if video is not found
    except Exception as e:
        print(e)
        print("cannot find video")
            
    q = input("press Enter to continue or enter 'Q' to quit: ")
    if q=='Q':
        break