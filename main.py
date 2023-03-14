import os
from pathlib import Path
import glob
import shutil
import re
# url folder hash file
dir = 'D:/hash_ror/2023_03_14_update_data/data_raw'

# Regex
regex_phrases_explanation = '^Description_\d+_\d+\.mp3$'
regex_description = '^Description_\d+.mp3$'
regex_check = '^chk_day\d+.mp3$'
regex_phrases = '^\d+e*\.mp3$'
regex_practice = '^prc_day\d+.mp3$'

# Function create folder if is exists
def create_folder(folder, dir):
   if not os.path.exists('{dir}/hash/{folder}'.format(dir=dir, folder=folder)):
      os.makedirs('{dir}/hash/{folder}'.format(dir=dir, folder=folder))

# Function copy file to hash folder
def copy_file(type, regex, dir):
   # get all file format .mp3
   files = glob.glob('{dir}/**/*.mp3'.format(dir=dir), recursive=True)
   for file in files:
      filename = os.path.split(file)[1]
      print(filename)
      if(re.compile(regex).match(filename)):
         if(regex == regex_phrases_explanation):
            lesson = filename.split('_')[1]
            if not os.path.exists('{dir}/hash/{type}/Day{lesson}'.format(dir=dir, lesson=lesson, type=type)):
               os.makedirs('{dir}/hash/{type}/Day{lesson}'.format(dir=dir, lesson=lesson, type=type))
            shutil.copy(file.replace('\\', '/'), '{dir}/hash/{type}/Day{lesson}/{file_}'.format(dir=dir, lesson=lesson, type=type, file_=filename))
            print(filename)
         else:
            if not os.path.exists('{dir}/hash/{type}'.format(dir=dir, type=type)):
               os.makedirs('{dir}/hash/{type}'.format(dir=dir, type=type))
            shutil.copy(file.replace('\\', '/'), '{dir}/hash/{type}/{file}'.format(dir=dir, type=type, file=filename))
            print(filename)

# list 5 folder default
folders = [
   ['practice', regex_practice],
   ['check', regex_check],
   ['description', regex_description],
   ['phrases_explanation', regex_phrases_explanation],
   ['phrases', regex_phrases]
]

for folder in folders:
   create_folder(folder[0], dir)
   copy_file(folder[0], folder[1], dir)

# Rename file of 3 folders
# NOTE recursive=True : get all files contained in 3 parent directories
checks = glob.glob('{dir}/hash/check/*.mp3'.format(dir=dir), recursive=True)
phrases_explanations = glob.glob('{dir}/hash/phrases_explanation/Day*/*.mp3'.format(dir=dir), recursive=True)
practices = glob.glob('{dir}/hash/practice/*.mp3'.format(dir=dir), recursive=True)

for file in phrases_explanations:
   dirSrc, filename = os.path.split(file)
   f, lesson, no = filename.split('_')
   no, ext = no.split('.')
   fileNameOut = 'Day{lesson}-{no}.{ext}'.format(lesson=lesson,no=int(no), ext=ext)
   os.rename(file.replace('\\', '/'), '{dirSrc}/{file}'.format(dirSrc=dirSrc, file=fileNameOut).replace('\\', '/'))

for file in checks:
      dir, name = file.split('_day')
      dirSrc = dir.split('chk')[0]
      fileName = 'Check_{name}'.format(name=name)
      os.rename(file.replace('\\', '/'), '{dirSrc}{file}'.format(dirSrc=dirSrc, file=fileName).replace('\\', '/'))

for file in practices:
      dir, name = file.split('_day')
      dirSrc = dir.split('prc')[0]
      fileName = 'Practice_{name}'.format(name=name)
      os.rename(file.replace('\\', '/'), '{dirSrc}{file}'.format(dirSrc=dirSrc, file=fileName).replace('\\', '/'))
