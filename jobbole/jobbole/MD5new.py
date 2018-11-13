import hashlib

def md5_JM(url):
    if isinstance(url,str):
        url=url.encode("utf-8")
        m=hashlib.md5()
        m.update(url)
        md5_jm=m.hexdigest()
        return md5_jm


#d5_JM("http://blog.jobbole.com/all-posts/",)