from data.mongo_client import get_mongoclient
from datetime import datetime
from datetime import timezone
from entities.yt_video import YTvideo, video_list_to_mongo_entities


class PlaylistDB:

    def __init__(self):
        self.mongo_client = get_mongoclient()["pirateradio"]
        self.playlist_coll = self.mongo_client["playlists"]

    def create_playlist(self, guild_id: int, playlist_name: str, creator: int):
        self.playlist_coll.insert_one({'guild_id': guild_id, 'name': playlist_name, 'creator': creator, 'created_on': datetime.now(tz=timezone.utc)})

    def get_playlist(self, guild_id: int, playlist_name: str):
        self.playlist_coll.find_one({'guild_id': guild_id, 'name': playlist_name})

    def delete_playlist(self, guild_id: int, playlist_name: str):
        self.playlist_coll.delete_one({'guild_id': guild_id, 'name': playlist_name})

    def add_video(self, guild_id: int, playlist_name: str, video: YTvideo):
        result = self.playlist_coll.update_one({'guild_id': guild_id, 'name': playlist_name}, {'$push': {'videos': video}})
        return result.raw_result["nModified"]

    def add_videos(self, guild_id: int, playlist_name: str, videos: []):
        mongo_entities = video_list_to_mongo_entities(videos)
        result = self.playlist_coll.update_one({'guild_id': guild_id, 'name': playlist_name}, {'$push': {'videos': {'$each': mongo_entities}}})
        return result.raw_result["nModified"]

    def get_videos(self, guild_id: int, playlist_name: str):
        return self.playlist_coll.find_one({'guild_id': guild_id, 'name': playlist_name}, {'videos': 1})['videos']

    def delete_video_by_title(self, guild_id: int, playlist_name: str, title: str):
        result = self.playlist_coll.update_one({'guild_id': guild_id, 'name': playlist_name}, {'$pull': {'videos': {'title' : title}}})
        print(title)
        return result.raw_result["nModified"]

    def delete_video_by_author(self, guild_id: int, playlist_name: str, author: str):
        result = self.playlist_coll.update_one({'guild_id': guild_id, 'name': playlist_name}, {'$pull': {'videos': {'author' : author}}})
        print(str(result.raw_result) + " " + author)
        return result.raw_result["nModified"]

