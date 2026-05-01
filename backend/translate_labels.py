import json
import urllib.request
import urllib.parse
import time
import os

def translate(text, target_lang):
    if not text: return ""
    # Simple free translation using google translate url hack
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return "".join([x[0] for x in data[0]])
    except Exception as e:
        print("Error translating:", text, e)
        return text

path = '../ml-model/models/class_labels.json'
with open(path, 'r') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"Translating {k}...")
    
    # If it's already a dict, skip
    if isinstance(v['name'], dict):
        continue
        
    orig_name = v['name']
    orig_desc = v['description']
    orig_treat = v['treatment']
    
    name_fr = translate(orig_name.replace("_", " "), "fr")
    name_de = translate(orig_name.replace("_", " "), "de")
    
    desc_fr = translate(orig_desc, "fr")
    desc_de = translate(orig_desc, "de")
    
    treat_fr = translate(orig_treat, "fr")
    treat_de = translate(orig_treat, "de")
    
    v['name'] = {'en': orig_name, 'fr': name_fr, 'de': name_de}
    v['description'] = {'en': orig_desc, 'fr': desc_fr, 'de': desc_de}
    v['treatment'] = {'en': orig_treat, 'fr': treat_fr, 'de': treat_de}
    time.sleep(0.5)

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Translation complete!")
