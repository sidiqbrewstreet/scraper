import requests, re, os, json, sys, traceback
from datetime import datetime
from bing_image_downloader import downloader
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs

dictor = ['Results/video-YT','Results/video-TT']
try:
    for x in dictor: os.mkdir(x)
except Exception as e:pass
try: os.mkdir('Dumps')
except Exception as e:pass

id = []
ok, loop = 0, 0

quality = {'1080p': '137', '720p' : '136'}

def clear(): os.system('cls' if 'win' in sys.platform.lower() else 'clear')

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
headersYT = lambda i=ua : {'Host': 'www.youtube.com','User-Agent': i,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'id,en-US;q=0.7,en;q=0.3','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Connection': 'close',}

###----------[ Menu ]------------###
def menu():
    try:
        print('==========================================')
        print('[1] Get Foto By BING AI')
        print('[2] Download Video Tiktok')
        print('[3] Download Video YouTube')
        print('[4] Dumps Video Tiktok')
        print('[5] Dumps Videp YouTube')
        print('==========================================')
        opsi = int(input('[+] Pilih : '))
        print('==========================================')
        if   opsi == 1: generate_foto()
        elif opsi == 2 or opsi == 3:
            print('[1] Link To Files')
            print('[2] Link Manual')
            print('==========================================')
            info = int(input('[+] Pilih : '));print('')
            if   info == 1:
                url = input(r'Alamat Directory : ')
                print('')
                convert(1,url)
            elif info == 2:
                url = input('Gunakan Koma (,) Jika Lebih Dari 1 : ').split(',')
                print('==========================================')
                convert(2,url)
            else: exit('Input Tidak Valid')
        elif opsi == 4: dumpsIDTT()
        elif opsi == 5: dumpsIDYT()
        else: exit('Input Tidak Valid')
    except ValueError: exit('Input Harus Angka')
    except KeyboardInterrupt: exit('')

def generate_foto():
    key = input("Kata Kunci  : ").lower()
    jumlah = int(input("Jumlah Foto : "))
    print('==========================================')
    downloader.download(key, limit=jumlah, output_dir='Results', adult_filter_off=True, force_replace=False, timeout=60)

def cvsubs(url):
    ses  = requests.Session()
    res1 = ses.get(url).text.replace('\\','')
    id   = re.search(r'"@id": "(.*?)"',str(res1)).group(1)
    try:
        if 'http' in str(id):
            res  = ses.get(id).text.replace('\\','')
            ids  = re.search(r'"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.*?)"', str(res)).group(1)
        else: pass
    except AttributeError: ids = '-'
    return(ids)

def cekangka(x):
    try:
        if   int(x) >= 1000000:    depan, belakang = x[:1], x[1];y = depan + ',' + belakang + ' Jt'
        elif int(x) >= 1000000000: depan, belakang = x[:1], x[1];y = depan + ',' + belakang + ' M'
        else: y = x[:3] + ' rb'
        return(str(y))
    except ValueError: return('-')
    except Exception: return('-')

def scrape_YTvideo(url) -> str:
    global judul
    res     = requests.Session().get(url).text
    judul   = re.search(r'name="twitter:title" content="(.*?)"', str(res)).group(1)
    chl     = re.search(r'link itemprop="name" content="(.*?)"', str(res)).group(1)
    subs    = re.search(r'"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.*?)"', str(res)).group(1)
    like    = re.search(r'"iconName":"LIKE","title":"(.*?)",', str(res)).group(1)
    output  = int(re.search(r'"viewCount":"(\d+)"',  str(res)).group(1))
    terbi   = re.search(r'"uploadDate":"(.*?)"', str(res)).group(1)
    videoid = re.search(r'"videoId":"(.*?)"', str(res)).group(1)
    tanggal = datetime.strptime(terbi, "%Y-%m-%dT%H:%M:%S%z").strftime("%d-%m-%Y")
    if   output >= 1000000: views = str(round(output / 1000000, 1)) + " Jt"
    elif output >= 1000000000: views = str(round(output / 1000000000, 1)) + " M"
    else: views = str(output)[:3] + " rb"
    print('')
    print('Judul     : ',judul)
    print('Channel   : ',chl)
    print('Subscribe : ',subs)
    print('Like      : ',like + ' Like')
    print('Views     : ',views)
    print('Upload    : ',tanggal)
    print('')
    return videoid

def scrape_YTshort(url) -> str:
    global judul
    res     = requests.Session().get(url).text.replace('\\','')
    judul   = re.search(r'name="twitter:title" content="(.*?)"', str(res)).group(1)
    chl     = re.search(r'link itemprop="name" content="(.*?)"', str(res)).group(1)
    subs    = cvsubs(url)
    lkcount = str(re.search(r'"likeCountWithLikeText":{"accessibility":{"accessibilityData":{"label":"(.*?)"}', str(res)).group(1).replace(".", "").split()[0])
    output  = str(re.search(r'"viewCount":"(\d+)"',  str(res)).group(1))
    terbit  = re.search(r'"uploadDate":"(.*?)"', str(res)).group(1)
    tanggal = datetime.strptime(terbit, "%Y-%m-%dT%H:%M:%S%z").strftime("%d-%m-%Y")
    like    = cekangka(lkcount)
    views   = cekangka(output)
    print('')
    print('Judul     : ',judul)
    print('Channel   : ',chl)
    print('Subscribe : ',subs)
    print('Like      : ',like)
    print('Views     : ',views)
    print('Upload    : ',tanggal)
    print('')
    return judul

def download_Tt(url):
    global ids, chl
    headers = {'authority': 'www.tiktok.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',}
    res     = bs(requests.Session().get(url, headers=headers).content, 'html.parser')
    element = json.loads(res.find(id='__UNIVERSAL_DATA_FOR_REHYDRATION__').contents[0])
    info  = element["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    ids   = info["id"]
    tag   = info["desc"]
    chl   = info["author"]["nickname"]
    msc   = info["music"]
    stat  = info["stats"]
    snd   = msc["title"]
    sndby = msc["authorName"]
    like  = stat["diggCount"]
    komen = stat["commentCount"]
    share = stat["shareCount"]
    print('')
    print("Username : ",chl)
    print("Like     : ",like)
    print("Komen    : ",komen)
    print("Share    : ",share)
    print("sound By : ",snd,'-',sndby)
    print("Caption  : ",tag)
    print('')

def GetID(r, url, headers) -> str:
    try:
        params = {'retry': 'undefined','platform': 'youtube',}
        data   = {'url' : '{}'.format(url),'ajax': '1','lang': 'en'}
        response = requests.post('https://yt1d.com/mates/en/analyze/ajax', params=params, headers=headers, data=data, allow_redirects=True).text.replace('\\','')
        ID = re.search(r'data-id="(.*?)"', str(response)).group(1)
        return ID
    except AttributeError: GetID(r, url, headers)

def GetURL(r, link, judul:str, pixel:str, idx:str):
    headers = {'Host': 'yt1d.com','Sec-Ch-Ua-Platform': '"Windows"','Sec-Ch-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"','Sec-Ch-Ua-Mobile': '?0','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36','Accept': 'application/json, text/javascript, */*; q=0.01','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','X-Note': '1080p','Origin': 'https://yt1d.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://yt1d.com/','Accept-Encoding': 'gzip, deflate','Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','Priority': 'u=1, i'}
    ID = str(GetID(r, link, headers))
    data = {
        'platform': 'youtube',
        'url'     : '{}'.format(link),
        'title'   : '{}'.format(judul),
        'id'      : '{}'.format(ID),
        'ext'     : 'mp4',
        'note'    : '{}'.format(pixel),
        'format'  : '{}'.format(idx),
    }
    try:
        response = r.post('https://yt1d.com/mates/en/convert?id={}'.format(ID), headers=headers, data=data, allow_redirects=True).json()
        if 'success' in str(response):
            urlx = response['downloadUrlX']
            return urlx
        elif 'downloaderror' in str(response):
            return ('downloaderror')
        else: return False
    except requests.exceptions.JSONDecodeError: return False
    except Exception: return False
        
def Download_YT(url, dir, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req   = Request(url, headers=headers)
    link  = urlopen(req).read()
    files = f'{dir}/{filename}'
    with open(f'{files}.mp4', 'wb') as r:
        r.write(link)
    r.close()

def convert(i,url):
    ok = 0
    ex = 0
    try:
        if i == 1:
            try: pathfile = open(url, 'r').read().splitlines()
            except FileNotFoundError: exit('File Tidak Ditemukan')
            print(f"Jumlah Video = {len(pathfile)} Video")
            print('==========================================')
            for x in pathfile:
                r = requests.Session()
                try:
                    if 'www.youtube.com' in x or 'youtu.be' in x:
                        if   'watch'  in x: judul = scrape_YTvideo(x)
                        elif 'shorts' in x: judul = scrape_YTshort(x)
                        print('==========================================')
                        print('[*] Start Downloading... ')
                        try:
                            pet = 'Results/video-YT'
                            os.makedirs(pet, exist_ok=True)
                            check = GetURL(r, x, str(judul), '1080p', quality['1080p'])
                            if   'genyoutube.online' in str(check): Download_YT(check, pet, judul)
                            elif 'downloaderror' in str(check):
                                check = GetURL(r, x, str(judul), '720p', quality['720p'])
                                Download_YT(check, pet, judul)
                            else:
                                print(f'[*] Gagal Mengunduh... ');print('')
                                print('==========================================')
                                ex +=1
                        except Exception as e:
                            print(f'[*] Gagal Mengunduh... {str(e)}');print('')
                            print('==========================================')
                            ex +=1
                        print('[*] Success Downloading... ');print('');ok +=1
                        print('==========================================')
                    elif 'www.tiktok.com' in x or 'vt.tiktok.com' in x:
                        download_Tt(x)
                        print('==========================================')
                        print('[*] Start Downloading... ')
                        if 'video' in x: link = urlopen(f"https://tikcdn.io/ssstik/{ids}").read()
                        else:
                            headers = {'authority': 'www.tiktok.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',}
                            response = requests.Session().get(x, headers=headers).text
                            info = re.search(r'"seo.abtest":{"canonical":"(.*?)"',str(response)).group(1)
                            if   'video' in info: link = urlopen(f"https://tikcdn.io/ssstik/{ids}").read()
                            elif 'photo' in info: link = urlopen(f"https://r8.ssstik.top/ssstik/{ids}").read()
                        pet = 'Results/video-TT'
                        os.makedirs(pet, exist_ok=True)
                        with open(f'{pet}/{ids}.mp4', 'wb') as r:
                            r.write(link)
                        r.close()
                        print('[*] Success Downloading... ');print('');ok +=1
                        print('==========================================')
                    else: exit('[#404] Domain URL Tidak Valid')
                except KeyboardInterrupt: exit()
                except requests.exceptions.ConnectionError: exit('[x] Koneksi Anda Bermasalah')
                except Exception as e:
                    traceback.print_exc()
                    exit(f'[x] Terjadi Kesalahan {e}')

            print(f'[*] Berhasil Mengunduh =-{ok} Video')
            print(f'[*] Gagal Mengunduh =-{ex} Video\n')
            print(f"[+] File Tersimpan Di Folder: {pet}")
            print('')

        elif i == 2:
            for x in url:
                try:
                    if 'www.youtube.com' in x or 'youtu.be' in x:
                        if   'watch'  in x: scrape_YTvideo(x)
                        elif 'shorts' in x: scrape_YTshort(x)
                        print('==========================================')
                        print('[*] Start Downloading... ')
                        try:
                            pet = 'Results/video-YT'
                            os.makedirs(pet, exist_ok=True)
                            check = GetURL(r, x, str(judul), '1080p', quality['1080p'])
                            if   'genyoutube.online' in str(check): Download_YT(check, pet, judul)
                            elif 'downloaderror' in str(check):
                                check = GetURL(r, x, str(judul), '720p', quality['720p'])
                                Download_YT(check, pet, judul)
                            else:
                                print(f'[*] Gagal Mengunduh... ');print('')
                                print('==========================================')
                                ex +=1
                                continue
                        except Exception as e:
                            print(f'[*] Gagal Mengunduh... {str(e)}');print('')
                            print('==========================================')
                            ex +=1
                            continue
                        print('[*] Success Downloading... ');print('');ok +=1
                        print('==========================================')
                    elif 'www.tiktok.com' in x or 'vt.tiktok.com' in x:
                        download_Tt(x)
                        print('==========================================')
                        print('[*] Start Downloading... ')
                        if 'video' in x: link = urlopen(f"https://tikcdn.io/ssstik/{ids}").read()
                        else:
                            headers = {'authority': 'www.tiktok.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',}
                            response = requests.Session().get(x, headers=headers).text
                            info = re.search(r'"seo.abtest":{"canonical":"(.*?)"',str(response)).group(1)
                            if   'video' in str(info): link = urlopen(f"https://tikcdn.io/ssstik/{ids}").read()
                            elif 'photo' in str(info): link = urlopen(f"https://r8.ssstik.top/ssstik/{ids}").read()
                        pet = 'Results/video-tT'
                        os.makedirs(pet, exist_ok=True)
                        with open(f'{pet}/{ids}.mp4', 'wb') as r:
                            r.write(link)
                        r.close()
                        print('[*] Success Downloading... ');print('');ok +=1
                        print('==========================================')
                    else: exit('[#404] Domain URL Tidak Valid')
                except FileNotFoundError: exit('File Tidak Ditemukan')
                except KeyboardInterrupt: exit()
                except Exception as e:exit(f'[x] Terjadi Kesalahan {e}')
            print(f'[*] Berhasil Mengunduh =-{ok} Video')
            print(f'[*] Gagal Mengunduh =-{ex} Video\n')
            print(f"[+] File Tersimpan Di Folder: {pet}")
            print('')
    except Exception as e:exit(f'[x] Terjadi Kesalahan {e}');print('')

def dumpsIDTT():
    try:
        ok = 0
        user = input('Username Tanpa "@" : ')
        link = input('URL : ')
        i    = input('UserAgent : ')
        HeaderTT = {'Host': 'www.tiktok.com','User-Agent': i,'Accept': '*/*','Accept-Language': 'id,en-US;q=0.7,en;q=0.3','Accept-Encoding': 'gzip, deflate','Referer': 'https://www.tiktok.com/','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin',}
        print('');print('Tekan "CTRL + C" Untuk Berhenti/Skip');print('')
        if 'https://www.tiktok.com/api/post/item_list/?WebIdLastTime' in str(link) or 'count' in str(link):
            response = requests.Session().get(link, headers=HeaderTT, allow_redirects=True)
            a = set(re.findall('"id":"(\d+)"',str(response.text)))
            for x in a:
                with requests.Session() as ses:
                    if len(x) == 19:
                        res = ses.get(f'https://www.tiktok.com/@{user}/video/{x}', headers=HeaderTT, allow_redirects=True).text
                        if "item doesn't exist" in str(res): pass
                        else:
                            ok +=1
                            open(f'Dumps/{user}.txt', 'a').write(f'https://www.tiktok.com/@{user}/video/{x}\n')
                            print(f'\rDump {ok} ID  ',end='')
                    else: continue
            print(f'\rBehasil Dump {ok} ID  ',end='');exit('')
        else: exit('Format Link Tidak Valid')
    except requests.exceptions.ConnectionError: exit('Koneksi Bermasalah')
    except KeyboardInterrupt: exit()
    except requests.JSONDecodeError: exit('Terjadi Kesalahan Pastikan Link Benar')
    except Exception: exit('Terjadi Kesalahan Pastikan Semua Sesuai')

def checkuser(r, params:dict):
    global loop
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8','Accept-Language': 'id,en-US;q=0.7,en;q=0.3','Accept-Encoding': 'gzip, deflate','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Connection': 'keep-alive',}
    response = r.get('https://www.youtube.com/results', params=params, headers=headers).text
    channel  = set(re.findall(r'"webCommandMetadata":{"url":"/@(.*?)"', str(response)))
    query    = '"searchEndpoint":{"query":"%s","params":"(.*?)"'%params['search_query']
    paramx   = re.search(query, str(response)).group(1)
    if params['search_query'] in channel: return True
    elif not channel: return False
    else:
        loop +=1
        if loop == 2: return False
        else:
            dat = params.copy()
            dat.update({'sp': paramx})
            user = checkuser(r, dat)
            if user: return True
            else: return False

def dumpsIDYT():
    global ok, id
    print('Gunakan Koma (,) Jika Lebih Dari 1 ')
    linkz = input('Masukan Username : @').split(',')
    r = requests.Session()
    for i in linkz:
        params = {'search_query': f'{i}'}
        user   = checkuser(r, params)
        if user:
            try:
                response = r.get(f'https://www.youtube.com/@{i}/videos', headers=headersYT(), allow_redirects=True).text
                video_id = set(re.findall(r'"videoId":"(.*?)"',str(response)))
                Data_YT  = re.findall(r'"text":{"content":"(.*?)"',str(response))
                params   = re.search(r'"continuationEndpoint":{"clickTrackingParams":"(.*?)"', str(response)).group(1)
                token    = re.search(r'"continuationCommand":{"token":"(.*?)"'     ,str(response)).group(1)
                print('')
                print( 'Channel      :', Data_YT[0])
                print( 'Username     :', Data_YT[1])
                print( 'Subscribe    :', Data_YT[2])
                print( 'Jumlah Video :', Data_YT[3])
                print('')
                for x in set(video_id):
                    if x in id: pass
                    else:
                        ok +=1
                        id.append(x)
                        print(f'\rDumps {ok} ID ',end='')
                        with open(r'Dumps/{}.txt'.format(Data_YT[0]), 'a+') as w:
                            w.write(f'https://www.youtube.com/watch?v={x}\n')
                        w.close()
                
                loopDump(r,Data_YT[0],params,token)
            except AttributeError as e: exit(f'[X] Terjadi Kesalahan {e}')
        else:
            print('')
            exit('[X] Username Tidak ditemukan')

def loopDump(r,user,clickparams,token):
    global ok
    try:
        data = {
            'context': {
                'client': {
                    'hl': 'id',
                    'gl': 'ID',
                    'remoteHost': '',
                    'deviceMake': '',
                    'deviceModel': '',
                    'visitorData': '',
                    'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20240210.05.00',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'originalUrl': f'https://www.youtube.com/{user}/videos',
                    'screenPixelDensity': 2,
                    'platform': 'DESKTOP',
                    'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                    'configInfo': {},
                    'screenDensityFloat': 1.5,
                    'userInterfaceTheme': 'USER_INTERFACE_THEME_DARK',
                    'timeZone': 'Asia/Bangkok',
                    'browserName': 'Firefox',
                    'browserVersion': '122.0',
                    'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'screenWidthPoints': 643,
                    'screenHeightPoints': 581,
                    'utcOffsetMinutes': 420,
                    'mainAppWebInfo': {
                        'graftUrl': f'https://www.youtube.com/{user}/videos',
                        'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_UNKNOWN',
                        'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                        'isWebNativeShareAvailable': False}},
                'user': {'lockedSafetyMode': False},
                'request': {
                    'useSsl': True,
                    'internalExperimentFlags': [],
                    'consistencyTokenJars': []},
                'clickTracking': {'clickTrackingParams': clickparams},
                'adSignalsInfo': {'params': []}},
            'continuation': token}

        response = r.post('https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false', headers=headersYT(), json=data).text
        video_id = set(re.findall(r'"videoId":"(.*?)"',str(response)))
        params   = re.search(r'"continuationEndpoint":{"clickTrackingParams":"(.*?)"',str(response)).group(1)
        tokenz   = re.search(r'"continuationCommand":{"token":"(.*?)"',str(response)).group(1)
        for x in set(video_id):
            if x in id: pass
            else:
                ok +=1
                id.append(x)
                print(f'\rDumps {ok} ID ',end='')
                with open(f'Dumps/{user}.txt', 'a+') as w:
                    w.write(f'https://www.youtube.com/watch?v={x}\n')
                w.close()
        loopDump(r,user,params,tokenz)
    except AttributeError:
        print(f'\rBerhasil Dump {ok} ID\n')
        pass

if __name__ == '__main__':
    clear()
    menu()
