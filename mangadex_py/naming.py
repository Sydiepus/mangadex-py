def rename_main(naming, digits, curly_count, special=None) :
    if len(digits) <= curly_count :
        return rename(naming, digits, special)
    else :
        index = naming.find("{}")
        diff = len(digits) - curly_count
        new_naming = naming[:index] + "{}" * diff + naming[index:]
        return rename(new_naming, digits, special)

def rename(naming, digits, special=None) :
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

def naming_main(volumes, i, zip_name=None) :
    if zip_name == None :
        if volumes != [] and len(i) == 3:
            contain_vol = True
            chapter = f"vol-{i[1]}-chapter-{i[0]}"
            return chapter, contain_vol
        else :
            chapter = f"chapter-{i[0]}"
            contain_vol = False
            return chapter, contain_vol
    else :
        contain_vol = False
        return custom_naming_main(i[0], zip_name), contain_vol