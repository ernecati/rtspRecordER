# rtspRecordER
This script is a tool for recording RTSP streams using Python. It allows for a variety of configurations, including the ability to set the record duration, add timestamps to the recorded files, and automatically clear old recordings. 

1 - Download & Unzip Code

https://github.com/ernecati/rtspRecordER

2 - Install Dependencies
sudo apt update 
sudo apt install libwayland-cursor0 libxfixes3 libva2 libdav1d4 libavutil56 libxcb-render0 libwavpack1 libvorbis0a libx264-160 libx265-192 libaec0 libxinerama1 libva-x11-2 libpixman-1-0 libwayland-egl1 libzvbi0 libxkbcommon0 libnorm1 libatk-bridge2.0-0 libmp3lame0 libxcb-shm0 libspeex1 libwebpmux3 libatlas3-base libpangoft2-1.0-0 libogg0 libgraphite2-3 libsoxr0 libatspi2.0-0 libdatrie1 libswscale5 librabbitmq4 libhdf5-103-1 libharfbuzz0b libbluray2 libwayland-client0 libaom0 ocl-icd-libopencl1 libsrt1.4-gnutls libopus0 libxvidcore4 libzmq5 libgsm1 libsodium23 libxcursor1 libvpx6 libavformat58 libswresample3 libgdk-pixbuf-2.0-0 libilmbase25 libssh-gcrypt-4 libopenexr25 libxdamage1 libsnappy1v5 libsz2 libdrm2 libxcomposite1 libgtk-3-0 libepoxy0 libgfortran5 libvorbisenc2 libopenmpt0 libvdpau1 libchromaprint1 libpgm-5.3-0 libcairo-gobject2 libavcodec58 libxrender1 libgme0 libpango-1.0-0 libtwolame0 libcairo2 libatk1.0-0 libxrandr2 librsvg2-2 libopenjp2-7 libpangocairo-1.0-0 libshine3 libxi6 libvorbisfile3 libcodec2-0.9 libmpg123-0 libthai0 libudfread0 libva-drm2 libtheora0
sudo pip install opencv-contrib-python==4.5.5.62
pip install imutils

3 - Build FTP Server
3.1 - Upload FTP Server Package

sudo apt-get install vsftpd

3.2 - Configure FTP Server

sudo nano /etc/vsftpd.conf

3.2.1 - Edit strings below
anonymous_enable=YES ====> anonymous_enable=NO
#local_enable=YES ========> local_enable=YES
#write_enable=YES ========> write_enable=YES

3.2.2 - Add Strings Below
force_dot_files=YES
local_root=your/video/directory *ie:/home/pi/Desktop/rtspSave*

4 - Edit & Configure Codes

4.1 - RTSP Connection Settings
rtspSource = 0 #0:use rtspString value directly , 1: use parameters 

#String
rtspString = "rtsp://user:pass@192.168.1.100:8080/h264_ulaw.sdp"

#Parameters
IP = "192.168.1.100"
PORT = "8080"
EXTENTION = "h264_ulaw.sdp"
USER = "user"
PASS = "pass"

4.2 - Recording Settings
recordMin = 15 #record new video every x minutes (min: 1 - max:59)
putTime = 1 #Put date and time on recorded video (0:No / 1:Yes)
recordWidth = 320 #only width available, height will set automaticly
showImage = 0 #show live stream (0:No / 1:Yes)
fpsVal = 30 #stream and record fps (max:30 - min:1)
restartTime = 1 #System will restart if any error occures! (minute)

5 - Run Codes
sudo python rstpRecorder.py

