#packages necessary for the script:
#!pip install python-docx
#!pip install spacy
#!python -m spacy download en_core_web_sm

import os
import re
from docx import Document

slist = [[] for _ in range(11)]

directory = '/content/resumes'
files = os.listdir(directory)

#curren time CHANGE IT TO FIT CURRENT TIME
curd = 2024*12+7

# Date pattern to match various date formats

year_pattern = re.compile(r'19[7-9]\d|20[0-2]\d')
digit_m_pattern = re.compile(r'\d{1,2}')
current_pattern = re.compile(r'current|present|now',re.IGNORECASE)


# One year and one month eg. Jan 2022-Apr 2023
date_pattern_ym = re.compile(r"""
    (
        (?:
            (?:
              (?:January|February|March|April|May|June|July|August|September|October|November|December)   # Full month names
            | (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                     # Abbreviated month names
            | (?: \b\d{2}\b)
            | (?: \b\d{1}\b))                                                                           # Numeric months
            \s*[ ,\-/\.]+\s*                                                                            # Separators
            (?:19[7-9]\d|20[0-2]\d|2025)                                                                  # Year
        )
    )
    |                                                                                               # OR
    (
        (?:
            (?:19[7-9]\d|20[0-2]\d|2025)                                                                  # Year
            \s*[ ,\-/\.]+\s*                                                                            # Separators
            (?:
              (?:January|February|March|April|May|June|July|August|September|October|November|December)  # Full month names
            | (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                   # Abbreviated month names
            | (?: \b\d{2}\b)
            | (?: \b\d{1}\b))                                                                           # Numeric months
        )
    )
    """, re.IGNORECASE|re.VERBOSE)

# One year and two months eg. Jan-Aug 2023
date_pattern_ymm = re.compile(r"""
    (
        # Match the format Month-Month-Year
        (?:
            (?:January|February|March|April|May|June|July|August|September|October|November|December)   # Full month names
            |(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                   # Abbreviated month names
        )
        [ ,\-/\.]+\s*[–\-—]?\s*                                                                         # Optional separators: en dash, hyphen, em dash with optional spaces
        (?:
            (?:January|February|March|April|May|June|July|August|September|October|November|December)   # Full month names
            |(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                   # Abbreviated month names
        )
        [ ,\-/\.]+\s*
        (?:19[7-9]\d|20[0-2]\d|2025)                                                                    # Year
    )
    |
    # Match the format Year-Month-Month
    (
        (?:19[7-9]\d|20[0-2]\d|2025)                                                                    # Year
        [ ,\-/\.]+\s*
        (?:
            (?:January|February|March|April|May|June|July|August|September|October|November|December)   # Full month names
            |(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                   # Abbreviated month names
        )
        [ ,\-/\.]+\s*[–\-—]?\s*                                                                         # Optional separators: en dash, hyphen, em dash with optional spaces
        (?:
            (?:January|February|March|April|May|June|July|August|September|October|November|December)   # Full month names
            |(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)                                   # Abbreviated month names
        )
    )
  """, re.IGNORECASE | re.VERBOSE)

# Two years format eg. 2019-2020
date_pattern_y = re.compile(r'((?:19[7-9]\d|20[0-2]\d)\s*[ -–—]?\s*(?:19[7-9]\d|20[0-2]\d))')

#NOTE: neglected the case where there are only one year (eg. Tech Developer 2018) because it is too easy to cause error


months_to_num = {
    "january": 1, "jan": 1, "jan.": 1,
    "february": 2, "feb": 2, "feb.": 2,
    "march": 3, "mar": 3, "mar.": 3,
    "april": 4, "apr": 4, "apr.": 4,
    "may": 5,
    "june": 6, "jun": 6, "jun.": 6,
    "july": 7, "jul": 7, "jul.": 7,
    "august": 8, "aug": 8, "aug.": 8,
    "september": 9, "sep": 9, "sept": 9, "sep.": 9, "sept.": 9,
    "october": 10, "oct": 10, "oct.": 10,
    "november": 11, "nov": 11, "nov.": 11,
    "december": 12, "dec": 12, "dec.": 12
}

# Function to extract text from a DOCX file
def get_text_from_docx(file_path):
    document = Document(file_path)
    doc_text = [paragraph.text for paragraph in document.paragraphs]
    return doc_text

# Calculate work time for ym format
def calc_ym(parsed_list,curs):
  wt = 0
  adpresent = False
  if (len(parsed_list) % 4 == 2):
    if current_pattern.search(curs):
        wt += curd
    else:
        adpresent = True
        wt += 1

  for i in range(len(parsed_list)):
      if(adpresent and i>=(len(parsed_list)-2)):
        break
      if i % 4 == 0 or i % 4 == 1:
          if year_pattern.search(parsed_list[i]):
              wt -= int(parsed_list[i]) * 12
          elif digit_m_pattern.search(parsed_list[i]):
              wt -= int(parsed_list[i])
          else:
              wt -= months_to_num[parsed_list[i].lower()]
      else:
          if year_pattern.search(parsed_list[i]):
              wt += int(parsed_list[i]) * 12
          elif digit_m_pattern.search(parsed_list[i]):
              wt += int(parsed_list[i])
          else:
              wt += months_to_num[parsed_list[i].lower()]
  if(wt>0 and wt<1000):
    return wt
  else:
    return 0

# Calculate work time for yym format
def calc_ymm(parsed_list):
  wt = 0
  cf = True

  for i in range(len(parsed_list)):
    if parsed_list[i].lower() in months_to_num:
      if(cf):
        wt-= months_to_num[parsed_list[i].lower()]
      else:
        wt+= months_to_num[parsed_list[i].lower()]
      cf = not cf
  if(wt>0 and wt<1000):
    return wt
  else:
    return 0

# Calculate work time for y format
def calc_y(parsed_list):
  wt = 0
  for i in range(len(parsed_list)):
    if(i%2==0):
      wt-=12*((int)(parsed_list[i])-1)
    else:
      wt+=12*((int)(parsed_list[i]))

  #eliminate obviously impossible responses
  if(wt>0 and wt<1000):
    return wt
  else:
    return 0





# Process each file in the directory

cnt = 0
for filename in files:


    #work_time with unit as month
    work_time = 0
    #work_time_bu = 0

    print(filename)
    file_path = os.path.join(directory, filename)
    parts = get_text_from_docx(file_path)
    sentences = []

    for part in parts:
        sentences.extend(part.split('\n'))

    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    for sentence in sentences:

      #in case of exception, skip
      try:
        ymm_date_instances = []
        date_instances = []

        #ymm format
        matches = date_pattern_ymm.findall(sentence)
        if matches:
          #print(matches)
          for match in matches:
              if(match[0]):
                  date = match[0]
              else:
                  date = match[1]
              ymm_date_instances.append(str(date))


        if(ymm_date_instances):
          parsed_list = []
          for element in ymm_date_instances:
            temp = (re.split(r'[ .\-–—]+', element))
            for splitedele in temp:
              if(splitedele!='' and splitedele!=r'[ .-–—]'):
                parsed_list.append(splitedele)

          if(parsed_list):
            work_time += calc_ymm(parsed_list)



        sentence = date_pattern_ymm.sub('', sentence)

        #ym format
        matches = date_pattern_ym.findall(sentence)
        if matches:
            #print(matches)
            for match in matches:
                if(match[0]):
                  date = match[0]
                else:
                  date = match[1]
                date_instances.append(str(date))

        if(date_instances):
          parsed_list = []
          for element in date_instances:
            temp = (re.split(r'[ .\-–—]+', element))
            for splitedele in temp:
              if(splitedele!=r'[ .\-–—]' and splitedele!=''):
                parsed_list.append(splitedele)


          if(parsed_list):
            work_time += calc_ym(parsed_list,sentence)


        sentence = date_pattern_ym.sub('', sentence)

        #y format
        matches = date_pattern_y.findall(sentence)
        if matches:
          #print(matches)
          parsed_list = []
          for element in matches:
            temp = (re.split(r'[ .\-–—&]+', element))
            for splitedele in temp:
              if(splitedele!=r'[ .\-–—&]' and splitedele!=''):
                parsed_list.append(splitedele)

          work_time+=calc_y(parsed_list)
      except:
        print("Error occured")



    #Print necessary info
    print("Processed:" + " " + filename)
    print('work time:' + ' ' + str(work_time))
    print('\n')


