class Album:

    Name :str = ""

    Artist :str = ""

    Year :str = ""

    CoverLink :str = ""

    Songs :list = []

    def info(self) ->str:
        return f"{self.Name} by {self.Artist} in {self.Year}"

    def all(self) ->str:
        return f"{self.info()} \n {self.CoverLink} \n {self.Songs}"

    def removeParens(self, string) ->str:
        result = ""
        parentheses_count = 0
        for char in string:
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
            elif parentheses_count == 0:
                result += char
        result += " " # if parentheses_count != 0 else " "
        return result

    def songs(self , includeParenthese = True) ->list:
        return [(self.removeParens(song) if includeParenthese == False else song) for song in self.Songs]

    def __str__(self):
        return self.info() + "\n" + ''.join(self.songs(False))

    def ToDictionary(self) ->dict:
        return {
        "name": self.Name,
        "artist": self.Artist,
        "year": self.Year,
        "cover": self.CoverLink,
        "songs": self.Songs
        }
