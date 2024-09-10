# CORA_Crackme_Generator

!!!! NOTE !!!!!!

As of right now, this program is incomplete. What's there seems to work, but I need to add further difficulty levels.
I'm basically just dumping this here incomplete as an extra backup, so stay tuned for the complete version!

Thought levels 5-6 were complete, but when attempting them on Kali Linux, I found an unusual problem. I techincally found a fix,
but it doesn't really make sense as to why it fixed it and seems to be a really crude way of doing so.
All the other current levels work on both Ubuntu and Kali, not sure if any of it works on Windows, though.

!!!!!!!!!!!!!!!!

CORA: Crackme Originating Randomizing Automator

For generating crackme challenges of different difficulty levels.

When studying software reverse engineering, I came across the concept of crackme challenges. I found many of them, but when searching for a program
that generates them, it seemed to turn up nothing. So, that's exactly what I made.

You enter the name of the resulting executable, and the difficulty level (0-8 so far). Then, it generates a prng key with varying size, and
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
