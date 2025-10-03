from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from video_generator import VideoGenerator

class VideoHandler():
    def __init__(self, user_query:str, user_context:str) -> None:        
        vg = VideoGenerator(user_query, user_context)
        vg.generate_video()
        text = vg.transcript
        duration_seconds = vg.VIDEO_DURATION
        # video output_video ve audio sosyal_medya_icerik.mp3 olarak kaydedildiği için o şekilde çekildi.
        # kullanıcı istenilen şekilde değiştirebilir.
        video = VideoFileClip("output_video.mp4")
        audio = AudioFileClip("sosyal_medya_icerik.mp3")
        audio = audio.subclipped(0, min(audio.duration, video.duration))

        words = text.split()
        num_words = len(words)
        word_duration = duration_seconds / num_words  # her kelime kaç saniye gösterilecek

        print(f"\nAltyazı oluşturuluyor...")
        print(f"Toplam kelime: {num_words}")
        print(f"Kelime başına süre: {word_duration:.2f}s")

        text_clips = []
        for i, word in enumerate(words):
            start_time = i * word_duration
                        
            txt_clip = TextClip(
                text=word,
                font_size=70,  
                color='yellow',
                font='c:/WINDOWS/Fonts/ARIALBD.TTF',  # Geliştiricinin bilgisayarında font pathini belirtmek gerekiyordu. Genellikle C dizini içinde Windows klasörünün altındadır.
                stroke_color='black',  
                stroke_width=2,
                method='caption',
                size=(int(video.w * 0.9), int(video.h * 0.2))  # Genişlik sınırı
            )
            
            txt_clip = txt_clip.with_position(('center', 'center')).with_start(start_time).with_duration(word_duration)
            text_clips.append(txt_clip)
            
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{num_words} kelime işlendi...")

        print("Video birleştiriliyor...")
        final_clip = CompositeVideoClip([video] + text_clips)
        final_clip = final_clip.with_audio(audio)
        final_clip.write_videofile("output_with_subtitles.mp4", fps=30, codec="libx264", audio_codec="aac")
        print("Altyazılı video oluşturuldu: output_with_subtitles.mp4")
        # Belleği temizle
        final_clip.close()
        video.close()
        audio.close()
        for clip in text_clips:
            clip.close()