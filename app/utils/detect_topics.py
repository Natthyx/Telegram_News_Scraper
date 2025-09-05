

TOPIC_KEYWORDS = {
    "sports": ["football", "soccer", "basketball", "match", "tournament", "goal","እግር ኳስ", "ቡድን", "ትዕይንት", "ጨዋታ", "ጎል"],
    "politics": ["government", "election", "parliament", "minister", "policy", "president", "መንግስት", "ምርጫ", "ፓርላማ", "ጠቅላይ ሚኒስትር", "ፖሊሲ"],
    "business": ["market", "bank", "stock", "trade", "investment", "company", "ገበያ", "ባንክ", "ንግድ", "ኢንቨስትመንት", "ኩባንያ"],
    "health": ["hospital", "covid", "disease", "vaccine", "doctor", "ሆስፒታል", "ኮቪድ", "በሽታ", "ክትባት", "ሐኪም"],
    "technology": ["app", "AI", "tech", "software", "startup", "internet", "ቴክኖሎጂ", "አፕሊኬሽን", "ሶፍትዌር", "ኢንተርኔት", "አርቲፊሻል ኢንቴለጀንስ"],
    "university": ["ዩኒቨርሲቲ", "ኮሌጅ", "university", "college", "campus","school","bachelor","gat","nat","exit exam"]
}

def detect_topic(text: str) -> str:
    result = set()
    text_lower = text.lower()
    for topic, keyword in TOPIC_KEYWORDS.items():
        if topic == text_lower:
            result.add(topic)
    
    if result:
        return list(result)
    else:
        return ["general"]
            
   