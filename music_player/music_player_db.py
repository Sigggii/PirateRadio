from data.mongo_client import get_mongoclient
from datetime import datetime
from datetime import timezone
from typing import Optional
from entities.yt_video import YTvideo, video_list_to_mongo_entities


class MusicPlayerDB:
    def __init__(self):
        self.mongo_client = get_mongoclient()["pirateradio"]
        self.music_player_coll = self.mongo_client["musicplayers"]

    """Create new MusicPlayer Document if no one exist yet for the given Server"""
    def create_if_new(self, guild_id: int):
        result = self.music_player_coll.find_one({"guild_id": guild_id})
        if not result:
            new_music_player = {"guild_id": guild_id, "joined": datetime.now(tz=timezone.utc)}
            self.music_player_coll.insert_one(new_music_player)

    def add_song(self, video: YTvideo, guild_id: int):
        self.music_player_coll.update_one({'guild_id': guild_id}, {'$push': {'queue': video.to_mongo_entity()}})

    def add_songs(self, guild_id: int, videos: []):
        self.music_player_coll.update_one({'guild_id': guild_id}, {'$push': {'queue': {'$each': videos}}})

    def next_song(self, guild_id: int) -> Optional[YTvideo]:
        result = self.music_player_coll.find_one({'guild_id': guild_id},{'queue': {'$slice': 1}, 'queue': 1})
        if not result:
            return None

        if not 'queue' in result:
            return None

        queue = result['queue']
        if len(queue) == 0:
            return None
        json_song = queue[0]
        self.music_player_coll.update_one({'guild_id': guild_id}, {'$pop': {'queue': 1}})
        return YTvideo(json_song["url"], json_song["title"], json_song["author"], json_song["length"])

    def change_currently_playing(self, song: YTvideo, guild_id: int):
        self.music_player_coll.update_one({'guild_id': guild_id}, {'$set': {'currently_playing': song.to_mongo_entity()}})

    def clear_queue(self, guild_id):
        self.music_player_coll.update_one({'guild_id': guild_id}, {'$set': {'queue': []}})




