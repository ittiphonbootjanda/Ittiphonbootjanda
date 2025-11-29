from flask import Flask, render_template, request, send_from_directory
import ffmpeg
import os
import textwrap
import uuid
from dotenv import load_dotenv

load_dotenv('.env.local')

app = Flask(__name__)

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
    music_file = 'music/background.mp3'
    video_filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join('videos', video_filename)

    create_video_from_text(text, music_file, output_path)

    return render_template('index.html', video_path=f'/videos/{video_filename}')

@app.route('/videos/<filename>')
def video(filename):
    return send_from_directory('videos', filename)

if __name__ == '__main__':
    if not os.path.exists('videos'):
        os.makedirs('videos')
    if not os.path.exists('music'):
        os.makedirs('music')

    host = os.environ.get('FLASK_RUN_HOST')
    port = os.environ.get('FLASK_RUN_PORT')

    app.run(debug=True, host=host, port=port)
