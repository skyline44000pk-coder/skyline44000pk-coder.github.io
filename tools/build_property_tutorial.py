#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import subprocess, wave, numpy as np, cv2, os
W,H,FPS=1280,720,12
OUT="skyline-free-property-ad-tutorial.mp4"
AUDIO="/tmp/skyline_voice.wav"
TEXT=("Want to list your property for free on SKYLINE? Follow these simple steps. "
"First, open the SKYLINE website and choose Post Free Ad. "
"Next, enter a clear property title and select whether you want to sell or rent. "
"Then choose your property type, city, area, and property size. "
"Add your asking price and a helpful description so people understand your listing. "
"Now upload up to ten clear property photos. "
"Finally, submit your ad and check your listing on SKYLINE. "
"That’s it. Share your property with more people, and list for free on SKYLINE.")
subprocess.run(["espeak","-v","en-us+f3","-s","145","-p","48","-a","175","-w",AUDIO,TEXT],check=True)
with wave.open(AUDIO,"rb") as f: duration=f.getnframes()/f.getframerate()
regular=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",25)
small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
bold=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)
large=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",54)
navy=(8,24,39); gold=(210,177,112); white=(248,249,250); muted=(183,197,210)
starts=[0,5.1,9.5,14.5,19.1,23.5,26.5]
caps=["Want to list your property for free on SKYLINE?","First, open the SKYLINE website and choose Post Free Ad.","Enter a clear property title and select sale or rent.","Choose your property type, city, area, and property size.","Add your asking price and a helpful description.","Upload up to ten clear property photos.","Submit your ad and check your listing on SKYLINE.","List your property for free on SKYLINE."]
steps=[("01","OPEN SKYLINE","Visit the website and tap","POST FREE AD"),("02","CHOOSE YOUR LISTING","Add a clear property title","Select SALE or RENT"),("03","ADD PROPERTY DETAILS","Choose type, city, area","and property size"),("04","SET PRICE & DESCRIPTION","Enter your asking price","and useful details"),("05","UPLOAD PHOTOS","Add up to 10 clear","property photos"),("06","SUBMIT YOUR AD","Submit the form and","check your listing")]
def wrap(d,s,font,width):
    out=[]; cur=""
    for w in s.split():
        t=(cur+" "+w).strip()
        if d.textbbox((0,0),t,font=font)[2]<=width: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def render(t):
    im=Image.new("RGB",(W,H),navy); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,10),fill=gold); d.text((64,40),"SKYLINE",font=bold,fill=white)
    d.text((64,82),"PROPERTY MARKETPLACE  ·  PAKISTAN",font=small,fill=gold)
    d.line((64,122,1216,122),fill=(47,67,83),width=2)
    idx=sum(1 for x in starts if x<=t)-1; idx=max(0,min(idx,7))
    if idx in (0,7):
        d.text((64,190),"YOUR PROPERTY.",font=large,fill=white); d.text((64,260),"YOUR NEXT MOVE.",font=large,fill=gold)
        d.text((68,350),"A simple, free way to publish a property ad.",font=regular,fill=muted)
        d.rounded_rectangle((760,185,1160,520),radius=22,fill=(245,244,239))
        d.rectangle((780,205,1140,380),fill=(207,216,220))
        d.polygon([(850,315),(950,240),(1050,315)],fill=(183,147,89))
        d.rectangle((875,315,1025,365),fill=(249,247,240)); d.rectangle((930,330,970,365),fill=navy)
        d.text((790,405),"LIST FOR FREE",font=bold,fill=navy); d.text((790,450),"SKYLINE",font=small,fill=(104,112,118))
    else:
        num,title,line1,line2=steps[idx-1]
        d.rounded_rectangle((64,165,160,261),radius=22,fill=gold); d.text((84,192),num,font=large,fill=navy)
        d.text((190,174),title,font=bold,fill=white); d.text((190,226),line1,font=regular,fill=muted); d.text((190,267),line2,font=regular,fill=muted)
        d.rounded_rectangle((650,165,1160,545),radius=18,fill=(245,246,246)); d.rounded_rectangle((650,165,1160,215),radius=18,fill=(228,231,232))
        for j,c in enumerate([(206,114,98),(218,181,102),(108,164,130)]): d.ellipse((674+j*22,183,686+j*22,195),fill=c)
        d.text((760,179),"skyline  /  post free ad",font=small,fill=navy)
        if idx==1:
            d.text((690,245),"Create your free property ad",font=bold,fill=navy); d.rounded_rectangle((690,300,1120,355),radius=8,fill="white",outline=(199,205,207),width=2); d.text((710,316),"Post Free Ad",font=regular,fill=(110,119,126)); d.rounded_rectangle((690,390,880,445),radius=8,fill=gold); d.text((715,405),"START LISTING",font=small,fill=navy)
        elif idx==2:
            d.text((690,245),"Property title",font=small,fill=(85,96,105)); d.rounded_rectangle((690,275,1120,330),radius=8,fill="white",outline=(199,205,207),width=2); d.text((710,291),"5 Marla House for Sale",font=regular,fill=navy); d.text((690,365),"Purpose",font=small,fill=(85,96,105)); d.rounded_rectangle((690,395,890,455),radius=8,fill=gold); d.text((725,412),"FOR SALE  ✓",font=small,fill=navy); d.rounded_rectangle((910,395,1120,455),radius=8,fill="white",outline=(199,205,207),width=2); d.text((950,412),"FOR RENT",font=small,fill=navy)
        elif idx==3:
            for j,(a,b) in enumerate([("Property type","House"),("City","Islamabad"),("Area / Society","G-13"),("Property size","5 Marla")]):
                x=690+(j%2)*220; y=245+(j//2)*125; d.text((x,y),a,font=small,fill=(85,96,105)); d.rounded_rectangle((x,y+30,x+195,y+82),radius=7,fill="white",outline=(199,205,207),width=2); d.text((x+12,y+44),b,font=regular,fill=navy)
        elif idx==4:
            d.text((690,245),"Asking price (PKR)",font=small,fill=(85,96,105)); d.rounded_rectangle((690,275,1120,330),radius=8,fill="white",outline=(199,205,207),width=2); d.text((710,291),"12,500,000",font=regular,fill=navy); d.text((690,365),"Description",font=small,fill=(85,96,105)); d.rounded_rectangle((690,395,1120,490),radius=8,fill="white",outline=(199,205,207),width=2); d.text((710,412),"Bright, well-maintained property...",font=small,fill=navy)
        elif idx==5:
            d.text((690,245),"Property photos",font=bold,fill=navy)
            for j in range(4):
                x=690+(j%2)*210; y=295+(j//2)*105; d.rounded_rectangle((x,y,x+185,y+85),radius=8,fill=(220,226,226),outline=(195,202,204)); d.rectangle((x+15,y+44,x+170,y+72),fill=(164,184,174)); d.polygon([(x+20,y+48),(x+72,y+10),(x+125,y+48)],fill=(192,164,116))
            d.text((690,510),"UP TO 10 PHOTOS",font=small,fill=(135,101,50))
        else:
            d.text((690,255),"Review your property ad",font=bold,fill=navy); d.rounded_rectangle((690,310,1120,385),radius=10,fill="white",outline=(199,205,207),width=2); d.text((715,325),"5 Marla House for Sale",font=regular,fill=navy); d.text((715,355),"Islamabad  ·  G-13  ·  12.5M PKR",font=small,fill=(95,105,112)); d.rounded_rectangle((690,420,1120,485),radius=10,fill=gold); d.text((835,438),"SUBMIT FREE AD  ✓",font=small,fill=navy)
    d.rounded_rectangle((64,590,1216,676),radius=16,fill=(17,42,63),outline=(71,91,106),width=1)
    lines=wrap(d,caps[idx],regular,1080); y=610 if len(lines)==1 else 600
    for line in lines[:2]: d.text((88,y),line,font=regular,fill=white); y+=32
    d.rounded_rectangle((64,700,1216,708),radius=4,fill=(35,55,71)); d.rounded_rectangle((64,700,64+int(1152*min(1,t/duration)),708),radius=4,fill=gold)
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
silent="/tmp/skyline_silent.mp4"; w=cv2.VideoWriter(silent,cv2.VideoWriter_fourcc(*"mp4v"),FPS,(W,H))
for t in np.arange(0,duration,1/FPS): w.write(render(float(t)))
w.release()
subprocess.run(["ffmpeg","-y","-i",silent,"-i",AUDIO,"-c:v","libx264","-preset","medium","-crf","22","-c:a","aac","-b:a","128k","-shortest","-pix_fmt","yuv420p",OUT],check=True)
