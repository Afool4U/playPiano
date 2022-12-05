# -*- coding : utf-8 -*-
"""
@author: Github-Afool4U
@Description: playPiano.py
@Date: 2022-12-5 12:07

"""

from os import environ
import threading

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time


class PlayPiano(threading.Thread):
    # 设置成类变量，保证所有实例共享同一个音频播放器
    pygame.mixer.init()
    pygame.mixer.set_num_channels(1000)
    sounds = {}  # 音频缓存
    pitchs = ('_', '▁', '▂', '▃', '▄', '▅', '▆', '▇')  # 音高符号
    for i in range(1, 8):
        for j in ['m', 'h', 'l']:
            sounds[j + str(i)] = pygame.mixer.Sound('resources\\audio\\' + j + str(i) + '.mp3')
            if j != 'm':
                sounds[2 * j + str(i)] = pygame.mixer.Sound('resources\\audio\\' + 2 * j + str(i) + '.mp3')
    sounds['m0'] = pygame.mixer.Sound('resources\\audio\\m0.mp3')  # 休止符

    def __init__(self, times, notes_visible=False):
        super().__init__(target=self.play)
        self.notes = None
        self.times = times
        self.notes_visible = notes_visible

    def load_notes(self, file_path):
        with open(file_path, 'r') as f:
            self.notes = f.readlines()
        self.notes = [note.split() for note in self.notes]
        return self

    def play(self):
        for notes in self.notes:
            for note in notes:
                note = (note[1:] + note[0]).replace('+', 'h').replace('-', 'l')
                if len(note) == 1:
                    note = 'm' + note
                self.sounds[note].play()
                if self.notes_visible:
                    print(self.pitchs[int(note[-1])], end=' ')
                time.sleep(self.times / 1000)
            if self.notes_visible:
                print()
