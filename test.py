import os
dirt = os.path.expanduser("./_posts")
data = []
i = 0
for f in os.listdir(dirt):
    if os.path.isfile(os.path.join(dirt, f)):
        i = i + 1
        data.insert(i,f)
import json 

print(json.dumps(data,separators=( ',' , ':'))) 
