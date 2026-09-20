# a
def part_a():
    comprehenesion = [(a,b,c,d)
        for a in range(1,11)
        for b in range(1,11)
        for c in range(1,11)
        for d in range(1,11)
        if a**2 + b**2 == c**2 + d**2 and len({a,b,c,d}) == 4]

    print(comprehenesion)

def part_b():
    strings = ['One', 'SEVEN', 'three', 'two', 'Ten']

    comprehension = [
        (word.lower(), len(word))
        for word in strings
        if len(word) < 5]

    print(comprehension)

def part_c():
    names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']

    comprehension = [
        name.split()[0] + " " + name.split()[1][0] + ". " + name.split()[2]
        for name in names ]
    print (comprehension)

def part_d():
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

    comprehension = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2if sorted(w1.lower()) == sorted(w2.lower())
    ]
    print(comprehension)

def part_e():
    s = ['one', 'two', 'three']

    comprehension = {
        word: len(word)
        for word in s
    }
    print(comprehension)

def part_f():
    text = "Hello World"

    comprehension = {
        i: c 
        for i, c in enumerate(text)
        if c.lower() in "aeiou"
    }
    print(comprehension)