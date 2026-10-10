from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import subprocess, json, argparse

parser=argparse.ArgumentParser(description='Render the Taiga-themed startup video from locally supplied media.')
parser.add_argument('--image',type=Path,required=True,help='Character image supplied by the user')
parser.add_argument('--audio',type=Path,required=True,help='Audio supplied by the user')
parser.add_argument('--output',type=Path,default=Path('dist/TaigaBoot'))
args=parser.parse_args()
if not args.image.is_file() or not args.audio.is_file():
    parser.error('Both --image and --audio must be existing files.')
ROOT=Path(__file__).resolve().parents[1]
OUT=args.output.resolve()
(OUT/'media').mkdir(parents=True,exist_ok=True)
W,H,FPS=1280,720,30
def font(n,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('msyhbd.ttc' if bold else 'msyh.ttc'),n)
def ease(x):
    x=max(0,min(1,x));return 1-(1-x)**3
art=ImageOps.fit(Image.open(args.image).convert('RGB'),(790,720),centering=(.51,.27))
base=Image.new('RGB',(W,H),'#fff3e9')
d=ImageDraw.Draw(base)
for x in range(0,W,24):
    for y in range(0,H,24):d.ellipse((x,y,x+1,y+1),fill='#e7c5b7')
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(args.audio),'-filter_complex','[1:a]adelay=3200|3200,apad[a]','-map','0:v','-map','[a]','-t','10','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'media/startup.mp4')],stdin=subprocess.PIPE)
for i in range(300):
    t=i/FPS;im=base.copy();d=ImageDraw.Draw(im)
    shift=int(-760*(1-ease(t/.9)))
    for off,col in [(35,'#f4b99e'),(20,'#e58b70'),(0,'#4d3042')]:
        d.polygon([(shift-100,0),(shift+660+off,0),(shift+455+off,H),(shift-100,H)],fill=col)
    x=int(510+900*(1-ease((t-.55)/1.25)))
    im.paste(art,(x,0));d=ImageDraw.Draw(im)
    d.line((654,0,450,H),fill='#ffe6cf',width=4)
    def text(s,xy,n,color,at,bold=False):
        a=ease((t-at)/.8)
        if a<=0:return
        layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
        ld.text((xy[0],xy[1]+int(24*(1-a))),s,font=font(n,bold),fill=color)
        layer.putalpha(layer.getchannel('A').point(lambda p:int(p*a)))
        im.paste(layer,(0,0),layer)
    text('CHATGPT · CHARACTER STARTUP',(64,55),13,'#ffd4b7',1.8,True)
    text('ChatGPT',(61,107),82,'#ffffff',1.8,True)
    text('掌心猛虎登场！',(64,211),38,'#ffd5ae',1.9,True)
    text('灵感加载中 · 稍等一下啦',(68,274),18,'#ffdcce',2)
    text('TORADORA! / TAIGA AISAKA',(68,368),13,'#ffc9ac',2.6)
    text('逢坂大河',(65,398),44,'#ffffff',2.6,True)
    if t>=3.2:
        d=ImageDraw.Draw(im);p=min(1,(t-3.2)/4)
        d.rounded_rectangle((68,481,398,486),radius=2,fill='#816373')
        d.rounded_rectangle((68,481,68+max(3,int(330*p)),486),radius=2,fill='#ffe1ad')
        d.text((68,502),'READY · 一起开始吧',font=font(14),fill='#ffdac7')
        a=ease((t-3.2)/.8);by=int(523+40*(1-a))
        layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
        ld.rounded_rectangle((729,by+8,1210,by+122),radius=26,fill='#d5726c')
        ld.rounded_rectangle((721,by,1202,by+112),radius=26,fill='#fffdfa',outline='#573643',width=3)
        ld.text((744,by+13),'うるさいわね！',font=font(29,True),fill='#4c2b39')
        ld.text((744,by+57),'やらないと未来は変わらないのよ！',font=font(17),fill='#b36662')
        ld.text((744,by+83),'不行动的话，未来可不会改变！',font=font(15),fill='#b36662')
        layer.putalpha(layer.getchannel('A').point(lambda p:int(p*a)));im.paste(layer,(0,0),layer)
    if t>=4.3:
        d=ImageDraw.Draw(im);d.ellipse((85,568,188,671),outline='#f7c1a1',width=2)
        d.text((103,594),'WELCOME',font=font(12,True),fill='#f7c1a1');d.text((117,616),'BACK',font=font(12,True),fill='#f7c1a1')
    if t>=7.8:
        # Shared rectangle path with launcher.json; real app progressively covers this panel.
        u=ease((t-8)/1.6);x0=int(.1*W*(1-u));y0=int(.1*H*(1-u))
        d=ImageDraw.Draw(im);d.rectangle((x0,y0,W-x0,H-y0),fill='#f9f9f9',outline='#e58b70',width=2)
        if t<8.4:d.text((W//2-115,H//2-20),'正在连接 ChatGPT…',font=font(24),fill='#4d3042')
    if i in (105,210,239,270):im.save(OUT/f'preview-{i}.jpg',quality=94)
    proc.stdin.write(im.tobytes())
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError('Video encoding failed')
cfg=json.loads((ROOT/'config/launcher.example.json').read_text(encoding='utf-8-sig'))
cfg.update(AutoReplaceEntrypoints=False,ScanAllLocalDrives=False,HoldAt=7.65,TransitionStart=8.0,TransitionEnd=9.6,PlayerWidth=1280,PlayerHeight=720,DisplayName='ChatGPT · 逢坂大河')
cfg['ScreenFrames']=[dict(Time=8,X=.1,Y=.1,Width=.8,Height=.8),dict(Time=9.6,X=0,Y=0,Width=1,Height=1)]
(OUT/'launcher.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8-sig')
print(str(OUT/'media/startup.mp4'))
