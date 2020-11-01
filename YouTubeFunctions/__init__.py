def get_ChannelId(url_channel):
    '''
    Function to get the channel id from URL of youtube Channel
    '''
    
    #Libraries
    import re
    
    return re.findall(r'([^/]+$)',url_channel)




def get_channel(url_channel, youtube_api_key):
    '''
    Function to get the data of the channel that was set in the previous function
    '''
    
    #Libraries
    import os
    import pandas as pd
    from googleapiclient.discovery import build
    
    #Get the channel id from URL of youtube Channel (Previous Function)
    get_channel_id = get_ChannelId(url_channel)
    
    #Build the socket with Youtube data API through the library googleapiclient
    youtube = build('youtube','v3', developerKey=youtube_api_key)
    
    #Request to get data of the channel
    request = youtube.channels().list(
                part='statistics, brandingSettings',
                id=get_channel_id
                )
    response = request.execute()
    
    #Empty Dictionary for Channel
    channel_dict = {
                       "Channel Id":[],
                       "Channel Title":[],
                       "View Count":[],
                       "Subscriber Count":[],
                       "Video Count":[],
                       "Channel Country":[],
                       "Channel Description":[]
                  }
    
    #Append the data from Chanel in the "channel_dict"
    for item in response['items']:
        channel_dict['Channel Id'].append(item['id'])
        channel_dict['Channel Title'].append(item['brandingSettings']['channel']['title'])
        channel_dict['View Count'].append(item['statistics']['viewCount'])
        channel_dict['Subscriber Count'].append(item['statistics']['subscriberCount'])
        channel_dict['Video Count'].append(item['statistics']['videoCount'])
        channel_dict['Channel Country'].append(item['brandingSettings']['channel'].get('country', None))
        channel_dict['Channel Description'].append(item['brandingSettings']['channel']['description'])
    
    #Create a dataFrame from The dicttionary "channel_dict"
    df_channel = pd.DataFrame(channel_dict)
    
    #Get the Title of the channel for organize in folders
    channel_title = list(df_channel['Channel Title'])[0]
    
    #Create de folder for chaneel in the Data diretory
    try:
        os.mkdir(f'../data/{channel_title}')
    except: pass        
    
    #Convert to CSV
    df_channel.to_csv(f'../data/{channel_title}/channel.csv',index=False)
    
    return df_channel




def get_playlist(url_channel, youtube_api_key):
    '''
    Function to get the data all playlists in the channel that was return in the previous function
    '''
    
    #Libraries
    from datetime import timedelta, datetime
    import pandas as pd
    from googleapiclient.discovery import build
    
    #Get the channel informations from URL of youtube Channel (Previous Function)
    channel_info = get_channel(url_channel, youtube_api_key)
    
    #Get the Title of the channel for organize in folders
    channel_title = list(channel_info['Channel Title'])[0]
    
    #Get the channel id from URL of youtube Channel (Previous Function)
    channel = list(channel_info['Channel Id'])[0]
    
    #Build the socket with Youtube data API through the library googleapiclient
    youtube = build('youtube','v3', developerKey=youtube_api_key)
    
    #formal for use in date formula
    f = "%Y-%m-%dT%H:%M:%S"
    
    #Empty Dictionary of a Playlist
    playlist_dict = {
                        "Playlist Id":[],
                        "Playlist Title":[],
                        "Channel Id":[],
                        "Published At":[],
                        "Playlist Description":[]
                      }
    
    #Loop While Break
    nextPageToken = None
    while True:
        #Request to get data of the playlist
        pl_request = youtube.playlists().list(
                part='contentDetails, snippet',
                channelId=channel,
                maxResults=50,
                pageToken = nextPageToken
                )
        pl_response = pl_request.execute() 
        
        #Append the data from Playlist in the "playlist_dict"
        for item in pl_response['items']:
            playlist_dict['Playlist Id'].append(item['id'])
            playlist_dict['Playlist Title'].append(item['snippet']['title'])
            playlist_dict['Channel Id'].append(channel)
            playlist_dict['Playlist Description'].append(item['snippet']['description'])

            playlist_publish = item['snippet']['publishedAt'].split('Z')[0]
            playlist_publish = datetime.strptime(playlist_publish,f)
            playlist_dict['Published At'].append(playlist_publish)
            
        
        #Loop While Break
        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken: break
     
    #Create a dataFrame from The dicttionary "playlist_dict"
    df_playlist = pd.DataFrame(playlist_dict)
            
    #Convert to CSV
    df_playlist.to_csv(f'../data/{channel_title}/playlist.csv',index=False)
    
    return df_playlist




def get_videos(url_channel, youtube_api_key):
    '''
    Function to get the data of all videos in each playlist that was return in the previous function
    '''
    
    #Libraries
    import re
    from datetime import timedelta, datetime
    import pandas as pd
    from googleapiclient.discovery import build
    
    #Build the socket with Youtube data API through the library googleapiclient
    youtube = build('youtube','v3', developerKey=youtube_api_key)

    #Get the Title of the channel for organize in folders
    channel_title = list(get_channel(url_channel, youtube_api_key)['Channel Title'])[0]
    
    #Get the list of all playlists id from URL of youtube Channel (Previous Function)
    playlist = list(get_playlist(url_channel, youtube_api_key)['Playlist Id'])
    
    #Patterns to calculate the duration of a video
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')
    
    #formal for use in date formula
    f = "%Y-%m-%dT%H:%M:%S"
    
    #Empty Dictionary of a Video
    video_dict = {
                    "Video Id":[],
                    "Video Title":[],
                    "Playlist Id":[],
                    "View Count":[],
                    "Like Count":[],
                    "Dislike Count":[],
                    "Comment Count":[],
                    "Duration":[],
                    "Published At":[],
                    "Video Description":[]
                  }
    #Itarate in each Playlist of the list of Playlist Id
    for play in playlist:
        #Loop While Break
        nextPageToken = None
        while True:
            #Request to get data of the items in each playlist
            pl_request_items = youtube.playlistItems().list(
                                part='contentDetails, snippet',
                                playlistId=play,
                                maxResults=50,
                                pageToken = nextPageToken
                                )
            pl_response_items = pl_request_items.execute()
            
            #Empty list to use for append all the videos id in a playlist
            vid_ids = list()
            
            #Itarate in each Playlist to get all the videos Id in each playlist
            for item in pl_response_items['items']:
                vid_ids.append(item['contentDetails']['videoId'])
            
            #Request to get data of all videos in each playlist
            vid_request = youtube.videos().list(
                            part='statistics, snippet, contentDetails',
                            id=','.join(vid_ids)
                            )
            vid_response = vid_request.execute()
            
            #Append the data from videos in the "video_dict"
            for item in vid_response['items']:
                video_dict['Video Id'].append(item['id'])
                video_dict['Video Title'].append(item['snippet']['title'])
                video_dict['Playlist Id'].append(play)
                video_dict['View Count'].append(item['statistics']['viewCount'])
                video_dict['Like Count'].append(item['statistics'].get('likeCount',0))
                video_dict['Dislike Count'].append(item['statistics'].get('dislikeCount',0))
                video_dict['Comment Count'].append(item['statistics'].get('commentCount',0))
                video_dict['Video Description'].append(item['snippet']['description'])
                
                #Duration calculate
                duration = item['contentDetails']['duration']
                hours = hours_pattern.search(duration)
                minutes = minutes_pattern.search(duration)
                seconds = seconds_pattern.search(duration)
                
                hours = '00' if not hours else f'0{int(hours.group(1))}' if int(hours.group(1)) < 10 else int(hours.group(1))
                minutes = '00' if not minutes else f'0{int(minutes.group(1))}' if int(minutes.group(1)) < 10 else int(minutes.group(1))
                seconds = '00' if not seconds else f'0{int(seconds.group(1))}' if int(seconds.group(1)) < 10 else int(seconds.group(1))

                duration = f'{hours}:{minutes}:{seconds}'
                        
                video_dict['Duration'].append(duration)
                               
                
                publishedAt = item['snippet']['publishedAt'].split('Z')[0]
                publishedAt = datetime.strptime(publishedAt,f)
                video_dict['Published At'].append(publishedAt)
               
            
            #Loop While Break
            nextPageToken = pl_response_items.get('nextPageToken')
            if not nextPageToken: break
    
    
    df_video = pd.DataFrame(video_dict)
    
    #Convert to CSV
    df_video.to_csv(f'../data/{channel_title}/videos.csv',index=False)
    
    return df_video




def get_comment_videos(url_channel, youtube_api_key):
    '''
    Function to get the data of the last 50 comments of all videos in each playlist that was return in the previous function
    '''
    
    #Libraries
    from datetime import datetime
    import pandas as pd
    from googleapiclient.discovery import build
    
    #Build the socket with Youtube data API through the library googleapiclient
    youtube = build('youtube','v3', developerKey=youtube_api_key)
    
    #Get the Title of the channel for organize in folders
    channel_title = list(get_channel(url_channel, youtube_api_key)['Channel Title'])[0]
    
    #Get the list of videos id of all playlists from URL of youtube Channel (Previous Function)
    videos = list(get_videos(url_channel, youtube_api_key)['Video Id'])
    
    #formal for use in date formula
    f = "%Y-%m-%dT%H:%M:%S"
    
    #Empty Dictionary of a Comment
    comment_dict = {
                "Comment Id":[],
                "Comment":[],
                "Comment Author":[],
                "Author Comment Id":[],
                "Like Comment Count":[],
                "Total Reply Comment":[],
                "Video Id":[],
                "Published At":[],
              }
    #Request to get data of the last 50 comments of each video for all videos of all playlists in the channel
    for video in videos:
        #Some videos could has disabled comments.
        try:
            comment_request = youtube.commentThreads().list(
                                part='snippet',
                                videoId=video,
                                maxResults=50,
                                )
            comment_response = comment_request.execute()

                #Append the data from comments in the "comment_dict"
            for item in comment_response['items']:
                comment_dict['Comment Id'].append(item['id'])
                comment_dict['Comment'].append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
                comment_dict['Comment Author'].append(item['snippet']['topLevelComment']['snippet'].get('authorDisplayName',None))
                comment_dict['Author Comment Id'].append(item['snippet']['topLevelComment']['snippet']['authorChannelId'].get('value',None))
                comment_dict['Like Comment Count'].append(item['snippet']['topLevelComment']['snippet'].get('likeCount',0))
                comment_dict['Total Reply Comment'].append(item['snippet'].get('totalReplyCount',0))
                comment_dict['Video Id'].append(video)

                publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt'].split('Z')[0]
                publishedAt = datetime.strptime(publishedAt,f)
                comment_dict['Published At'].append(publishedAt)
        except: pass

    #Create a dataFrame from The dicttionary "comment_dict"
    df_comment = pd.DataFrame(comment_dict)
    
    #Convert to CSV
    df_comment.to_csv(f'../data/{channel_title}/comments.csv',index=False)
    
    return df_comment