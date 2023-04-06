from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, VideoSendMessage
)
import os
import random

import dropbox

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "ロムちゃ～ん":
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        res = dbx.files_list_folder('/Pictures', recursive=True)
        arr_picpath = []
        for i in res.entries:
            if i.path_display.endswith("jpg") or i.path_display.endswith("mov"):
                arr_picpath.append(i.path_display)

        selected_path = random.choice(arr_picpath)

        setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
        try:
            link = dbx.sharing_list_shared_links(path=selected_path, direct_only=True).links[0]
        except:
            link = dbx.sharing_create_shared_link_with_settings(path=selected_path, settings=setting)

        url = link.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('?dl=0', '')

        arr_romu_voice = [
            "ぶにゃんっ",
            "ふにゃん～～",
            "きゅるんっ",
            "ロムにゃんかわいいニャン！",
            "この世で一番可愛いニャン",
            "世界平和はロム様により成り立つニャン",
            "100歳まで生きるニャン",
            "おねむだにゃーん",
            "ねっちのお膝が好きだニャン",
            "ちゅーるは毎日くださいニャン",
            "スーパーロム様タイムだにゃん！",
            "一富士二鷹三ロムにゃん！",
            "お兄ポンが拾ってくれたんだにゃん",
            "リカちゃんはこわいニャン",
            "かつお節はまだかニャン",
            "いつもごきげんだにゃん",
            "お風呂はきらいだにゃん",
            "ごろごろにゃ～ん",
            "ロムちゃん参上だにゃん！"
        ]

        if selected_path.split(".")[1] == "jpg":
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=random.choice(arr_romu_voice)),
                    ImageSendMessage(
                        original_content_url=url,
                        preview_image_url=url
                    )
                ]
            )
        elif selected_path.split(".")[1] == "mov":
            preview_jpg_path = f"/thumbnails/{selected_path.split('/')[2].replace('mov', 'jpg')}"
            try:
                preview_link = dbx.sharing_list_shared_links(path=preview_jpg_path, direct_only=True).links[0]
            except:
                preview_link = dbx.sharing_create_shared_link_with_settings(path=preview_jpg_path, settings=setting)

            preview_url = preview_link.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('?dl=0', '')

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(
                        text=f"\uDBC0\uDC39大当たりだにゃん！\uDBC0\uDC39\nかわいさあふれるロム様ムービーで癒やされるにゃんっ\uDBC0\uDC5F"
                    ),
                    VideoSendMessage(
                        original_content_url=url,
                        preview_image_url=preview_url
                    )
                ]
            )

    # elif event.message.text == "1":
    #     dbx = dropbox.Dropbox(ACCESS_TOKEN)
    #     res = dbx.files_list_folder('/Pictures', recursive=True)
    #     arr_picpath = []
    #     for i in res.entries:
    #         if i.path_display.endswith("mov"):
    #             arr_picpath.append(i.path_display)
    #
    #     selected_path = random.choice(arr_picpath)
    #
    #     setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
    #     try:
    #         link = dbx.sharing_list_shared_links(path=selected_path, direct_only=True).links[0]
    #     except:
    #         link = dbx.sharing_create_shared_link_with_settings(path=selected_path, settings=setting)
    #
    #     url = link.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('?dl=0', '')
    #
    #     arr_romu_voice = [
    #         "ぶにゃんっ",
    #         "ふにゃん～～",
    #         "きゅるんっ",
    #         "ロムにゃんかわいいニャン！",
    #         "この世で一番可愛いニャン",
    #         "世界平和はロム様により成り立つニャン",
    #         "100歳まで生きるニャン",
    #         "おねむだにゃーん",
    #         "ねっちのお膝が好きだニャン",
    #         "ちゅーるは毎日くださいニャン",
    #         "スーパーロム様タイムだにゃん！",
    #         "一富士二鷹三ロムにゃん！",
    #         "お兄ポンが拾ってくれたんだにゃん",
    #         "リカちゃんはこわいニャン",
    #         "かつお節はまだかニャン",
    #         "いつもごきげんだにゃん",
    #         "お風呂はきらいだにゃん",
    #         "ごろごろにゃ～ん",
    #         "ロムちゃん参上だにゃん！"
    #     ]
    #     preview_jpg_path = f"/thumbnails/{selected_path.split('/')[2].replace('mov', 'jpg')}"
    #     try:
    #         preview_link = dbx.sharing_list_shared_links(path=preview_jpg_path, direct_only=True).links[0]
    #     except:
    #         preview_link = dbx.sharing_create_shared_link_with_settings(path=preview_jpg_path, settings=setting)
    #
    #     preview_url = preview_link.url.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('?dl=0', '')
    #
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         [
    #             TextSendMessage(text=random.choice(arr_romu_voice)),
    #             VideoSendMessage(
    #                 original_content_url=url,
    #                 preview_image_url=preview_url
    #             )
    #         ]
    #     )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="何言ってるかわからないにゃ～((≡ﾟ♀ﾟ≡))")]
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)