# -*- coding : utf-8 -*-
"""
@author: Github-Afool4U
@Description: Python弹奏起风了
@Date: 2022-12-5 12:07

"""

from playPiano import PlayPiano

if __name__ == '__main__':
    PlayPiano(180, notes_visible=True).load_notes(r'resources\notes\起风了_180.notes').start()
    PlayPiano(180).load_notes(r'resources\notes\起风了_180.accompaniments').start()
