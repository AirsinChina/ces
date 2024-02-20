from music21 import *
import random
import inspect

# 基本音级
BASE_NOTE = ['C', 'D', 'E', 'G', 'A']
# 节拍类型
BEAT_TYPE = ['2/4', '3/4', '4/4']
# 三种基本调式的音程关系 (清乐, 雅乐, 燕乐)
KEY_MODE_INTERVAL = [
    [2, 2, 1, 2, 2, 2, 1],
    [2, 2, 2, 1, 2, 2, 1],
    [2, 2, 1, 2, 2, 1, 2]
]
# 基本调式对应的调式名称
KEY_MODE_NAME = ["清乐", "雅乐", "燕乐"]
# 调式主音的选择权重, 偏音不能成为调式主音
MAIN_NOTE_WEIGHT = [20, 20, 20, 0, 20, 20, 0]
# 调式主音对应的音级名称
MAIN_NOTE_NAME = ["宫", "商", "角", "偏1", "徵", "羽", "偏2"]


class Melody:
    """旋律类"""
    def __init__(self):
        # 实例属性的初始化
        self.beat_text = ""  # 拍号的说明文字
        self.melody_measure = stream.Measure()  # 旋律最终的 Measure 对象
        self.key_mode_type = ""  # 调式类型的字符串说明, 取值可能是清乐雅乐燕乐
        self.main_note_type = ""  # 调式类型的字符串说明, 取值可能是宫商角徵羽
        self.main_note_name = ""  # 调式主音音名的字符串
        # 对节拍与调性宫音做出选择
        self.key = self.choose_key()  # 挑选调号 (调式宫音)
        self.beat = self.choose_beat()  # 挑选拍号
        self.set_signature()  # 设置调号和拍号
        # 对调式与调式主音做出选择
        self.key_mode = self.choose_key_mode()  # 挑选七声调式类型, 返回包含音程关系数的 List
        self.gong_scale = self.generate_gong_scale()  # 根据调号和调式类型, 生成对应的宫调式音阶, 返回的是 Note对象组成的 List
        self.main_note = self.choose_main_note()  # 挑选调式主音
        # 最终的说明
        self.key_text = self.get_key_text()  # 调式调性的说明文字
        self.print_init_msg()  # 输出初始化信息, 包含节拍与调式调性的信息

    def show_melody(self):
        """展示旋律"""
        self.melody_measure.show()

    def choose_key(self):
        """挑选调号"""
        chosen_key = random.choice(BASE_NOTE)
        print(f"{inspect.currentframe().f_lineno} 行, 此次挑选了 {chosen_key} 为调式宫音.")
        return chosen_key

    def choose_beat(self):
        """挑选拍号"""
        chosen_beat = random.choice(BEAT_TYPE)
        self.beat_text = f"{chosen_beat} 拍"
        print(f"{inspect.currentframe().f_lineno} 行, 此次挑选了 {self.beat_text}.")
        return chosen_beat

    def set_signature(self):
        """根据挑选的调号拍号设置"""
        # 设置拍号
        time_signature = meter.TimeSignature(self.beat)
        self.melody_measure.append(time_signature)
        # 设置调号
        self.melody_measure.append(key.Key(self.key))

    def choose_key_mode(self):
        """挑选调式"""
        chosen_key_mode = random.choice(KEY_MODE_INTERVAL)
        self.key_mode_type = KEY_MODE_NAME[KEY_MODE_INTERVAL.index(chosen_key_mode)]
        print(f"{inspect.currentframe().f_lineno} 行, 此次挑选了 {self.key_mode_type} 调式.")
        return chosen_key_mode  # 返回的是包含音程关系数的 List

    def generate_gong_scale(self):
        """生成对应的宫调式音阶"""
        # 生成在小字一组的宫音对象
        gong_note = note.Note()
        gong_note.name = self.key
        gong_note.octave = 4
        # 根据调式类型生成对应的宫调式音阶
        gong_scale = [gong_note]
        for i in self.key_mode[:-1]:
            gong_note = gong_note.transpose(i)
            gong_scale.append(gong_note)
        print(f"{inspect.currentframe().f_lineno} 行, 生成的对应宫调式音阶: {gong_scale}.")
        return gong_scale  # 返回的是 Note对象组成的 List

    def choose_main_note(self):
        """挑选主音"""
        # 从生成的宫调式音阶中根据主音的权重挑选调式主音
        chosen_main_note = random.choices(self.gong_scale, MAIN_NOTE_WEIGHT, k=1)[0]
        chosen_main_note_type = MAIN_NOTE_NAME[self.gong_scale.index(chosen_main_note)]
        # 调式类型, 即宫商角徵羽
        self.main_note_type = chosen_main_note_type
        # 调式主音音名
        self.main_note_name = chosen_main_note.nameWithOctave
        print(f"{inspect.currentframe().f_lineno} 行, 此次挑选了 {chosen_main_note_type} 作为调式主音.")
        return chosen_main_note  # 返回的是一个 note.Note

    def get_key_text(self):
        """生成对应的调式调性说明文字"""
        return f"{self.main_note_name[0]} {self.main_note_type} {self.key_mode_type} 调式"

    def print_init_msg(self):
        """打印输出初始化文字"""
        print(f"初始化完成! 此次旋律为 {self.beat_text}, 调式调性为 {self.key_text}.")


if __name__ == "__main__":
    mld_1 = Melody()
    mld_1.show_melody()
