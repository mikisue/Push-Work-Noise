import os
import sounddevice as sd
import numpy as np
import time
from pydub import AudioSegment


# 设置 ffmpeg 路径（非常重要！！！）
os.environ["PATH"] = r"F:\ffmpeg\bin" + os.pathsep + os.environ.get("PATH", "")
os.environ["PYDUB_FFPROBE"] = r"F:\ffmpeg\bin\ffprobe.exe"
os.environ["PYDUB_FFMPEG"] = r"F:\ffmpeg\bin\ffmpeg.exe"

AudioSegment.converter = r"F:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"F:\ffmpeg\bin\ffprobe.exe"


# 设置 ffmpeg 路径（非常重要）
AudioSegment.converter = r"F:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"F:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"F:\ffmpeg\bin\ffprobe.exe"

# 加入系统 PATH
os.environ["PATH"] = r"F:\ffmpeg\bin" + os.pathsep + os.environ.get("PATH", "")

# 打印调试信息
print("Current PATH:", os.environ["PATH"])

# 加载 MP3 文件
def load_mp3_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"找不到文件: {filename}")
    print("正在加载文件...")
    audio = AudioSegment.from_mp3(filename)
    audio = audio.set_channels(1)  # 单声道
    samples = np.array(audio.get_array_of_samples())
    return samples.astype(np.float32) / 32768.0, audio.frame_rate

# 播放音频
def play_audio(audio_data, samplerate):
    print("🔊 正在播放自然白噪音...")
    sd.play(audio_data, samplerate=samplerate)

# 停止播放
def stop_audio():
    sd.stop()
    print("⏹️ 已停止播放")

# 主程序
if __name__ == "__main__":
    sounds = {
        "1": "early-morning-sound-in-village-345750.mp3",
        "2": "birds-19624.mp3",
        "3": "gentle-rain-for-relaxation-and-sleep-337279.mp3",
        "4": "forest-atmosphere-013-localization-poland-369645.mp3",
        "5": "forest-ambience-296528.mp3"
    }

    print("请选择一种自然白噪音：")
    for key, file in sounds.items():
        print(f"[{key}] {file.split('.')[0]}")

    choice = input("请输入编号：").strip()
    sound_file = sounds.get(choice)

    if not sound_file:
        print("❌ 输入无效，请重试。")
        exit()

    print("当前工作目录:", os.getcwd())
    print("文件是否存在:", os.path.exists(sound_file))

    if not os.path.exists(sound_file):
        print("❌ 文件不存在，请检查文件名或路径")
        exit()

    try:
        audio_data, sample_rate = load_mp3_file(sound_file)
        duration = len(audio_data) / sample_rate
        print(f"⏱️ 即将播放《{sound_file}》，持续时间：{int(duration)} 秒")

        play_audio(audio_data, sample_rate)

        remaining = int(duration)
        for i in range(remaining):
            print(f"\r⏳ 学习中...（剩余时间：{remaining - i} 秒）", end="")
            time.sleep(1)
        print("\n✅ 白噪音播放完毕，现在可以休息啦！")

        stop_audio()

    except Exception as e:
        print(f"⚠️ 发生错误：{e}")