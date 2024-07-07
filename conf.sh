pip install TTS
# pip install git+https://github.com/openai/whisper.git
# pip install jiwer
# pip install googletrans==4.0.0-rc1
mkdir content -p
cd content
git clone https://github.com/justinjohn0306/Wav2Lip
cd Wav2Lip && pip install -r requirements_colab.txt


# wget "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" -O "face_detection/detection/sfd/s3fd.pth"
# wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth' -O 'checkpoints/wav2lip.pth'
wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip_gan.pth' -O 'checkpoints/wav2lip_gan.pth'
# wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/resnet50.pth' -O 'checkpoints/resnet50.pth'
wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/mobilenet.pth' -O 'checkpoints/mobilenet.pth'

pip install batch-face


cd ..

git clone https://github.com/vinthony/video-retalking.git &> /dev/null

sudo apt-get install -y libblas-dev liblapack-dev libx11-dev libopenblas-dev

git clone https://github.com/davisking/dlib.git

pip install basicsr==1.4.2 face-alignment==1.3.4 kornia==0.5.1 ninja==1.10.2.3 einops==0.4.1 facexlib==0.2.5 librosa==0.9.2 build

cd dlib && python setup.py install
cd ..

cd video-retalking

mkdir ./checkpoints
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/30_net_gen.pth -O ./checkpoints/30_net_gen.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/BFM.zip -O ./checkpoints/BFM.zip
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/DNet.pt -O ./checkpoints/DNet.pt
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/ENet.pth -O ./checkpoints/ENet.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/expression.mat -O ./checkpoints/expression.mat
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/face3d_pretrain_epoch_20.pth -O ./checkpoints/face3d_pretrain_epoch_20.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/GFPGANv1.3.pth -O ./checkpoints/GFPGANv1.3.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/GPEN-BFR-512.pth -O ./checkpoints/GPEN-BFR-512.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/LNet.pth -O ./checkpoints/LNet.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/ParseNet-latest.pth -O ./checkpoints/ParseNet-latest.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/RetinaFace-R50.pth -O ./checkpoints/RetinaFace-R50.pth
wget https://github.com/vinthony/video-retalking/releases/download/v0.0.1/shape_predictor_68_face_landmarks.dat -O ./checkpoints/shape_predictor_68_face_landmarks.dat
unzip -d ./checkpoints/BFM ./checkpoints/BFM.zip
cd ..

git clone https://github.com/vinthony/video-retalking.git &> /dev/null

pip install torchvision==0.15.2