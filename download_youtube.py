import csv
import os

from moviepy import editor
from pytube import YouTube

#csvから情報をゲットして保存
csv_file = './data/test.csv'
save_dir = './videos'
errored_txt = './not-succeed.txt'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
with open(errored_txt, 'w'):
    pass

with open(csv_file) as f:
    print("now loading CSV file")
    info = csv.reader(f)
    for i, r in enumerate(info, start=1):
        short_url = r[0]
        start = float(r[1])
        end = float(r[2])
        url = 'https://www.youtube.com/watch?v='+short_url

        try:
            yt = YouTube(url)
            # yt = YouTube(url, proxies={"https":"https://~:XXXX"}) # for proxy environment

            stream = yt.streams.first()
            stream.download(save_dir)

            filename = stream.default_filename
            file_path = os.path.join(save_dir, filename)
            base, ext = os.path.splitext(filename)

            video = editor.VideoFileClip(file_path)
            duration = video.duration
            if end > duration:
                diff = end - duration
                end = duration
                start = max(start - diff, 0)

            video = video.subclip(start, end)        
            
            try:
                video.write_videofile(
                    filename=os.path.join(save_dir, str(i)+'_'+base+'_cut.mp4'),
                    codec='libx264', 
                    audio_codec='aac') 
                os.remove(file_path)
            except:
                with open(errored_txt, mode='a') as f:
                    f.write(str(i)+'_not-edited_'+url+'\n')

                print(filename, 'cannnot be editted!')

        except:
            with open(errored_txt, mode='a') as f:
                    f.write(str(i)+'_not-download_'+url+'\n')

            print(i, ":", url, 'cannnot be downloaded!')

print('finish')