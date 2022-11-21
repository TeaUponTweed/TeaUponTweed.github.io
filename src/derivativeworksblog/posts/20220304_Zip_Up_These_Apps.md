Zip Up These Apps March 4th, 2022 (Edited November 20th, 2022)
---------------------------------

<!---
Goal: Make people think about why companies choose to implement certain features serverside.
Outline:
- Showcase the problem
- Explain what is happening

-->
Here is an experiment: Turn your phone on airplane mode and ask (hey Siri in my case) it to tell you the time.
You should see something like:

```
You: "Hey Siri, what time is it?"
....
...
....
Siri: "Sorry..."
```

Notice two things:
First, that the hard problem of transcribing free form human speech into text is accomplished flawlessly.
Second, the relatively simple task of executing the command isn't even attempted.
Regardless of the arcane magic that Apple employs to transform the text "what time is it" into 8:43, one could imagine using a lookup table [1].
Mapping a list of common commands to actual implementations seems like something a large multinational corporation would be capable of.
They're, but no not, because it's not in their interest.
[Until recently](https://openai.com/blog/whisper/) voice transcription was a "hard" problem.
Recently, the best way to tackle these hard problems has been:
1) Provide source data that your algorithm will operate on
2) describe what you would like it to do

From these simple ingredients, you have a recipe to make some pretty [amazing things](https://en.wikipedia.org/wiki/Reinheitsgebot).
However, sometime a recipe calls for the equivalent of "10 billion kg flour"/
That's where the always online requirements come from, you need to offer the flour one bit at a time.
Voice transcription is a [benign](https://www.politico.com/news/2022/02/16/my-journey-down-the-rabbit-hole-of-every-journalists-favorite-app-00009216) case, and many would donate their data towards the goal of never typing again.
However, there are issues.
Firstly with privacy and "you _are_ the product" and [all that](https://www.kolide.com/blog/is-grammarly-a-keylogger-what-can-you-do-about-it). 
Arguably as importantly: it makes the user experience worse for no appreciable benefit.
Computing has and continues to advance incredibly, but expectations are slipping.

[1] I don't need to talk to my IPhone like a person, just like I'm fine not writing letters to a C++ compiler. This might not be a popular opinion.
