from googleapiclient.discovery import build

api_key = 'AIzaSyApFJLZu6l0pbTgHUMOddWKHWScvHEGJGI'
youtube = build('youtube', 'v3', developerKey=api_key)



class YoutubeFinder:
    def __init__(self):
        self.video_ids = []
        self.play_list_id = ""


    def get_channel_info(self, category, id):

        req = youtube.channels().list(part=category, id=id)
        res = req.execute()
        items = res.get("items")
        for item in items:
            channel_id = item.get("id")
            title = item.get("snippet").get("title")
            published_at = item.get("snippet").get("publishedAt")
            stats = item.get("statistics")
            playlist_id = item.get("contentDetails").get("relatedPlaylists").get("uploads")
            self.play_list_id = playlist_id
            channel_details = {
                "channel_id": channel_id,
                "title": title,
                "published_At": published_at,
                "views_count": stats.get("viewCount"),
                "subscriber_count": stats.get("subscriberCount"),
                "video_count": stats.get("videoCount"),
                "playlist_id": playlist_id

            }
            return channel_details

    def get_playlist(self, category, id):
        req = youtube.playlistItems().list(part=category, playlistId=id)
        res = req.execute()
        items = res.get("items")

        for item in items:
            video_id = item.get("contentDetails").get("videoId")
            self.video_ids.append(video_id)
        return self.video_ids

    @staticmethod
    def get_video_info(category, id):

        req = youtube.videos().list(part=category, id=id)
        res = req.execute()
        items = res.get("items")
        for item in items:
            channel_id = item.get("snippet").get("channelId")
            video_id = item.get("id")
            video_title = item.get("snippet").get("title")
            video_stats = item.get("statistics")
            viewCount = video_stats.get("viewCount")
            likeCount = video_stats.get("likeCount")
            favoriteCount = video_stats.get("favoriteCount")
            commentCount = video_stats.get("commentCount")

            video_info = {
                "channel_id": channel_id,
                "video_id": video_id,
                "video_title": video_title,
                "viewCount": viewCount,
                "likeCount": likeCount,
                "favoriteCount": favoriteCount,
                "commentCount": commentCount
            }
            return video_info

# ytube = YoutubeFinder()
# channel_info = ytube.get_channel_info("snippet,contentDetails,statistics", "UCUAaV8D54bHDfSNLhWS61Ow")
# playlists = ytube.get_playlist("contentDetails", ytube.play_list_id)
#
# video_list_cols =[]
# video_len = 0
# for x in ytube.video_ids:
#     video = ytube.get_video_info("snippet,statistics", x)
#     video_len += 1
#     if video_len == 1:
#         video_list_cols.append((video))
