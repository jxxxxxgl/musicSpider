# -*- coding: UTF-8 -*-
'''
@Project ：musicSpider 
@Author  ：L--favork
@Date    ：2024/1/14 13:52
@Desc    : 
@Version ：V1.0
'''
import time
from argparse import ArgumentParser

import requests
import json
import execjs
import os
from pydub import AudioSegment
from termcolor import colored


def QQmusic_spider(query):
    if not os.path.exists("QQ音乐"):
        os.makedirs("QQ音乐")

    with open('222.js', encoding='utf-8') as f1:
        js_code = f1.read()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://y.qq.com",
        "Connection": "keep-alive",
        "Referer": "https://y.qq.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }
    cookies = {
        "需要自己的Cookie"
    }
    url = "https://u.y.qq.com/cgi-bin/musics.fcg"
    params = {
        "_": "1705206484344",
    }

    
    searchid = execjs.compile(js_code).call('search')

    query_data = "需要自己的搜索表单信息 --> 将要搜索的 由 query 替换" 
    
    query_data = json.dumps(query_data, separators=(',', ':'), ensure_ascii=False)
    sign = execjs.compile(js_code).call('get_sign', query_data)
    params['sign'] = sign

    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=query_data.encode("utf-8"))

    response_text = response.text
    response_text = json.loads(response_text)

    song_list = response_text["req_1"]["data"]["body"]["song"]["list"]

    print("\t------歌曲名称------歌曲链接------歌手------歌曲公布时间------下载状态")
    for song in song_list:

        play_data = {
            "common":"需要自己的common信息",
            "req_1": {
                "module": "vkey.GetVkeyServer",
                "method": "CgiGetVkey",
                "param": {
                    "guid": "323158658",
                    "songmid": [
                        song["mid"]

                    ],
                    "songtype": [
                        0
                    ],
                    "uin": "自己的qq号",
                    "loginflag": 1,
                    "platform": "20"
                }
            },
            "req_2": {
                "module": "music.musicasset.SongFavRead",
                "method": "IsSongFanByMid",
                "param": {
                    "v_songMid": [
                        song["mid"],
                    ]
                }
            },
            "req_3": {
                "module": "music.musichallSong.PlayLyricInfo",
                "method": "GetPlayLyricInfo",
                "param": {
                    "songMID": song["mid"],
                    "songID": song["id"]
                }
            },
            "req_4": {
                "method": "GetCommentCount",
                "module": "music.globalComment.GlobalCommentRead",
                "param": {
                    "request_list": [
                        {
                            "biz_type": 1,
                            "biz_id": "449205",
                            "biz_sub_type": 0
                        }
                    ]
                }
            },
            "req_5": {
                "module": "music.musichallAlbum.AlbumInfoServer",
                "method": "GetAlbumDetail",
                "param": {
                    "albumMid": "002Neh8l0uciQZ"
                }
            },
            "req_6": {
                "module": "vkey.GetVkeyServer",
                "method": "CgiGetVkey",
                "param": {
                    "guid": "805555582",
                    "songmid": [
                        song["mid"]
                    ],
                    "songtype": [
                        0
                    ],
                    "uin": "自己的qq号",
                    "loginflag": 1,
                    "platform": "20"
                }
            },
            "req_7": {
                "module": "music.trackInfo.UniformRuleCtrl",
                "method": "CgiGetTrackInfo",
                "param": {
                    "ids": [
                        song["id"]
                    ],
                    "types": [
                        0
                    ]
                }
            }
        }
        play_data = json.dumps(play_data, separators=(',', ':'), ensure_ascii=False)
        sign = execjs.compile(js_code).call('get_sign', play_data)
        params['sign'] = sign
        response = requests.post(url, headers=headers, cookies=cookies, params=params, data=play_data.encode("utf-8"))
        time.sleep(10)
        response_text = response.text
        response_text = json.loads(response_text)

        testfile2g = response_text["req_6"]["data"]["midurlinfo"][0]["purl"]

        song_url = "https://dl.stream.qqmusic.qq.com/" + testfile2g

        # 下载文件
        input_file = "QQ音乐/" + song["title"] + ".m4a"
        output_file = "QQ音乐/" + song["title"] + ".mp3"
        song_data = requests.get(song_url).content
        with open(input_file, 'wb') as f:
            f.write(song_data)
        AudioSegment.from_file(input_file,format="m4a").export(output_file,format="mp3")
        if os.path.exists(output_file):
            os.remove(input_file)
        print("\t正在下载", song["title"], ".........")
        print("\t------", song["title"], "------", song_url, "------", song["singer"][0]["name"], "------",
              song["time_public"], "------", "下载成功")


def get_m4a_files(directory):
    """
    获取指定文件夹中所有后缀为m4a的文件

    Args:
      directory: 要遍历的文件夹的路径

    Returns:
      一个包含所有m4a文件路径的列表
    """

    # 获取文件夹中所有文件
    files = os.listdir(directory)

    # 过滤出后缀为m4a的文件
    m4a_files = []
    for file in files:
        if file.endswith(".m4a"):
            m4a_files.append(os.path.join(directory, file))

    return m4a_files


def m4a_to_mp3(input_file):
    output_file = input_file.replace(".m4a", ".mp3")
    if not os.path.isfile(input_file):
        raise FileNotFoundError("Input file not found: {}".format(input_file))

    if os.path.isfile(output_file):
        raise FileExistsError("Output file already exists: {}".format(output_file))
    command = "ffmpeg -i {} -acodec libmp3lame -ac 2 -ab 192k {}".format(input_file, output_file)
    os.system(command)


if __name__ == '__main__':
    name_data = 'QQ音乐'
    arg = ArgumentParser(description=colored(name_data, 'cyan'))
    arg.add_argument("-q", "--query", help="输入歌名或者歌手")
    args = arg.parse_args()
    query = args.query
    QQmusic_spider(query)

