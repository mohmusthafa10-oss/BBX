def reverse_words(s):
    """Return the words of a string in reverse order."""
    s = s.split(" ")
    s.reverse()
    s = " ".join(s)
    return s


def is_palindrome(s):
    """Return True if a string is a palindrome ignoring case and punctuation."""
    s = s.casefold()
    st = []

    for char in s:
        if char.isalnum():
            st.append(char)

    st = "".join(st)
    rev = st[::-1]

    if rev == st:
        return True
    else:
        return False


def char_frequency(s):
    """Return a dictionary containing character frequencies, ignoring spaces."""
    frequency = {}

    for char in s:
        if char == " ":
            continue

        if char in frequency:
            frequency[char] = frequency[char] + 1
        else:
            frequency[char] = 1

    return frequency


def is_anagram(a, b):
    """Return True if two strings are anagrams ignoring case and spaces."""
    a = a.casefold()
    b = b.casefold()

    sa = []
    sb = []

    for char in a:
        if char.isalnum():
            sa.append(char)

    sa.sort()
    sa = "".join(sa)

    for char in b:
        if char.isalnum():
            sb.append(char)

    sb.sort()
    sb = "".join(sb)

    if sa == sb:
        return True
    else:
        return False


def capitalise_names(s):
    """Capitalise the first letter of each name."""
    return s.title()


def truncate(s, n):
    """Return a string truncated to at most n characters."""
    if len(s) <= n:
        return s

    x = n - 3
    s = s[:x]
    s = s + "..."
    return s


def count_vowels(s):
    """Return the number of vowels in a string."""
    count = 0

    for char in s:
        if char.lower() in "aeiou":
            count += 1

    return count


def longest_word(s):
    """Return the longest word in a sentence."""
    longest = ""

    for word in s.split():
        if len(longest) < len(word):
            longest = word

    return longest


if __name__ == "__main__":
    print(reverse_words("the sky is blue"))

    print(is_palindrome("A man, a plan, a canal: Panama"))

    print(char_frequency("apple"))

    print(is_anagram("listen", "silent"))

    print(capitalise_names("john  smith"))

    print(truncate("Hello world", 8))

    print(count_vowels("Hello World"))

    print(longest_word("I love programming"))
