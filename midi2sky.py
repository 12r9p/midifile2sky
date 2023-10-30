#  -- MIDIを使ってskyで楽器演奏 --

#MIDIキーボードからの入力から適切をキーを出力する｡
#キー出力はパソコン版skyに準拠｡
#動作確認をしたMIDIキーボードは88鍵のみ
#キーボード側では真ん中のドから2オクターブまでを変換｡
#真ん中のドから1オクターブ下のドより下を押すとプログラムが終了｡
#pyautoguiの改造推奨

import pygame
import pygame.midi
import pyautogui
import time

def main():
    while True:
        print("----------------------------------------")
        mode=str(input("動作モードを入力してください\n...k = keyboard mode\n...f = file mode\n......"))
        print("----------------------------------------")
        if mode == "k":
            print("キーボードからの入力で再生します")
            break
        elif mode == "f":
            print("midiファイルを読み込んで再生します")
            break
        else:
            print("正しく入力してください")
    if mode == "k":
        keyboard_midi()
    elif mode == "f":
        file_midi()
    print("\n")

def keyboard_midi():
    try:
        pygame.midi.init()
        midi_in = pygame.midi.Input(pygame.midi.get_default_input_id())   #MIDI機器を設定する
        print("接続完了")
    except:
        print("デバイスを接続してください｡ はじめからやり直してください｡")
        time.sleep(5)
        main()
    while True:
        if midi_in.poll():
            midi_read=midi_in.read(1)
            if midi_read[0][0][1] in midi_scale_list:
                push_key(midi_read)                
            elif midi_read[0][0][1] <= 48:   #真ん中のドから下を押すと終了
                midi_in.close()
                pygame.midi.quit()
                print("終了します")
                break
            else:
                continue

def file_midi():
    print("準備中です｡キーボードモードを使ってください｡")

def push_key(midi):
    midi_status,midi_scale,midi_volume = midi[0][0][0],midi[0][0][1],midi[0][0][2]   #音量でキーが押されたかを判断してキー入力をする
    if midi_volume > 0 and midi_status == 144:
        pyautogui.keyDown(key_list[midi_scale_list.index(midi_scale)])
    elif midi_volume == 0:
        pyautogui.keyUp(key_list[midi_scale_list.index(midi_scale)])

midi_scale_list = (60,62,64,65,67,69,71,72,74,76,77,79,81,83,84)
key_list = ("y","u","i","o","p","h","j","k","l",":","n","m",",",".","/")  #skyの楽器キー配列

if __name__ == "__main__":
    main()
