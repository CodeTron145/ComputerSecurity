from cryptogram import Cryptogram


class Cryptogram:

	def __init__(self, line):
		self.letters = []

		for byteStr in str(line).split(' '):
			self.letters.append(chr(int(byteStr, 2)))

	def letter_id(self, index):
		if index < len(self.letters):
			return self.letters[index]
		else:
			return '*'

class Decrypt:
    def __init__(self, data):
        self.data = data
        self.cryptograms = []

        self.letter_freq = {'a': 89, 'i': 82, 'o': 78, 'e': 77, 'z': 56, 'n': 55, 'r': 47, 'w': 47, 's': 43, 't': 40,
                           'c': 40, 'y': 38, 'k': 35, 'd': 33, 'p': 31, 'm': 28, 'u': 25, 'j': 23, 'l': 21, 'b': 15,
                           'g': 14, 'h': 11, 'f': 3, 'q': 1, 'v': 1, 'x': 1, ' ': 100, ',': 16, '.': 10, '-': 10,
                           '"': 10, '!': 10, '?': 10, ':': 10, ';': 10, '(': 10, ')': 10}

        self.create_cryptograms()

    def create_cryptograms(self):
        for line in self.data.splitlines():
            self.cryptograms.append(Cryptogram(line))

    def find_key(self):
        key = []
        longestString = max(len(cryptogram.letters) for cryptogram in self.cryptograms)

        for i in range(longestString):
            possible_keys = {}
            for cryptogram in self.cryptograms:
                if i >= len(cryptogram.letters):
                    continue

                for letter in self.letter_freq.keys():
                    possible_key = ord(cryptogram.letter_by_id(i)) ^ ord(letter)
                    possible_keys[possible_key] = possible_keys.get(possible_key, 0) + self.letter_freq[letter]

            sorted_keys = sorted(possible_keys.keys(), key=lambda k: possible_keys[k], reverse=True)

            possible_letter = ord(' ')
            count = 0

            for letter in sorted_keys:
                counter = 0

                for cryptogram in self.cryptograms:
                    if i >= len(cryptogram.letters):
                        continue
                    if (chr(ord(cryptogram.letter_by_id(i)) ^ letter)) in self.letter_freq.keys():
                        counter += 1

                if counter > count:
                    count = counter
                    possible_letter = letter

            key.append(possible_letter)
        return key

    def decrypt(self):
        key = self.find_key()
        result = ""

        for cryptogram in self.cryptograms:
            for i in range(0, len(cryptogram.letters)):
                result += chr(ord(cryptogram.letter_by_id(i)) ^ key[i])
            result += "\n"

        return result


def main():
    with open('data.txt', 'r') as file:
        decrypt = Decrypt(file.read())

    txt = decrypt.decrypt()
    print(txt)


if __name__ == '__main__':
    main()
