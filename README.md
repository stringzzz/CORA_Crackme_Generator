# CORA_Crackme_Generator

I finished this project for now. Levels 0-9 are complete and tested (On Ubuntu and Kali). I may make further levels eventually, but I'm not sure yet.
One thing I will do is analyze the disassemblies of them, and along with the solution code I already have written,
I will upload a directory 'solutions' with all of that.

!!!! NOTE !!!!!!

If you are using any version that was up on here before 09-10-2024, do not bother using it, just download the new one.
The newer one will have this comment at the top:

"Major overhaul to fix several different problems Complete Date: 09-10-2024"

Due to the mistakes made in it, you can actually end up getting the correct password, but it won't be correct
in the 'strcmp' by time it goes through the rest of the code. This is an embarassing mistake, and apologies
to anyone who used this program before that date, as they may have wasted a lot of time trying to solve something that didn't even
work properly. (>_<)

!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!

CORA: Crackme Originating Randomizing Automator

For generating crackme challenges of different difficulty levels.

When studying software reverse engineering, I came across the concept of crackme challenges. I found many of them, but when searching for a program
that generates them, it seemed to turn up nothing. So, that's exactly what I made.

You enter the name of the resulting executable, and the difficulty level (0-9). Then, it generates a prng key with varying size, and
sets up the C source code according to the difficulty level. Finally, it outputs the source code and compiles it with gcc. Then, the idea is to use whatever tools
you wish to RE the executable and get the correct password to input. Obviously, you could just change the jump conditional to a jmp straight to
the win message, but this defeats the whole point of the challenge. Do what you want, though...

It uses gcc by default, but of course you could change this to any other command line C compiler of your choice. 
If you want to see the source code first without compiling it, you can also just comment out that 'os.system(gcc __)' line. 

By default, it also does not delete the source code file. If you are serious about practicing reverse engineering, you may want to 
uncomment the 'os.system(rm -i ___)' line so it deletes that file, then you can avoid the temptation of peeking at the C source which does make it too easy to solve.

This program will not have any kind of license on it, so you are free to do whatever with it.
I hope someone gets something out of this, enjoy!
--stringzzz
