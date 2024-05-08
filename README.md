█▀▀▀█ █▀▀█ ▀▀█▀▀ █▀▀▀█ █▀▀█ █  █ █▀▀▀█ █▄  █ ▀█▀ █▀▀█ 
█   █ █      █   █   █ █▄▄█ █▀▀█ █   █ █ █ █  █  █    
█▄▄▄█ █▄▄█   █   █▄▄▄█ █    █  █ █▄▄▄█ █  ▀█ ▄█▄ █▄▄█ 

███ ▀▄▀   ▄▀█ █ █ █▀▄ █ █▀█   █▀█ █   ▄▀█ █▄█ █▀▀ █▀█ 
█▄█ █ █   █▀█ █▄█ █▄▀ █ █▄█   █▀▀ █▄▄ █▀█  █  ██▄ █▀▄ 

v0.1 Alpha

This is an 8 Track audio player written in Python for the [HifiBerry DAC8](https://www.hifiberry.com/shop/boards/hifiberry-dac8x/). I don't write Python often, so this is not very good and it barely works.

You will need to setup a virtual environment to run the code. You can do this by running the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a directory to place the tracks you want to play. In this example we will use the directory `tracks`. You can use any folder you wqnt. You can use the following command:

```bash
mkdir tracks
```

Place your multi-track audio files in the directory you created in the previous step. Place each song in a separate folder. The code will play the songs/tracks in the order they are listed in the directory. If more than 8 tracks are present, the code will only play the first 8 tracks.

```
tracks
├── 01_Dangerous_Match_One
│   └── 01_drums.wav
│   └── 02_bass.wav
│   └── 03_gtar.wav
│   └── 04_gtar2.wav
│   └── 05_keys.wav
│   └── 06_horns.wav
│   └── 07_vox.wav
│   └── 08_vox2.wav
├── track2
│   └── track1.wav
│   └── track2.wav
│   └── track3.wav
│   ...
```

To run the code, you can use the following command:
Replace `./tracks` with the directory you created in the previous step.

```bash
sudo ./venv/bin/python3 ./player.py ./tracks
```

The code will start playing the tracks in the directory `tracks`. You can stop the code by pressing `Ctrl+C`.

```
Controls:
Space: Play/Pause
N: Next track
P: Previous track
```