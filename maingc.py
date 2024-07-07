# @title Run App 
# import locale
# locale.getpreferredencoding = lambda: "UTF-8"
from flask import Flask, request, jsonify,send_from_directory,render_template
from werkzeug.utils import secure_filename
import os
import subprocess
# import whisper
# from googletrans import Translator
from TTS.api import TTS
import torch
app = Flask(__name__)
import threading
PORT=5005
# import requests
# response = requests.get('https://raw.githubuser/content.com/iamthehimansh/Lip2Lip/main/templates/index.html')
# os.makedirs('templates', exist_ok=True)
# with open('templates/index.html', 'w') as f:
#     f.write(response.text)
def func():
    
    cmd=f'ssh -o "StrictHostKeyChecking=no" -R 80:localhost:{PORT} serveo.net'
    subprocess.run(cmd, shell=True)
threading.Thread(target=func,daemon=True).start()
# Set the upload folder for video and audio files
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# def resize_video(filename):
#     output_filename = f"resized_{filename}"
#     cmd = f"ffmpeg -i {filename} -vf 'scale=-1:720' {output_filename}"
#     subprocess.run(cmd, shell=True)
#     print(f'Resized video saved as {output_filename}')
#     return output_filename

genrated=os.path.exists("/content/output_high_qual_hi.mp4")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/vid')
def vid():
    if genrated:
        genrated=False
        return send_from_directory('/content', 'output_high_qual_hi.mp4'),200
    else:
        return "Not Generated Yet",200
    
@app.route('/process', methods=['POST'])
def generate_video():
    # Check if the request contains video, audio, and text files
    print("Request Received")
    if 'video' not in request.files or 'audio' not in request.files or 'text' not in request.form:
        return jsonify({'error': 'Video, audio, and text files are required.'}), 400
    print("Request Contains Video, Audio and Text")
    video_file = request.files['video']
    audio_file = request.files['audio']
    text = request.form['text']
    quality = request.form['quality']

    # Save the video and audio files to the upload folder
    video_filename = secure_filename(video_file.filename)
    audio_filename = secure_filename(audio_file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    video_file.save(video_path)
    audio_file.save(audio_path)

    # Generate the video based on the provided files and text
    # Replace this code with your video generation logic
    generated_video_path,code = generate_video_function(video_path, audio_path, text,quality)

    # Check if the video generation was successful
    if generated_video_path is None:
        return jsonify({'error': 'Failed to generate the video.'}), 500

    # Return the generated video file
    return generated_video_path,code

def generate_video_function(video_path, audio_path_, text_,quality="low"):
    # resized_video_path = resize_video(video_path)
    genrated=True
    resized_video_path=video_path
    

    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Initialize TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    mutual_fund_speech=text_
    cmd="rm -rf /content/output_synth_audio_final.wav"
    subprocess.run(cmd, shell=True)
    tts.tts_to_file(mutual_fund_speech,
        speaker_wav=audio_path_,
        file_path="output_synth_audio_final.wav",
        language="en"
        )
    try:
        del tts
    except NameError:
        print("Voice model already deleted")

    try:
        del model
    except NameError:
        print("Whisper model already deleted")

    torch.cuda.empty_cache()
    if quality == "low":
        cmd="cd /content/Wav2Lip "

        #This is the detection box padding, if you see it doesnt sit quite right, just adjust the values a bit. Usually the bottom one is the biggest issue
        pad_top =  0
        pad_bottom =  15
        pad_left =  0
        pad_right =  0
        rescaleFactor =  1

        video_path_fix = f"'../{resized_video_path}'"
        subprocess.run(cmd, shell=True)
        cmd=f"python inference.py --checkpoint_path 'checkpoints/wav2lip_gan.pth' --face {video_path_fix} --audio '/content/output_synth_audio_final.wav' --pads {pad_top} {pad_bottom} {pad_left} {pad_right} --resize_factor {rescaleFactor} --nosmooth --outfile '/content/output_high_qual_hi.mp4'"
        # f"python inference.py --checkpoint_path 'checkpoints/wav2lip_gan.pth' --face /content/uploads/VID-20240601-WA0039.mp4 --audio '/content/output_synth_audio_final.wav' --pads 0 15 0 0 --resize_factor 1 --nosmooth --outfile '/content/output_high_qual_hi.mp4'"
        subprocess.run(cmd, shell=True)
    else:
        cmd="cd /content/video-retalking &&"

        video_path_fix = f"'../{resized_video_path}'"
        cmd+="rm -rf ../output_high_qual_hi.mp4 &&"
        cmd+=f"""python inference.py \
        --face {video_path_fix} \
        --audio {"../output_synth_audio_final.wav"} \
        --outfile {'../output_high_qual_hi.mp4'}"""+ " && cd ../.."
        f"""python inference.py --face /content/uploads/VID-20240601-WA0039.mp4 --audio "/content/output_synth_audio_final.wav" --outfile '/content/output_high_qual_hi2.mp4'"""
        subprocess.run(cmd, shell=True)
    genrated=True
    return send_from_directory('/content', 'output_high_qual_hi.mp4'),200

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=PORT)