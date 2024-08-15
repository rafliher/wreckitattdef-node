class Satanize:
    def __init__(self):
        FLAG = open('../flag.txt', 'r').read().strip()
        self.banned_words = ["7","import","system"]
        # self.banned_words = ""

    def satanizer(self, text):
        for word in self.banned_words:
            if word in text:
                print("SATANNNNNNNN")
                return True
        return False
