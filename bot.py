# Import library to make bot interact with discord
import discord
from discord.ext import commands

# Import library to randomly choose a word from the list
import random

# Import library to interact with JSON files
import json

# Set up a command prefix to allow bot interaction
client = commands.Bot(command_prefix = '.')

# Remove the default help command to allow for the custom one
client.remove_command('help')

# Wordbank for hangman
words = {"bank":['awkward', 'jazz', 'dragon', 'abyss', 'unicorn', 'medusa', 'sphinx', 'manticore', 'phoenix', 'minotaur',
         'polytheism', 'monotheism', 'deity', 'omniscient', 'context', 'metaphor', 'essay', 'english', 'genre', 'haiku',
         'skiing', 'aerobics', 'rugby', 'basketball', 'jogging', 'virtual', 'monitor', 'microsoft', 'bluetooth',
         'hangman', 'charades', 'jigsaw', 'uno', 'poker', 'gallery', 'nightclub', 'store', 'museum', 'canada', 'colombia', 'liberia',
         'vietnam', 'cuba', 'contempt','nostalgia', 'puzzled', 'loneliness', 'joyful', 'beekeeper', 'author', 'teacher', 'salesman', 'coach',
         'artist', 'physician', 'privacy', 'premium', 'popular', 'discord']}
    
# Variables storing the hangman (this looks complicated but it's just the hangman drawing in string form)
hangman = ['  _____ \n |     | \n |      \n |        \n |        \n | \n ---', # Nothing
           '  _____ \n |     | \n |     o \n |        \n |        \n | \n ---', # Head
           '  _____ \n |     | \n |     o \n |     |  \n |      \n | \n ---', # Head + Body
           '  _____ \n |     | \n |     o \n |    /| \n |     \n | \n ---', # Head + Body + Arm
           '  _____ \n |     | \n |     o \n |    /|\\ \n |     \n | \n ---', # Head + Body + Arm x2
           '  _____ \n |     | \n |     o \n |    /|\\ \n |    /  \n | \n ---', # Head + Body + Arm x2 + Leg
           '  _____ \n |     | \n |     o \n |    /|\ \n |    / \\ \n | \n ---'] # Head + Body + Arm x2 + Leg x2

# Dictionary of games. Stores seperate games by server so different servers have different games
game = {}

# Define class for a game. This is a template for creating new and unique hangman games
class newGame:

    # Function to create a new class. Every class is a unique game with a unique word
    def __init__(self, word):

        # Variable to contain the word
        self.word = word

        # Variable for the letters
        self.letters = []

        # Variable to count mistakes
        self.mistakes = 0

        # Variable to track used letters
        self.usedLetters = []
        
        # Hangman strings
        self.person = ['  _ _ _ \n |     | \n |      \n |        \n |        \n | \n _ _ ', # Nothing
                       '  _ _ _ \n |     | \n |     o \n |        \n |        \n | \n _ _', # Head
                       '  _ _ _ \n |     | \n |     o \n |     |  \n |      \n | \n _ _', # Head + Body
                       '  _ _ _ \n |     | \n |     o \n |    /| \n |     \n | \n _ _', # Head + Body + Arm
                       '  _ _ _ \n |     | \n |     o \n |    /|\\ \n |     \n | \n _ _', # Head + Body + Arm X2
                       '  _ _ _ \n |     | \n |     o \n |    /|\\ \n |    /  \n | \n _ _', # Head + Body + Arm X2 + Leg
                       '  _ _ _ \n |     | \n |     o \n |    /|\ \n |    / \\ \n | \n _ _ '] # Head + Body + Arm X2 + Leg

    # Function to break up the word into dashes (JAZZ -> _ _ _ _)
    def breakWord(self, word, letters):
        
        # Measure the word to break it up correctly
        wordLength = len(word)

        # Loop to create dashes for the empty list of letters
        for i in range(wordLength):
            letters.append("_")
         
# Event for when bot is ready
@client.event
async def on_ready():
    
    # Debugging statement sent to console at home
    print("Bot is ready.")

# Command to view the custom word bank
@client.command()
async def bank(ctx):

    # Check to see if there is a game
    if ctx.guild.id in game:

        # Restrict access to the bank when there is a game to prevent cheating
        await ctx.send("```There is currently a game in progress. Access to the custom word bank is limited.```")

    # If there isn't a game in progress, access to the bank is unfiltered
    else:

        # Get the guild number and convert it to a string
        number = str(ctx.guild.id)

        # Access the json file 
        with open("wordBank.json", "r") as jsonFile:

            # Store the data to the 'data' variable
            data = json.load(jsonFile)

        # If the word bank is empty send a message
        if number not in data or data[number] == []:
            await ctx.send("```The custom word bank is empty.```")
            await ctx.send("```Use the commands .add and .delete to modify the custom word bank.```")

        # If there the guild number is in the json file, print all all entries
        else:   
            customBank = data[number]
            await ctx.send(f"```Custom Word Bank: {(', '.join(map(str, customBank)))}```")
            await ctx.send("```Use the commands .add and .delete to modify the custom word bank.```")
            
# Command to add a word to the json file
@client.command()
async def add(ctx, *addition):

    # Keep track of all the words added
    wordsAdded = 0

    # For every word that is being added:
    for i in addition:
        
        # Vet the word
        if i.isalpha() == False:
            await ctx.send(f"```Invalid Input. Words must contain no numbers or special characters. '{i}' will not be added to the custom word bank.```")

        # If the word is valid, continue the function
        else:

            # Get the guild number and convert it to a string
            number = str(ctx.guild.id)

            # Lowercase the word
            word = i.lower()

            # Access the json file
            with open("wordBank.json", "r") as jsonFile:

                # Store the data to the 'data' variable
                data = json.load(jsonFile)

            # If the guild number is not in the json data, create a new empty list for new words
            if number not in data:
                data[number] = []

            # Store the custom bank in a variable
            customBank = data[number]

            # Check to see if the word is already in the bank
            if word in customBank:

                # Send a message if the word is already in the bank
                await ctx.send(f"```'{word}' is already in the custom word bank.```")

            # If the word is not in the bank, add the word
            else:
                customBank.append(word)
                
                # Track a new word being added
                wordsAdded += 1

            # Open the json file
            with open("wordBank.json", "w") as jsonFile:

                # Format the data and update the json file
                json.dump(data, jsonFile)

    # Send a message based on previous actions
    if wordsAdded == 1:
        await ctx.send(f"```A word has been added to the custom word bank. Use the command .bank to view all words in the custom word bank.```")

    elif wordsAdded > 1:
        await ctx.send(f"```Words has been added to the custom word bank. Use the command .bank to view all words in the custom word bank.```")

    else:
        await ctx.send(f"```No items were added to the custom word bank. Use the command .bank to view all words in the custom word bank.```")

# Command to delete a word from the json file
@client.command()
async def delete(ctx, *delete):

    # Keep track of all the words deleted
    wordsDeleted = 0

    # For every word that is being deleted:
    for i in delete:

        # Get the guild number and convert it to a string
        number = str(ctx.guild.id)

        # Lowercase the word
        word = i.lower()

        # Access the json file
        with open("wordBank.json", "r") as jsonFile:

            # Store the data to the 'data' variable
            data = json.load(jsonFile)

        # If the guild number is not in the json data, create a new empty list for new words
        if number not in data:
            data[number] = []

        # Store the custom bank in a variable
        customBank = data[number]

        # Check the bank for the word
        if word in customBank:

            # If the word is in the bank, delete it
            customBank.remove(word)

            # Track the amount of words deleted
            wordsDeleted += 1

        # If the word is not in the custom word bank, send a message
        else:
            await ctx.send(f"```'{word}' is not a word in the custom word bank.```")

        # Open the json file
        with open("wordBank.json", "w") as jsonFile:

            # Format the data and update the json file
            json.dump(data, jsonFile)


    # Send a message based on previous actions
    if wordsDeleted == 1:
        await ctx.send(f"```A word has been deleted from the custom word bank. Use the command .bank to view all words in the custom word bank.```")

    elif wordsDeleted > 1:
        await ctx.send(f"```Words has been deleted from the custom word bank. Use the command .bank to view all words in the custom word bank.```")

    else:
        await ctx.send(f"```No items were deleted to the custom word bank. Use the command .bank to view all words in the custom word bank.```")
    
# Command to start a new game
@client.command()
async def hangman(ctx, *mode):

    # Check to see if there is a game
    if ctx.guild.id in game:
        await ctx.send("```There is currently a game in progress. Use the .restart command if you wish to restart the game.```")

    # Check to see if there are no more than one modifiers
    elif len(mode) > 1:
        await ctx.send("```The .hangman command does not support more than one modifier.```")
        
    # If there isn't a game and the modifiers are good, create a game
    else:

        # Enable the custom word bank option until otherwise
        customBankOption = True

        # Access the json file
        with open("wordBank.json") as jsonFile:

            # Store the data to the 'data' variable
            data = json.load(jsonFile)

        # Retrieve the bank from the json file
        bank = data['bank']

        # Get the guild number and convert it to a string
        number = str(ctx.guild.id)

        # If the guild has not been added to the json file, disable the custom word bank option
        if number not in data:
            customBankOption = False

            # Create a bank for that server
            data[number] = []
            
        # If the guild has a custom word bank, store it in the 'custom bank' variable
        else:
            customBank = data[number]

        # If the bank is empty, disable the custom word bank option
        if data[number] == []:
            customBankOption = False

        # Determine the game mode based on the modifiers
        if "-c" in mode and customBankOption == True:
            customGame = True
            defaultGame = False
            await ctx.send("```[Custom Game Mode] has been enabled. The game will only use words in the custom word bank. Use the command .help for more information.```")

        elif "-m" in mode and customBankOption == True:
            customGame = True
            defaultGame = True
            await ctx.send("```[Mixed Game Mode] has been enabled. The game will use words in the default word bank and the custom word bank. Use the command .help for more information.```")

        elif ("-m" in mode or "-c" in mode) and customBankOption == False:
            customGame = False
            defaultGame = True
            await ctx.send("```[Default Game Mode] has been enabled. The game will only use words in the default word bank. To access other game modes, add words to the custom word bank. Use the command .help for more information.```")
            
        else:
            customGame = False
            defaultGame = True
            await ctx.send("```[Default Game Mode] has been enabled. The game will only use words in the default word bank. Use the command .help for more information.```")

        # Send message
        await ctx.send('```A new game has been started. Use the .guess command to guess letters. Use the .fill command to guess a word. You can use the .guess command to guess multiple letters.```')

        # Prepare to choose from a word bank
        choice = random.randrange(1,7)

        # Choose a word based on all the conditions established
        if defaultGame == True and customGame == False:
            chosenWord = random.choice(bank)

        elif defaultGame == True and customGame == True:
            if choice == 1 and customBankOption == True:
            
                chosenWord = random.choice(customBank)

            else:
                chosenWord = random.choice(bank)

        elif defaultGame == False and customGame == True:

            if customBankOption == True:
                chosenWord = random.choice(customBank)

            else:
                chosenWord = random.choice(bank)
            
        else:
            chosenWord = random.choice(bank)

        # Print the word to my console for "debugging purposes"
        print(f"The word is: {chosenWord}")

        # Create a new game specifically for the current server (AKA guild) using the game class template
        game[ctx.guild.id] = newGame(chosenWord)

        # Break the word up into empty pieces
        game[ctx.guild.id].breakWord(game[ctx.guild.id].word, game[ctx.guild.id].letters)

        # Send the hangman to the chat and post all the letters used and correct
        await ctx.send(f"```{game[ctx.guild.id].person[game[ctx.guild.id].mistakes]}\n \n Letters Used: {(' '.join(map(str, game[ctx.guild.id].usedLetters)))}```")
        await ctx.send(f"```{(' '.join(map(str, game[ctx.guild.id].letters)))}```")

# Command to restart the game
@client.command()
async def restart(ctx, *mode):

    # Check to see if there are no more than one modifiers
    if len(mode) > 1:
        await ctx.send("```The .restart command does not support more than one modifier.```")
        
    # Check to see if there is a game
    elif ctx.guild.id in game:
        
        # Enable the custom word bank option until otherwise
        customBankOption = True

        # Access the json file
        with open("wordBank.json") as jsonFile:

            # Store the data to the 'data' variable
            data = json.load(jsonFile)

        # Retrieve the bank from the json file
        bank = data['bank']

        # Get the guild number and convert it to a string
        number = str(ctx.guild.id)

        # If the guild has not been added to the json file, disable the custom word bank option
        if number not in data:
            customBankOption = False
            
        # If the guild has a custom word bank, store it in the 'custom bank' variable
        else:
            customBank = data[number]

        # If the bank is empty, disable the custom word bank option
        if data[number] == []:
            customBankOption = False

        # Determine the game mode based on the modifiers
        if "-c" in mode and customBankOption == True:
            customGame = True
            defaultGame = False
            await ctx.send("```[Custom Game Mode] has been enabled. The game will only use words in the custom word bank. Use the command .help for more information.```")

        elif "-m" in mode and customBankOption == True:
            customGame = True
            defaultGame = True
            await ctx.send("```[Mixed Game Mode] has been enabled. The game will use words in the default word bank and the custom word bank. Use the command .help for more information.```")

        elif ("-m" in mode or "-c" in mode) and customBankOption == False:
            customGame = False
            defaultGame = True
            await ctx.send("```[Default Game Mode] has been enabled. The game will only use words in the default word bank. To access other game modes, add words to the custom word bank. Use the command .help for more information.```")
            
        else:
            customGame = False
            defaultGame = True
            await ctx.send("```[Default Game Mode] has been enabled. The game will only use words in the default word bank. Use the command .help for more information.```")

        # Send message
        await ctx.send('```A new game has been started. Use the .guess command to guess letters. Use the .fill command to guess a word. You can use the .guess command to guess multiple letters.```')

        # Prepare to choose from a word bank
        choice = random.randrange(1,7)

        # Choose a word based on all the conditions established
        if defaultGame == True and customGame == False:
            chosenWord = random.choice(bank)

        elif defaultGame == True and customGame == True:
            if choice == 1 and customBankOption == True:
            
                chosenWord = random.choice(customBank)

            else:
                chosenWord = random.choice(bank)

        elif defaultGame == False and customGame == True:

            if customBankOption == True:
                chosenWord = random.choice(customBank)

            else:
                chosenWord = random.choice(bank)
            
        else:
            chosenWord = random.choice(bank)

        # Print the word to my console for "debugging purposes"
        print(f"The word is: {chosenWord}")

        # Create a new game specifically for the current server (AKA guild) using the game class template
        game[ctx.guild.id] = newGame(chosenWord)

        # Break the word up into empty pieces
        game[ctx.guild.id].breakWord(game[ctx.guild.id].word, game[ctx.guild.id].letters)

        # Send the hangman to the chat and post all the letters used and correct
        await ctx.send(f"```{game[ctx.guild.id].person[game[ctx.guild.id].mistakes]}\n \n Letters Used: {(' '.join(map(str, game[ctx.guild.id].usedLetters)))}```")
        await ctx.send(f"```{(' '.join(map(str, game[ctx.guild.id].letters)))}```")

    # If there isn't a game, tell the player they can't restart
    else:
        await ctx.send("```There is currently no game in progress. Use the .hangman command to start a new game.```")
        
# Command to compute a guess
@client.command()
async def guess(ctx, *inputLetter):

    # Check to see if there is a game
    if ctx.guild.id not in game:
        await ctx.send("```There is currently no game in progress. Use the .hangman command to start a new game.```")

    # If a game is in progress, proceed
    else:

        # Create an empty list to store all guesses
        guess = []

        # For every inputed letter:
        for i in inputLetter:

            # Lower case the letter
            lower = i.lower()

            # Add the letter to the guess list
            guess.append(lower)

        # For every guess
        for i in guess:
            
            # Vet the guess to make sure it is a letter, under one character, and haven't been used yet
            if i.isalpha() == False or len(i) > 1 or i.lower() in game[ctx.guild.id].usedLetters:

                # If the letter has been used, tell the player
                if i.lower() in game[ctx.guild.id].usedLetters:
                        
                    await ctx.send(f"```'{i}' has already been used.```")

                # If the guess is invalid for any other reason, send a message to tell them
                else:

                    await ctx.send("```Invalid Input.```")

            # If the guess is valid, proceed
            else:

                # Search the word for the letter
                currentIndex = 0
                for j in game[ctx.guild.id].word:

                    # If the letter is in the word, fill in the letters list in the game class
                    if j == i:
                        game[ctx.guild.id].letters[currentIndex] = i
                        
                    # Continue the search
                    currentIndex += 1

                # If the letter is not in the word, add a point to mistakes variable
                if i not in game[ctx.guild.id].word:

                    # Increase mistake counter
                    game[ctx.guild.id].mistakes += 1

                # Add the letter to the used bin
                game[ctx.guild.id].usedLetters.append(i)


        # Send the hangman to the chat and post all the letters used and correct
        await ctx.send(f"```{game[ctx.guild.id].person[game[ctx.guild.id].mistakes]}\n \n Letters Used: {(' '.join(map(str, game[ctx.guild.id].usedLetters)))}```")
        await ctx.send(f"```{(' '.join(map(str, game[ctx.guild.id].letters)))}```")

        # End the game if there are no more empty dashes
        if "_" not in game[ctx.guild.id].letters:

            # Send the win message
            await ctx.send("```Congratulations, you figured it out! The game is now over.```")

            # Delete the class
            del game[ctx.guild.id]

        # End the game if the player has made 6 mistakes
        elif game[ctx.guild.id].mistakes == 6:
            # Send the win message
            await ctx.send(f"```Game Over! The word was '{game[ctx.guild.id].word}'.```")

            # Delete the game
            del game[ctx.guild.id]

# Command to fill in the word
@client.command()
async def fill(ctx, *, inputWord):
    
    # Check to see if there is a game
    if ctx.guild.id not in game:
        await ctx.send("```There is currently no game in progress. Use the .hangman command to start a new game.```")

    # If a game is in progress, proceed
    else:
        # Lowercase the guess to prevent capitalized letters from being used
        guess = inputWord.lower()

        # Vet the guess to make sure it is a letter, under one character, and haven't been used yet
        if guess.isalpha() == False:

            # If the guess is invalid for any reason, send a message to tell them
            await ctx.send("```Invalid Input.```")

        # If the guess is valid, proceed
        else:

            # If the word is correct, end the game
            if guess == game[ctx.guild.id].word:

                # For every letter in guess
                for i in range(len(guess)):

                    # Fill in the list
                    game[ctx.guild.id].letters[i] = guess[i]
                    

            # If the word is wrong, add a counter to mistakes variable
            else:
                # Increase mistake counter
                game[ctx.guild.id].mistakes += 1

            # Send the hangman to the chat and post all the letters used and correct
            await ctx.send(f"```{game[ctx.guild.id].person[game[ctx.guild.id].mistakes]}\n \n Letters Used: {(' '.join(map(str, game[ctx.guild.id].usedLetters)))}```")
            await ctx.send(f"```{(' '.join(map(str, game[ctx.guild.id].letters)))}```")

            # End the game if there are no more empty dashes
            if "_" not in game[ctx.guild.id].letters:

                # Send the win message
                await ctx.send("```Congratulations, you figured it out! The game is now over.```")

                # Delete the class
                del game[ctx.guild.id]

            # End the game if the player has made 6 mistakes
            elif game[ctx.guild.id].mistakes == 6:
                # Send the win message
                await ctx.send(f"```Game Over! The word was '{game[ctx.guild.id].word}'.```")

                # Delete the game
                del game[ctx.guild.id]

# Command to end a game
@client.command()
async def end(ctx):
    
    # Check to see if there is a game
    if ctx.guild.id not in game:

        # If there isn't a game, tell the user
        await ctx.send("```There is currently no game in progress. Use the .hangman command to start a new game.```")

    else:
        # Delete the class
        del game[ctx.guild.id]
        
        # Update the user
        await ctx.send("```The game has been ended.```")
        
# Command to help users understand the bot and commands
@client.command()
async def help(ctx):

    # Send information to the chat
    await ctx.send("```Commands: \n  .add [word]: adds a word(s) to the custom word bank \n  .bank: displays all items in the custom word bank \n  .delete [word]: deletes a word(s) from the custom word bank \n  .end: ends a game \n  .fill [word]: fill in a potential solution during a game \n  .guess [letter]: guess a letter(s) during a game \n  .hangman [-modifier]: starts a new game \n    -c: starts a game using only the custom word bank \n    -m starts a game using both word banks \n  .restart [-modifier]: restarts a game with a different word \n    -c: starts a game using only the custom word bank \n    -m starts a game using both word banks \n \nTo start a game, use the .hangman command. Good luck and have fun!```")
    
# Assign bot to token generated by discord
client.run('ADD TOKEN')
