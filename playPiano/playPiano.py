# -*- coding : utf-8 -*-
"""
@author: Github-Afool4U
@Description: playPiano.py
@Date: 2022-12-5 14:40

"""

import os
from os import environ
from collections import OrderedDict
import threading
import concurrent.futures

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time


class PlayPiano(threading.Thread):
    # 设置成类变量，保证所有实例共享同一个音频播放器
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.set_num_channels(1024)
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
        self.ended = 0

    def load_notes(self, notes):
        self.notes = notes
        return self

    def play(self):
        def play_note(note):
            if self.ended:
                return
            note = (note[1:] + note[0]).replace('+', 'h').replace('-', 'l')
            if len(note) == 1:
                note = 'm' + note
            self.sounds[note].play()
            if self.notes_visible:
                print(self.pitchs[int(note[-1])], end=' ')

        with concurrent.futures.ThreadPoolExecutor(max_workers=1024) as executor:
            for notes in self.notes:
                for note in notes:
                    executor.submit(play_note, note)
                    time.sleep(self.times / 1000)
                    if self.ended:
                        return
                if self.notes_visible:
                    print()
            self.ended = 1

    def stop(self):
        self.ended = 1

    def __bool__(self):
        return self.ended == 1


class Notes:
    def __init__(self):
        self.notes = OrderedDict()

    def load_note(self, file_path):
        file = os.path.basename(file_path)
        suffix = file.split('.')[1]
        title = file.split('_')[0]
        times = int(file[file.find('_') + 1:file.rfind('.')])
        with open(file_path, 'r') as f:
            notes = f.readlines()
        notes = [note.split('//')[0].split() for note in notes]
        if self.notes.get(title) is None:
            self.notes[title] = {}
        self.notes[title][suffix] = notes
        self.notes[title]['times'] = times

    def load_notes(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                self.load_note(os.path.join(root, file))
        return self.notes


class StopThreads(threading.Thread):
    def __init__(self):
        super().__init__(target=self.stop_threads)
        self.threads = None
        self.choice = None

    def stop_threads(self):
        line = input()
        if any(self.threads):
            self.choice = line
        else:
            for thread in self.threads:
                thread.stop()
