import requests
import bs_headers
import os
from tqdm import tqdm

#https://www.jianshu.com/p/331aa20937ba?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

ENABLE_LOG = 1

def my_print(dat):
    if (ENABLE_LOG):
        print(dat)

def download_from_url(url, dsts):
    dst = dsts
    headers = bs_headers.get_headers(url)
    my_print(headers)
    response = requests.get(url, headers=headers, stream=True)
    file_size = int(response.headers['content-length'])
    my_print(file_size)

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    
    if first_byte >= file_size:
        return file_size
    

    headers['Range'] = f"bytes={first_byte}-{file_size}"
    pbar = tqdm(
        total = file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst
    )

    req = requests.get(url, headers=headers, stream=True)
    with open(dst, 'ab') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    
    pbar.close()
    return file_size



if __name__ == "__main__":
    url = 'https://www.gamersky.com/showimage/id_gamersky.shtml?https://img1.gamersky.com/upimg/users/2020/08/15/origin_202008150756594065.jpg'
    dst = 'aa.jpeg'
    download_from_url(url, dst)


