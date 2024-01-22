import pandas as pd
import timeit

import speech_recognition as sr
import msvcrt

from difflib import SequenceMatcher

SIMILARITY = 0.80
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def get_voice_input(voice_handler:sr.Recognizer, dev=False,target_line=None):
    assert type(voice_handler)==sr.Recognizer, "voice_handler should be speech_recognition.Recognizer"
    # Flush input buffer for windows
    while msvcrt.kbhit():
        msvcrt.getch()
    flag = input('Enter을 누르면 녹음을 시작합니다.')

    print('시작하세요.')
    with sr.Microphone() as source:
        audio = voice_handler.listen(source)
    print('녹음 종료.')

    try:
        start = timeit.default_timer()
        input_line = voice_handler.recognize_whisper(audio, language="korean")
        print(input_line)
        stop = timeit.default_timer()
        if dev == True:
            print(f"{stop-start}s")
        input_line = input_line.replace(' ', '').replace(',','').replace('.','')
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")

    return input_line

    



def get_console_input():
    pass


def run_dev(voice_handler:sr.Recognizer, target_line:str):
    input_line = get_voice_input(voice_handler, dev=True, target_line=target_line)
    print(f'{similar(input_line, target_line)*100//1}점이네용^^')
    print('target :', target_line)

    wrong_count = 0

    while similar(input_line, target_line) < SIMILARITY:
        wrong_count += 1
        print(f'땡! {wrong_count}번 틀리셨어요... ')
        print()

        input_line = get_voice_input(voice_handler, dev=True, target_line=target_line)
        print(f'{similar(input_line, target_line)*100//1}점이네용^^')

        print('input :', input_line, '/ target :', target_line)
    print('dev:)')


def run_mode_0(target_line:str, target_character:str):
    input_line = input(f'{target_character} : ').replace(' ', '').replace(',','')
    wrong_count = 0
    while input_line != target_line:
        wrong_count += 1
        print(f'땡! {wrong_count}번 틀리셨어요... ')
        print()
        # Get line input
        input_line = input(f'{target_character} : ').replace(' ', '').replace(',','')



def run_mode_1(voice_handler:sr.Recognizer, target_line:str):             
    input_line = get_voice_input(voice_handler)
    print(f'{similar(input_line, target_line)*100//1}점이네용^^')

    wrong_count = 0
    while similar(input_line, target_line) < SIMILARITY:
        wrong_count += 1
        print(f'땡! {wrong_count}번 틀리셨어요... ')
        print()

        input_line = get_voice_input(voice_handler) 
        print(f'{similar(input_line, target_line)*100//1}점이네용^^')  



def main():
    voice_handler = None

    # Select normal / voice mode
    mode = input('일반모드(0) \t | \t 음성모드(1) : ')
    print()


    # Load livewhisper on voice mode
    if mode == '1':
        print('음성 인식 모듈을 로딩 중이에요.')
        voice_handler = sr.Recognizer()
        print('음성 인식 모듈 준비 완료\n')
    elif mode == 'dev':
        print('Enter DEV mode.')
        print('음성 인식 모듈을 로딩 중이에요.')
        voice_handler = sr.Recognizer()
        print(type(voice_handler))
        print('음성 인식 모듈 준비 완료\n')
    
    if mode == '1' or 'dev':
        global SIMILARITY
        SIMILARITY = int(input('통과 점수를 입력해주세요. (0~100 사이의 정수): '))/100

    # Load play script
    start = timeit.default_timer()
    print('대본을 불러오고 있어요.')

    df = pd.read_csv('./script/script_csv.csv', encoding='utf8')

    stop = timeit.default_timer()
    print(f'대본을 불러왔어요.\n걸린시간 : {stop-start}s')
    print()


    # Load chapters
    df_grouped = df.groupby('chapter')

    # Select chapter to practice
    print('막:', df['chapter'].unique())
    target_chapter = input("(n)막 연습하기 : ")
    print()
    target_chapter_lines = df_grouped.get_group(target_chapter)


    # Load characters
    characters = target_chapter_lines['character'].unique()
    character_select_text = '' 
    for i in range(len(characters)):
        character_select_text += f'{i+1}. {characters[i]} '
    
    # Select character
    target_character_index = input("(캐릭터) 연습하기\n숫자로 입력해주세요.\n" + character_select_text + '\n')
    print()
    target_character = characters[int(target_character_index)-1]


    # Run through lines
    for _, row in target_chapter_lines.iterrows():
        
        # If not target character
        if row['character'] != target_character:
            input_line = input(f'{row["character"]} : {row["line"]}')

        # If target character
        else:
            target_line = row['line'].replace(' ', '').replace(',','')
            if mode == '1' or 'dev':
                target_line = target_line.replace('.','')



            if mode == 'dev':
                run_dev(voice_handler, target_line)
                continue

            elif mode =='0':
                run_mode_0(target_line, target_character)
            
            elif mode == '1':
                run_mode_1(voice_handler, target_line)

            print(':)')
            


if __name__ == "__main__":
    main()
