def rename_main(naming, digits, curly_count, special) :
    if len(digits) <= curly_count :
        return rename(naming, digits, special)
    else :
        index = naming.find("{}")
        diff = len(digits) - curly_count
        new_naming = naming[:index] + "{}" * diff + naming[index:]
        return rename(new_naming, digits, special)

def rename(naming, digits, special) :
    b = naming
    if special == None :
        for i in range(0, len(digits) + 1) :
            try :
                b = rreplace(b, "{}", digits[i], 1)
            except IndexError :
                c = b.replace("{}", "0")
                return c
    else :
        for i in range(0, len(digits) + 1) :
            try :
                b = rreplace(b, "{}", digits[i], 1)
            except IndexError :
                c = b.replace("{}", "0")
                return c + f"-{special}"


def rreplace(string, old, new, occurrence) :
    li = string.rsplit(old, occurrence)
    return new.join(li)

def custom_naming_main(chapter_number, naming) :
    chapter = chapter_number.split(".") #check for special
    a = naming.count("{}")
    digits = []
    for i in chapter :
        for p in i :
            digits.append(p)
        digits = digits[::-1]
        if len(chapter) > 1 :
            special = chapter[-1]
            return rename_main(naming, digits, a, special)
        else :
            return rename_main(naming, digits, a)

def naming_main(vol, chap, zip_name) :
    if zip_name == None :
        if vol != None :
            chapter = f"vol-{vol}-chapter-{chap}"
            return chapter
        else :
            chapter = f"chapter-{chap}"
            return chapter
    else :
        return custom_naming_main(chap, zip_name), 