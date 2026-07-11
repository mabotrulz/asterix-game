#!/usr/bin/env python3
"""Download Asterix character PNGs for the game"""
import subprocess, json, os

dest = '/home/hermes/asterix-game/assets'
os.makedirs(dest, exist_ok=True)

files = {
    'obelix': 'Obelix-img.png',
    'asterix': 'Asterix%2A.png',
    'roman': 'Roman_Soldier.png',
    'boar': 'Wild_boar.gif',
    'getafix': 'Getafix_-_Master_of_the_Magic_Potion.jpg',
    'dogmatix': 'Dogmatix.jpg',
}

for name, fname in files.items():
    api_url = f'https://asterix.fandom.com/api.php?action=query&titles=File:{fname}&prop=imageinfo&iiprop=url&format=json'
    r = subprocess.run(['curl', '-s', api_url, '-A', 'Mozilla/5.0'], capture_output=True, text=True, timeout=10)
    try:
        d = json.loads(r.stdout)
    except:
        print(f'{name}: JSON parse error')
        continue
    img_url = None
    for p in d.get('query',{}).get('pages',{}).values():
        for ii in p.get('imageinfo',[]):
            img_url = ii.get('url')
    
    if not img_url:
        print(f'{name}: no URL')
        continue
    
    ext = os.path.splitext(fname)[1].lower().replace('%2A','').replace('*','')
    if ext in ('.jpg','.gif'): ext = '.png'  # save as png for consistency
    outpath = os.path.join(dest, f'{name}.png')
    subprocess.run(['curl', '-sL', img_url, '-o', outpath, '-A', 'Mozilla/5.0', '-H', 'Referer: https://asterix.fandom.com/'], timeout=20)
    size = os.path.getsize(outpath)
    print(f'{name}: {outpath} ({size/1024:.0f}KB)')
PYEOF