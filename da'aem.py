from bs4 import BeautifulSoup
import re

file = open('1_1684314644/67b91e09-83e7-404d-92fe-98a36cb96ec5.html')
test = open('test.txt', 'a')
daaem_al_islam = BeautifulSoup(file.read(), 'html.parser')
ids = []
for i in range(3076, 3098): ids.append(i)


def is_digit(x):
    return '1' in x \
           or '2' in x \
           or "3" in x \
           or '4' in x \
           or '5' in x \
           or '6' in x \
           or '7' in x \
           or '8' in x \
           or '9' in x \
           or '0' in x


class GetData:
    def __init__(self, hadith_id):
        self.book = daaem_al_islam
        self.hadith_id = hadith_id
        self.maasoom = GetData.get_maasoom(self)
        self.sanad = GetData.get_sanad(self)
        self.text = GetData.get_texts(self)
        self.footnote = GetData.get_footnote(self)
        self.bookinfo = GetData.get_bookinfo(self)

    def get_maasoom(self):
        sanad = self.book.find('p', id=self.hadith_id)
        maasoom = sanad.findAll('format', class_='maasoom')
        maasoom_final = ""
        for i in maasoom:
            eng_filter = re.search('[a-zA-z]', i.get_text())
            if eng_filter is None:
                maasoom_final += i.get_text() + '\n'
        self.maasoom = maasoom_final
        return maasoom_final

    def get_sanad(self):
        hadith = daaem_al_islam.find('p', id=self.hadith_id)
        sanad = hadith.find('format', class_='sanadHadith')
        sanad_split = re.split(r'<format|</format>', sanad.get_text())
        x = " ".join(sanad_split)
        eng_filter = re.search('[a-zA-z]', x)
        sanad_final = ''
        for i in x:
            if eng_filter is None:
                sanad_final += str(i)
        self.sanad = sanad_final
        return sanad_final

    def get_texts(self):
        hadith = self.book.find('p', id=self.hadith_id)
        text = hadith.find('format', class_='hadith')
        text.find('format', class_='sanadHadith').clear()
        text_split = re.split(r'<format|</format>', text.get_text())
        x = " ".join(text_split)
        eng_filter = re.search('[a-zA-z]', x)
        text_final = ''
        for i in x:
            if eng_filter is None:
                text_final += i
        self.text = text_final
        return text_final

    def get_footnote(self):
        hadith = self.book.find('p', id=self.hadith_id)
        pages = hadith.find_parent('div', class_='PageText')
        code = pages.findAll('div', class_='CODE')
        letter_footnote = []
        letter_footnote += hadith.findAll('lfootnote')
        footnote = []
        footnote = code[0].find(text='________________________________________').parent.parent.find_all('p', class_="G")
        footnote_one = footnote[0].get_text()
        other_footnotes = []
        for i in range(0, len(footnote)):
            other_footnotes += footnote[i].findAll('footnote')
        final_footnotes = ""
        for i in letter_footnote:
            if '(' + i.get_text() + ')' in footnote_one:
                final_footnotes += footnote_one
            for x in range(0, len(other_footnotes)):
                if '(' + i.get_text() + ')' in other_footnotes[x].get_text():
                    final_footnotes += other_footnotes[x].get_text()
            final_footnotes += '\n'
        text = GetData.get_texts(self)
        text_arr = text.split()
        indexes = []
        for i in text_arr:
            if is_digit(i):
                indexes.append(text_arr.index(i))
        tople_footnote = ()
        for i in range(0, len(letter_footnote)):
            tople_footnote += (letter_footnote[i].get_text(), final_footnotes.split('\n')[i], text_arr[indexes[i - 1]]),
        self.footnote = tople_footnote
        return tople_footnote

    def get_bookinfo(self):
        hadith = self.book.find('p', id=self.hadith_id)
        page_num = hadith.find_parent('div', class_='PageText') \
            .find('div', class_='PageHead') \
            .find('span', class_='PageNo') \
            .get_text()
        cover_num = hadith.find_parent('div', class_='PageText') \
            .find('div', class_='PageHead') \
            .find('span', class_='PageTitle') \
            .get_text()
        final_page_num = ""
        for x in page_num:
            if is_digit(x):
                final_page_num += x
        final_page_num = int(final_page_num)
        final_cover_num = ""
        for c in cover_num:
            if is_digit(c):
                final_cover_num += c
        page_cover = (final_page_num, final_cover_num)
        self.bookinfo = page_cover
        return page_cover


Daaem_AlIslam = GetData(3084)
print(Daaem_AlIslam.bookinfo)
