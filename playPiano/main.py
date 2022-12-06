# -*- coding : utf-8 -*-
"""
@author: Github-Afool4U
@Description: Python弹奏钢琴曲
@Date: 2022-12-5 14:40

"""

from playPiano import PlayPiano, Notes, StopThreads

if __name__ == '__main__':
    playlist = Notes().load_notes(r'resources\notes')
    stop_threads = StopThreads()
    while True:
        print('请选择您想弹奏的琴谱：')
        for idx, (title, song) in enumerate(playlist.items()):
            notes, accompaniments, times = song['notes'], song['accompaniments'], song['times']
            print('{:3}. {}'.format(idx + 1, title.ljust(28, '-')), end='' if (idx + 1) % 3 else '\n')
        print('\n请输入要弹奏的歌曲：', end='')
        if stop_threads.is_alive():
            stop_threads.join()
            choice = stop_threads.choice
        else:
            choice = input()
        try:
            choice = int(choice)
            if not (1 <= choice <= len(playlist)):
                raise Exception
        except Exception:
            print('请重新输入！')
            continue
        title, song = list(playlist.items())[choice - 1]
        notes, accompaniments, times = song['notes'], song['accompaniments'], song['times']
        print('正在弹奏{}...'.format(title))
        play_notes = PlayPiano(times=times, notes_visible=True).load_notes(notes)
        play_accompaniments = PlayPiano(times=times).load_notes(accompaniments)
        play_notes.start()
        play_accompaniments.start()
        if not stop_threads.is_alive():
            stop_threads = StopThreads()
        stop_threads.threads = [play_notes, play_accompaniments]
        stop_threads.start()
        play_notes.join()
        play_accompaniments.join()
        print('播放完毕！')
