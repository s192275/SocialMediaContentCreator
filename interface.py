import gradio as gr
from video_handler import VideoHandler
  
VIDEO_PATH = "output_with_subtitles.mp4"

def show_video(title: str, context: str):
    try:
        VideoHandler(title, context)
        return VIDEO_PATH
    except Exception as e:
        print(f"Hata: {e}")
        return None

with gr.Blocks(title="Sosyal Medya İçerik Oluşturucu") as demo:
    gr.Markdown(
        "# Sosyal Medya İçerik Oluşturucu\n\n"
        "Sosyal medya platformlarınız için oluşturulmasını istediğiniz fikri ve içeriğini girin ardından videonuz hazır hale gelsin."
    )

    with gr.Row():
        with gr.Column(scale=1):
            text1_in = gr.Textbox(
                label="Başlık", 
                placeholder="Lütfen sosyal medya videonuz için içerik başlığını girin. (Mümkünse birkaç kelime ve İngilizce olsun nature gibi.)",
                lines=1
            )
            text2_in = gr.Textbox(
                label="İçerik", 
                placeholder="Lütfen sosyal medya videonuz için içerik fikrini girin",
                lines=3
            )       
            show_btn = gr.Button("Videoyu Göster")

        with gr.Column(scale=1):
            video_out = gr.Video(
                label="Video",
                autoplay=False
            )

    show_btn.click(
        fn=show_video, 
        inputs=[text1_in, text2_in], 
        outputs=video_out
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)