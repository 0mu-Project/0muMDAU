### Reimu(0mu) MarkDown Automatic Uploading Control Panel


簡稱: 0mu MDAU-panel

簡單說 他是一個靜態化 MD blog（EX. jekyll） 的 **動態式分散式後台**

現在很紅的靜態化部落格有個缺點 他 沒 有 後台 , 所以常常需要這堆指令

```
vim _post/xxx.md 
```
```
git add _post/xxx.md
```
```
git co -a
```
```
git pull
```

有點麻煩吧... 因此 我們想出要製作一個可以視覺化管理的後台

就有了這個東西產生了

本後台採用了 bootstrap markdown 當作預設的編輯器 （[link](https://github.com/toopay/bootstrap-markdown)）

技術 上面 使用了 bootstrap 以及 html5 跟 jQuery 建構前端

後端採用 python 2.7 的web.py進行 fastCGI 的開發

如果您需要自己架設的話 請 使用 nginx 以及 安裝 python 2.7
