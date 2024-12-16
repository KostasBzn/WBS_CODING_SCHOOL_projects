import random

def hangman():
    words = ["python", "chair", "programming", "berlin", "laptop", "bootcamp", "winter"]
    random_word_to_guess = random.choice(words)
    word_to_guess = "_"*len(random_word_to_guess)
    guessed_letters = []
    attempts = 6
    print("**Welcome to Hangman!**")
    print("Try to guess the word..you have 6 wrong attempts!\n")
    while attempts > 0:
       print("Progress: ", word_to_guess)
       print(f"You have {attempts} attempts left.")
       guessed_letter = input("Please guess a letter:").lower()
       
       if not guessed_letter.isalpha() or len(guessed_letter) != 1:
            print("Please type a valid alphabetic character.\n")
            continue
       
       if guessed_letter in guessed_letters:
           print(f"You have already guessed the letter {guessed_letter}\n")
           continue
       
       guessed_letters.append(guessed_letter)
       
       if guessed_letter in random_word_to_guess:
            print(f"Good job! The letter {guessed_letter} is in the word\n")

            for i in range(0, len(random_word_to_guess)):
              if random_word_to_guess[i] == guessed_letter:
                 word_to_guess = word_to_guess[:i] + guessed_letter + word_to_guess[i + 1:]

                
            
            if "_" not in word_to_guess:
                print(f"Congratulations! You won! The word is {random_word_to_guess}")
                break
       else:
            attempts -= 1
            print(f"Sorry, the letter {guessed_letter} is not in the word\n")
            

       if attempts == 0:
           print(f"Sorry you have run out of attempts :(")
           print(f"The word was {random_word_to_guess}")
           exit = input("Press 'Enter' to exit the game")
           if exit == "":
               print("That was fun! Until next time!")
               break
           
hangman()