from flask import Flask, render_template, request, send_from_directory
import ffmpeg
import os
import textwrap
import uuid
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

def generate_video_with_veo(prompt, output_path):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    client = genai.Client(api_key=api_key)

    print(f"Starting video generation with Veo for prompt: {prompt}")
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
    )

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    if operation.exception:
        raise Exception(f"Video generation failed: {operation.exception}")

    # Download the generated video.
    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(output_path)
    print(f"Generated video saved to {output_path}")


def create_video_from_text(text, music_path, output_path):
    # Video settings
    width = 1280
    height = 720
    fps = 25
    duration_per_char = 0.1
    font_size = 48
    font_color = 'white'
    box_color = 'black'
    font_file = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

    # Wrap text
    wrapped_text = "\n".join(textwrap.wrap(text, width=40))

    # Calculate video duration
    duration = len(wrapped_text) * duration_per_char

    # Create a blank video stream
    input_video = ffmpeg.input(f'color=c=black:s={width}x{height}:d={duration}', f='lavfi')

    # Add text overlay
    video_with_text = ffmpeg.drawtext(
        input_video,
        text=wrapped_text,
        fontfile=font_file,
        fontsize=font_size,
        fontcolor=font_color,
        box=1,
        boxcolor=box_color + '@0.5',
        boxborderw=10,
        x='(w-text_w)/2',
        y='(h-text_h)/2'
    )

    # Add audio
    input_audio = ffmpeg.input(music_path)
    output_video = ffmpeg.output(video_with_text, input_audio, output_path, vcodec='libx264', acodec='aac', strict='experimental', t=duration)

    # Run ffmpeg
    ffmpeg.run(output_video, overwrite_output=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    video_filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join('videos', video_filename)

    try:
        if os.getenv("GOOGLE_API_KEY"):
            generate_video_with_veo(text, output_path)
        else:
            # Fallback to local generation if no API key is provided
            # This allows testing without a real API key if needed
            music_file = 'music/background.mp3'
            create_video_from_text(text, music_file, output_path)
    except Exception as e:
        return render_template('index.html', error=str(e))

    return render_template('index.html', video_path=f'/videos/{video_filename}')

@app.route('/videos/<filename>')
def video(filename):
    return send_from_directory('videos', filename)

if __name__ == '__main__':
    if not os.path.exists('videos'):
        os.makedirs('videos')
    if not os.path.exists('music'):
        os.makedirs('music')
    app.run(debug=True, port=3000)
