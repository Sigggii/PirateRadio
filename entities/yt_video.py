from pytube import YouTube


def url_to_song(url: str):
    song_info = YouTube(url)
    return YTvideo(url, song_info.title, song_info.author, song_info.length)


def video_list_to_mongo_entities(video_list: []):
    mongo_list = []
    video: YTvideo
    for video in video_list:
        mongo_list.append(video.to_mongo_entity())

    return mongo_list


"""Represents a YoutubeVideo, the url is the watch url, not the stream url because that one can expire"""


class YTvideo:
    def __init__(self, url: str, title: str, author: str, length: int):
        self.url = url
        self.title = title
        self.author = author
        self.length = length

    def to_mongo_entity(self):
        return {'url': self.url, 'title': self.title, 'author': self.author, 'length': self.length}
