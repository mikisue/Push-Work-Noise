import os
import sounddevice as sd
import tkinter as tk
from tkinter import ttk, messagebox
from pydub import AudioSegment
import numpy as np

class WhiteNoiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("白噪音学习助手")
        self.root.geometry('500x500')
        self.is_playing = False
        self.current_audio_data = None
        self.sample_rate = None
        self.volume = 0.5

        self.DEFAULT_SOUNDS = {
            "1": ("清晨村庄声", "early-morning-sound-in-village-345750.mp3"),
            "2": ("鸟鸣声", "birds-19624.mp3"),
            "3": ("轻柔雨声", "gentle-rain-for-relaxation-and-sleep-337279.mp3"),
            "4": ("波兰森林声", "forest-atmosphere-013-localization-poland-369645.mp3"),
            "5": ("森林环境声", "forest-ambience-296528.mp3"),
        }

        # 设置 FFmpeg 路径
        self.setup_ffmpeg()

        self.create_widgets()

    def setup_ffmpeg(self):
        """设置本地指定的 FFmpeg 路径（固定路径）"""
        ffmpeg_path = r"F:\ffmpeg\bin"
        ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
        ffprobe_exe = os.path.join(ffmpeg_path, "ffprobe.exe")

        # 检查 ffmpeg 和 ffprobe 是否存在
        if not os.path.isfile(ffmpeg_exe):
            raise FileNotFoundError(f"未找到 ffmpeg.exe，请确认路径是否正确：{ffmpeg_exe}")
        if not os.path.isfile(ffprobe_exe):
            raise FileNotFoundError(f"未找到 ffprobe.exe，请确认路径是否正确：{ffprobe_exe}")

        # 设置 pydub 使用的路径
        AudioSegment.converter = ffmpeg_exe
        AudioSegment.ffmpeg = ffmpeg_exe
        AudioSegment.ffprobe = ffprobe_exe

        # 将 ffmpeg 路径加入系统 PATH（确保子进程调用正常）
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")

        # 可选：设置 PYDUB_FFMPEG 和 PYDUB_FFPROBE 环境变量（有些库会读取这些变量）
        os.environ["PYDUB_FFMPEG"] = ffmpeg_exe
        os.environ["PYDUB_FFPROBE"] = ffprobe_exe

        print("[调试] FFmpeg 路径配置成功")

    def create_widgets(self):
        """创建GUI组件"""
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=tk.YES)

        title_label = ttk.Label(frame, text="选择您的背景音效", font=('Helvetica', 20))
        title_label.pack(pady=10)

        # 音效选择框
        self.sound_var = tk.StringVar(value=[name for name, _ in self.DEFAULT_SOUNDS.values()][0])
        self.sound_combo = ttk.Combobox(frame, textvariable=self.sound_var, state="readonly",
                                        values=[name for name, _ in self.DEFAULT_SOUNDS.values()])
        self.sound_combo.pack(pady=10, fill=tk.X)

        # 控制按钮
        control_frame = ttk.Frame(frame)
        control_frame.pack(pady=10)

        self.play_button = ttk.Button(control_frame, text="播放", command=self.toggle_play)
        self.play_button.grid(row=0, column=0, padx=5)

        stop_button = ttk.Button(control_frame, text="停止", command=self.stop_audio)
        stop_button.grid(row=0, column=1, padx=5)

        # 音量控制
        volume_frame = ttk.Frame(frame)
        volume_frame.pack(pady=10, fill=tk.X)

        ttk.Label(volume_frame, text="音量:").pack(side=tk.LEFT)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL,
                                       command=self.update_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)

    def toggle_play(self):
        """播放或暂停音频"""
        if not self.is_playing:
            selected_name = self.sound_var.get()
            print(f"[调试] 选择的音效名称: {selected_name}")

            filename = [file for name, file in self.DEFAULT_SOUNDS.values() if name == selected_name][0]
            print(f"[调试] 尝试加载的文件路径: {filename}")  # 打印文件路径

            if not filename:
                print(f"[错误] 未找到音效文件: {selected_name}")
                return
            print(f"[调试] 尝试加载的文件路径: {filename}")

            self.load_and_play(filename)
        else:
            self.stop_audio()

    def load_and_play(self, filename):
        """加载并开始播放音频"""
        print(f"[调试] 进入 load_and_play，文件路径: {filename}")
        try:
            base_dir = os.path.dirname(__file__)
            sound_dir = os.path.join(base_dir, "source_mp3")
            file_path = os.path.join(sound_dir, filename)

            print(f"[调试] 文件绝对路径: {file_path}")

            if not os.path.exists(file_path):
                print(f"[错误] 文件不存在: {file_path}")
                messagebox.showerror("播放失败", f"文件不存在：{file_path}")
                return

            # 加载音频
            audio = AudioSegment.from_mp3(file_path)
            audio = audio.set_channels(1)  # 单声道
            samples = np.array(audio.get_array_of_samples())
            print(f"[调试] 成功加载音频文件: {file_path}")

            sd.play(samples.astype(np.float32) / 32768.0, audio.frame_rate)


            self.is_playing = True
            self.play_button.config(text="暂停")

        except Exception as e:
            print(f"[错误] 加载音频失败: {e}")
            messagebox.showerror("播放失败", f"文件无法播放：{filename}")
            import traceback
            traceback.print_exc()

    def stop_audio(self):
        """停止播放"""
        self.is_playing = False
        sd.stop()
        self.play_button.config(text="播放")
        print("[信息] 停止播放")

    def update_volume(self, value):
        """更新音量"""
        self.volume = float(value)
        print(f"[调试] 当前音量: {self.volume}")