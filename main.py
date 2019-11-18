# -*- coding: utf-8 -*-

import asyncio

import pyttsx3
import translate

import blivedm.blivedm as blivedm


class BLiveTts(blivedm.BLiveClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 翻译
        self._translator = translate.Translator(from_lang='zh', to_lang='ja')
        # TTS
        self._tts = None

    def start(self):
        self._loop.run_in_executor(None, self._tts_loop)
        return super().start()

    def _tts_loop(self):
        self._tts = pyttsx3.init()
        # voice = self._tts.getProperty('voice')
        # print('cur voice', voice)
        # voices = self._tts.getProperty('voices')
        # for voice in voices:
        #     print(voice)
        self._tts.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0')
        self._tts.startLoop()

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        self._say(danmaku.msg)

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        self._say(message.message)

    def _say(self, text):
        self._loop.create_task(self._do_say(text))

    async def _do_say(self, text):
        # TODO 常用的加缓存？
        translated_text = await self._loop.run_in_executor(None, self._translator.translate, text)
        print(f'{text} - {translated_text}')
        # TODO 加入队列
        self._tts.say(translated_text)


async def main():
    client = BLiveTts(213)
    await client.start()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
