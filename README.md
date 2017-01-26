
# Async Content

An asynchronous content tracker.

## How do I use it?

First create a file called `whatever_the_hell_you_want.anything`, that follows the structure:
```
http://site1 NOHASH
http://site2 NOHASH
.
.
.
http://siteN NOHASH
```
and then go into `asyncent\__main__.py` and change `sample.txt` to `path\to\whatever_the_hell_you_want.anything`.

After this short setup, run the module with `python -m asyncent`.



## FAQs (Questions asked more than 0 times)

### How does it do it?

Utilizes aiohttp to call out quickly, and then hashes the html. Checks that html against a saved hash to see if it is updated.

### Why are you using sha512?

While sha512 is not the quickest hashing algorithm in the world, it does offer some great protections against collisions.

### The probability of a collision in sha256 has a probability of ~.5*(n/(2^128)) collisions for n-values. Why do you need to go up to 512? And, for that matter, why are you worried about collisions?

Touche, me. Perhaps you would like to contribute a pull request that allows you to choose your own hashing algorithm. Besides, the real hang up right now is not in the hashing, but in the file i/o that is being done.

### Nah, not right now.

Well, okay then.


