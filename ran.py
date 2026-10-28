from random import * 

secret = randint(1,20)

guess = 0 

tries = 0
print("I'm thinking of a number between 1 and 20")

while guess != secret:
    guess = int(input('Take a guess:'))
    tries += 1 
    if guess > 20 or guess < 1: print('your guess is out of range')
    elif guess < secret: print('too low')
    elif guess > secret: print('too high')
    else:
        print('You got it in. Your tries: ', tries, sep = '')
