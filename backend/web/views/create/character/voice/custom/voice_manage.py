from dotenv import load_dotenv
from web.views.create.character.voice.custom.list_voice import list_voice
from web.views.create.character.voice.custom.creat_voice import create_voice
from web.views.create.character.voice.custom.delete_voice import delete_voice

def creat_v():
    vs = [1,4]
    for v in vs:
        print(create_voice(f'https://app8072.acapp.acwing.com.cn/media/tmp/{v}.mp3',v))

def delete_v():
    res = list_voice()
    for v in res['output']['voice_list']:
        print(delete_voice(v['voice_id']))

if __name__ == '__main__':
    load_dotenv()
    print(list_voice())