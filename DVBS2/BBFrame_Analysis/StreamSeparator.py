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
        
# The following command from is from llogan's answer to this question.  
# ffprobe -v error -show_entries program=program_id:program_tags=service_name -of xml input.ts

# Return a dictionary (The dictionary has 3 entries p['format'], p['programs'] and p['streams']).
p = ffmpeg.probe(inputAddress, show_entries='program=program_id:program_tags=service_name:streams=stream_id:stream_tags=stream_index')

programs = p['programs']  # Get p['programs']. programs is a list

# Iterate programs.
# program is a dictionary (entries are program['program_id'], program['streams'], program['tags'])
for program in programs:
    tags = program['tags']  # tags is a dictionary (has the entry tags['service_name']).
    service_name = tags['service_name']
    print('program_id ' + str(program['program_id']) + ' has Service Name: ' + service_name)
