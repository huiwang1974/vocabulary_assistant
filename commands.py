command_translations = {
    # Chinese
    "chinese": "chinese",
    "chinois": "chinese",  
    "chino": "chinese",  
    "chinesisch": "chinese",  
    "中文": "chinese",  
    "중국어": "chinese",  
    "中国語": "chinese",  

    # Korean
    "korean": "korean",
    "coréen": "korean",  
    "coreano": "korean",  
    "koreanisch": "korean",  
    "韩语": "korean",  
    "조선어": "korean",  
    "朝鮮語": "korean",  

    # Japanese
    "japanese": "japanese",
    "japonais": "japanese",  
    "japonés": "japanese",  
    "japanisch": "japanese",  
    "日语": "japanese",
    "일본어": "japanese",  
    "日本語": "japanese",  

    # English
    "english": "english",
    "anglais": "english",  
    "inglés": "english",  
    "englisch": "english",  
    "英语": "english",  
    "영어": "english",  
    "英語": "english",  

    # German
    "german": "german",
    "allemand": "german",  
    "alemán": "german",  
    "deutsch": "german",  
    "德语": "german",  
    "독일어": "german",  
    "ドイツ語": "german",  

    # French
    "french": "french",
    "français": "french",  
    "francés": "french",  
    "französisch": "french",  
    "法语": "french",  
    "프랑스어": "french",  
    "フランス語": "french",  

    # Spanish
    "spanish": "spanish",
    "espagnol": "spanish",  
    "español": "spanish",  
    "spanisch": "spanish",  
    "西班牙语": "spanish",  
    "스페인어": "spanish",  
    "スペイン語": "spanish",  

    # Read
    "read": "read",
    "lire": "read",  
    "leer": "read",  
    "lesen": "read",  
    "朗读": "read",  
    "읽다": "read",  
    "読む": "read",  

    # Be quiet
    "quiet": "quiet",
    "silence": "quiet",  
    "silencio": "quiet",  
    "sei ruhig": "quiet",  
    "安静": "quiet",  
    "조용히 해": "quiet",  
    "静かにして": "quiet",  

    # Store
    "store": "store",
    "sauvegarder": "store",  
    "guardar": "store",  
    "speichern": "store",  
    "保存": "store",  
    "저장": "store",  
    "保存する": "store",

    # Search
    "search": "search",
    "consultation": "search",
    "Suche": "search",
    "consulta": "search",
    "查找": "search",
    "검색": "search",
    "検索": "search",
}

def command_in_english(cmd):
    if cmd in command_translations:
        return command_translations[cmd]
    return None
