# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 13:26:39 2021
@author: Mh
"""
import ffmpeg


inputAddress = './log_dvbs2.ts'

streamList=ffmpeg.probe(inputAddress)['streams']

inputdData = ffmpeg.input(inputAddress)
videoCh_list=[]

for stream in streamList:
   if('codec_name' in stream):
     if(stream['codec_name']=='h264'):
         id_video=stream['id']
         index_audio=list(filter(lambda n: n['id']==str(hex(int(id_video, 16)+1)), streamList))[0]['index']
         videoCh_list.append((stream['index'],index_audio))
         
for item in videoCh_list:
         
      streamVideo = inputdData[str(streamList[item[0]]['index'])]
      streamAudio = inputdData[str(streamList[item[1]]['index'])]
      outfile = ffmpeg.output(streamVideo,streamAudio, str(streamList[item[0]]['index'])+'.mp4')
      outfile = ffmpeg.overwrite_output(outfile)
      try:
          ffmpeg.run(outfile)
          print(str(streamList[item[0]]['index'])+' success!')
      except:
          print(str(streamList[item[0]]['index'])+' failed!')
        
