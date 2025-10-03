import os
import requests
from dotenv import load_dotenv
from moviepy import VideoFileClip, concatenate_videoclips
from vocalize import Vocalize

class VideoGenerator:
    def __init__(self, user_query:str, user_context:str) -> None:
        load_dotenv()
        self.PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
        self.TEMP_DIR = 'temp_videos'
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        self.FINAL_VIDEO = "output_video.mp4"
        self.VIDEOS_PER_QUERY = 15
        self.vocalize = Vocalize(user_context)
        self.transcript = self.vocalize.return_script()
        self.VIDEO_DURATION = self.vocalize.find_duration() + 5
        self.PROMPT_TEXT = user_query
        self.TARGET_WIDTH = 1080
        self.TARGET_HEIGHT = 1920
        
    def search_pexels_videos(self, query:str, per_page:int=3) -> list:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.PEXELS_API_KEY}
        params = {"query": query, "per_page": per_page, "size": "large", "orientation": "portrait"}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            print("Pexels API hatası:", resp.text)
            return []
        data = resp.json()
        return [video["video_files"][0]["link"] for video in data.get("videos", [])]

    def download_video(self, url:str, file_path:str):
        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        f.write(chunk)
                return True
        except Exception as e:
            print("Video indirilemedi:", e)
        return False

    def resize_and_crop(self, clip: VideoFileClip, target_width:int, target_height:int) -> VideoFileClip:
        """Videoyu hedef boyuta sığdırır ve gerekirse kırpar"""
        clip_width, clip_height = clip.size
        clip_ratio = clip_width / clip_height
        target_ratio = target_width / target_height
        if clip_ratio > target_ratio:
            new_height = target_height
            new_width = int(clip_width * (target_height / clip_height))
            resized = clip.resized(height=new_height)
            x_center = new_width / 2
            x1 = int(x_center - target_width / 2)
            cropped = resized.cropped(x1=x1, width=target_width)
        else:
            new_width = target_width
            new_height = int(clip_height * (target_width / clip_width))
            resized = clip.resized(width=new_width)
            y_center = new_height / 2
            y1 = int(y_center - target_height / 2)
            cropped = resized.cropped(y1=y1, height=target_height)
        return cropped

    def generate_video(self) -> None:
        video_urls = self.search_pexels_videos(self.PROMPT_TEXT, per_page=self.VIDEOS_PER_QUERY)
        if not video_urls:
            raise ValueError("Pexels'ten video bulunamadı. Query'i değiştirin.")

        video_files = []
        for i, url in enumerate(video_urls):
            file_path = os.path.join(self.TEMP_DIR, f"video_{i}.mp4")
            if not os.path.exists(file_path):
                print(f"İndiriliyor: {url}")
                if self.download_video(url, file_path):
                    video_files.append(file_path)
            if len(video_files) == self.VIDEOS_PER_QUERY:
                break

        if not video_files:
            raise ValueError("Hiçbir video indirilemedi.")

        clips = []
        for file_path in video_files:
            try:
                clip = VideoFileClip(file_path)
                resized_clip = self.resize_and_crop(clip, self.TARGET_WIDTH, self.TARGET_HEIGHT)
                min_clip_duration = self.VIDEO_DURATION / self.VIDEOS_PER_QUERY
                short_clip = resized_clip.subclipped(0, min(min_clip_duration, resized_clip.duration))
                clips.append(short_clip)
                print(f"Video yüklendi: {file_path} - Boyut: {short_clip.size}")
            except Exception as e:
                print(f"Video yüklenemedi: {file_path}, hata: {e}")

        if not clips:
            raise ValueError("Hiçbir video yüklenemedi. Çalışmayı durduruyoruz.")

        final_clips = []
        current_duration = 0
        clip_index = 0

        while current_duration < self.VIDEO_DURATION:
            clip = clips[clip_index % len(clips)]
            remaining = self.VIDEO_DURATION - current_duration
            if remaining >= clip.duration:
                final_clips.append(clip)
                current_duration += clip.duration
            else:
                final_clips.append(clip.subclipped(0, remaining))
                current_duration += remaining
            clip_index += 1

        print("Videolar birleştiriliyor...")
        final_clip = concatenate_videoclips(final_clips, method="compose")
        final_clip.write_videofile(self.FINAL_VIDEO, fps=30, codec="libx264")
        final_clip.close()

        for clip in clips:
            try:
                clip.close()
            except:
                pass

        print("Video oluşturuldu:", self.FINAL_VIDEO)