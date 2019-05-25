
# qContent

An asynchronous content tracker.

## Installation

## Usage

## Testing



### How does it do it?

Utilizes aiohttp to call out quickly, and then hashes the html. Checks that html against a saved hash to see if it is updated.

### Why are you using sha512?

While sha512 is not the quickest hashing algorithm in the world, it does offer some great protections against collisions.

### The probability of a collision in sha256 has a probability of ~.5*(n/(2^128)) collisions for n-values. Why do you need to go up to 512? And, for that matter, why are you worried about collisions?

Touche, me. Perhaps you would like to contribute a pull request that allows you to choose your own hashing algorithm. Besides, the real hang up right now is not in the hashing, but in the file i/o that is being done.

### Nah, not right now.

Well, okay then.


