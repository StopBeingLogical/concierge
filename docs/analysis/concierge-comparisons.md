How to Never Hit Your Claude Session Limit Again
https://youtu.be/_qZvORxGqI0

Chapter 1: Intro
0:00
If you use Claude, this video is going to save you money today. Hitting session limits has been a huge issue lately across the entire community. So, today I'm going to show you everything I know
0:07
7 seconds
about how to make sure you don't hit your limit. I'm going to show you guys a custom token dashboard that I built. I'm going to show you guys custom skills that I've built to help you manage your session limits. I'm going to show you
0:16
16 seconds
the best free tools that help you reduce the amount of tokens you're sending. And I'm going to show you Enthropic's actual best practices for making sure you don't hit your limit. So, no matter where you
0:24
24 seconds
use Claude, I'm going to save you money in this video. So, let's not waste any time and get straight into it. So let's just start at the top here with what is context. Context is basically everything that cloud code can see at one time.
Chapter 2: How Tokens Actually Work
0:35
35 seconds
That includes the system prompt, your full conversation, every tool call,
0:39
39 seconds
every tool output, every file that Claude has read, every skill or MCP server or agent in your project. It's basically all of that kind of stuff.
0:48
48 seconds
Think of it like Claude's current working memory. Now Claude Code gives us a 1 million token context window, which is a ton. But before you even type
0:56
56 seconds
anything in there, you're already burning like 8,000ish because of just startup overhead. So things like your system prompts or your cloudmd or your,
1:04
1 minute, 4 seconds
you know, context files or like I said,
1:06
1 minute, 6 seconds
MCP tools skills, things like that. And honestly, it could be way more than that 8,000. When I first found out about this, I realized that I actually had
1:13
1 minute, 13 seconds
like 62,000 tokens just off of a fresh session. So if you haven't already, go into a fresh session, do slashcontext,
1:22
1 minute, 22 seconds
and see what you're sitting at before you even send off anything. And that might tell you to delete some stuff or move some things around based on that number that you see because otherwise it
1:30
1 minute, 30 seconds
could be a lot of invisible tokens that you don't even know are being spent. And real quick, there's one super important thing that you guys have to understand about how tokens work. And this one
1:38
1 minute, 38 seconds
thing alone has saved people hundreds and thousands of tokens. So I'm going to insert a clip real quick. So as I've been optimizing my own token management,
1:45
1 minute, 45 seconds
I think that what's really important to realize first is how tokens actually work. Because once you realize how Claude uses tokens, it makes it very
1:53
1 minute, 53 seconds
clear how you should actually reverse engineer the way that you work in order to use less tokens. So a token is the smallest unit of text that an AI model
2:01
2 minutes, 1 second
reads and charges you for. It's roughly one token is one word, but that's not explicitly true. Kind of just a good baseline. So every time that you send a
2:08
2 minutes, 8 seconds
message, Claude rereads the entire conversation from the beginning. And all of those are tokens that it's charging you for. So message one, it will read
2:15
2 minutes, 15 seconds
it, then it will read its reply, and then message two, and then the reply all the way up to your latest prompt. And it does that every single time. And I think
2:23
2 minutes, 23 seconds
that alone is a huge light bulb moment for a lot of people. This means as you're having a conversation with Claude, your cost is compounding, not just adding, it's exponentially growing.
2:33
2 minutes, 33 seconds
Meaning message one might cost 500 tokens, message 30 costs 15,000 because it's rereading everything before it. One developer actually tracked a 100 plus
2:41
2 minutes, 41 seconds
message chat and found that 98.5% of all the tokens were just spent rereading the old chat history in the session. Like
2:49
2 minutes, 49 seconds
that's a huge waste. Now yes, the argument has to be made that well it needs the context and it needs to understand what we're doing. But still 98.5% is crazy. So take a quick look at
2:58
2 minutes, 58 seconds
this graphic here. Along the x-axis we have message number and as it increases you can see that we have our per message cost and our cumulative tokens
3:05
3 minutes, 5 seconds
increasing. But it's not linear. It's basically each message is rereading all of the past ones, and it has to count that in. So message one could be 500.
3:14
3 minutes, 14 seconds
Message 30 could be 15,500, which is 31 times more. And then after 30 messages,
3:18
3 minutes, 18 seconds
you might already be at almost a quarter million cumulative tokens. All right, cool. Glad you guys know that. Now,
3:23
3 minutes, 23 seconds
let's get back to the video. Which leads us into context rot. And in my mind, I basically think of context rot as a fancy word for AI dementia. Because this
Chapter 3: Context Rot & Auto Compaction
3:32
3 minutes, 32 seconds
basically happens as your session grows and the model's performance starts to degrade because its attention gets spread across every single token, every
3:40
3 minutes, 40 seconds
single message that has been sent. And basically, it starts to get really distracted. It starts to forget things.
3:44
3 minutes, 44 seconds
It starts to contradict itself and like edit files without reading them first.
3:48
3 minutes, 48 seconds
And it gets very vague and just noticeably worse. And the statistics actually show us that retrieval accuracy
3:54
3 minutes, 54 seconds
drops from 92% at 256,000 tokens all the way down to 78% at a million tokens. So
4:02
4 minutes, 2 seconds
even if you can fill up your a million token context window, the model is going to be measurably worse at finding what it needs inside of that window. And now
4:10
4 minutes, 10 seconds
if you think about that, as the model starts to get worse, your token efficiency is going way down because you might have to spend 500,000 tokens for
4:18
4 minutes, 18 seconds
example to get an output that could have taken you 200,000 tokens if the model was performing the way it should be. So try to avoid context rot at all costs
4:26
4 minutes, 26 seconds
across your sessions. Okay, so next we have autoco compaction. Now this will automatically kick in, hence autoco compaction around 95% of the way through
4:35
4 minutes, 35 seconds
your window. But all of the community has basically agreed that that's way too late. And I 100% agree because when it autocompacts, you only keep about 20 to
4:44
4 minutes, 44 seconds
30% of the original detail. So you're losing a ton of important context and the model is doing that compaction at
4:51
4 minutes, 51 seconds
its absolute least intelligent point because obviously the auto impaction fires at like the peak of context rot.
4:57
4 minutes, 57 seconds
So imagine you're packing for a trip. If you were to pack the night before, you'd have time to think and you'd grab all the right stuff and you probably wouldn't forget anything because you'd make a list and you'd check it. But if
5:06
5 minutes, 6 seconds
you're frantically stuffing your bag because you woke up 5 minutes before you have to go, you're probably going to forget your charger, your toothbrush,
5:12
5 minutes, 12 seconds
things like that, and that's basically auto compaction at 95%. So, the solution would just to be manual compaction. I like to do this about 60% of my way
5:21
5 minutes, 21 seconds
through my contact window if I'm at like the 250,000 model, which definitely beats autoco compaction at 95% every single time.
5:29
5 minutes, 29 seconds
However, there is something that I like to do which I do a lot more often compared to just manually compacting and I'm going to cover that in just a minute here. And by the way, a lot of these
5:37
5 minutes, 37 seconds
diagrams that you might be seeing right here are from Anthropics article and I thought that they were just really good.
5:42
5 minutes, 42 seconds
So, wanted to chuck them in here. But anyways, speaking of Anthropics article,
Chapter 4: Rewind, Compact, Clear, Sub Agents
5:45
5 minutes, 45 seconds
this next one was in here, this next kind of like section. And I really liked the way they put it. So, basically they said after every single time that Claude
5:52
5 minutes, 52 seconds
responds to you, you basically have five options. The first one being to continue, which means you just respond,
5:57
5 minutes, 57 seconds
you send another message. and it's very natural and it's easy to get in this loop of just continuing. And then you have slashre which lets you jump back to
6:06
6 minutes, 6 seconds
a previous message and drop everything after it. So that's very cool. You also could slash clear, start completely fresh. You could slash compact to
6:14
6 minutes, 14 seconds
summarize the session and replace the history with that summary. Or you could shoot off messages to a sub agent. So basically delegating the work to a fresh
6:21
6 minutes, 21 seconds
context window and then you get back some sort of end result. Real quick guys, I know that we're about to cover a ton of information in this video. So, I put all of this that we're about to talk
6:30
6 minutes, 30 seconds
about in a full resource guide that you can access for completely free. The link for that will be down in the description. Join my free school community and that's where you'll be able to get this doc, like I said, for
6:38
6 minutes, 38 seconds
completely free and every single other free resource that I've dropped with all my YouTube videos. So, I'll see you guys over there. Let's get back to the video.
6:44
6 minutes, 44 seconds
So, let's kind of dive into some of these because once you start to understand which ones you should use in which scenario, it could be a game changer for you. So, slashre, which is
6:53
6 minutes, 53 seconds
the number one habit that Enthropic recommends. Now, I've been doing this a lot manually, not using the actual slashre feature, but I'm definitely going to start using this feature
7:02
7 minutes, 2 seconds
because basically you can double tap escape or you can run /re and it lets you jump back to any previous message in your session and everything at that
7:09
7 minutes, 9 seconds
point after gets dropped, which is obviously huge for the context. And it's a lot more powerful than you may think because most of the time when Claude
7:17
7 minutes, 17 seconds
does something wrong, and I do this a lot myself admittedly, I will just say something like, "That didn't work. Try this instead." and then Claude will try
7:25
7 minutes, 25 seconds
something else. And a lot of times that works. So you think, "Okay, there's nothing wrong with what I just did." But if you think about it, that failed attempt, that broken code, whatever it
7:32
7 minutes, 32 seconds
did wrong, the wrong approach, all of that is still sitting in your context and it's still being read every time and it's just polluting your future responses. Now, I do think that there's
7:41
7 minutes, 41 seconds
an argument to be made about the fact that if you leave stuff like that, it's able to read through and it's able to learn and it's able to not make that same mistake again. But I think there's
7:49
7 minutes, 49 seconds
different ways that you can essentially teach Claude not to make the same mistake twice that is more effective or more efficient with your tokens than just, you know, leaving it in there.
7:57
7 minutes, 57 seconds
Maybe you just have a decision log or maybe you just, you know, prompt it better next time, things like that. So rewinding is better because now your context is clean. And when you do /re,
8:06
8 minutes, 6 seconds
there's also a summarize from here option in that menu which basically creates you a handoff message, which is,
8:12
8 minutes, 12 seconds
you know, a note from Claude's future self to its past self saying, "Here's what we figured out. Do it this way."
8:17
8 minutes, 17 seconds
Okay. So now let's talk about compact and clear. So the rule of thumb kind of from like a documentation standpoint would be if you're starting a new task
8:25
8 minutes, 25 seconds
do/clear and if you're continuing the same task do /compact. And honestly I kind of disagree. I don't use /compact
8:33
8 minutes, 33 seconds
at all anymore. What I actually do is essentially my own version of it. Um, if I'm running Opus with 1 million token
8:39
8 minutes, 39 seconds
context window, if I cross around 120,000 tokens, so about 12%, then I will just say to Claude, "Hey, give me a full summary of everything that we've
8:48
8 minutes, 48 seconds
done and the current status of what we're about to do next." And then I just take that summary and I do a slash clear, paste it in, and I keep going.
8:56
8 minutes, 56 seconds
So, I basically just get to reset, and it feels like I didn't reset because I already have all that context. It already, you know, it points to any plan files or decision files or task lists
9:05
9 minutes, 5 seconds
that were created. And that's also very key. If you're losing all that conversation history, you need to make sure you're storing data somewhere. So,
9:12
9 minutes, 12 seconds
like I said, tracking sheets, activity logs, task list, things like that. That way, even if you reset a session, it doesn't feel like you reset. It's kind
9:20
9 minutes, 20 seconds
of just like if you want to close out of all your Chrome tabs, but you still have like all of your bookmarks that you can get to really quickly. And yeah, that's just kind of the way in my mind for some
9:28
9 minutes, 28 seconds
reason that I think about it. But this one habit alone, if you can actually make that shift and start to do it, it has probably made the most noticeable
9:36
9 minutes, 36 seconds
difference on my actual session limit filling up. So what I did is I actually built a skill for this. So right here,
9:41
9 minutes, 41 seconds
you guys can see I've got, you know, a long conversation right here. We've got about 224,000 tokens out of the window already been taken up. So I just type in
9:49
9 minutes, 49 seconds
slash session handoff as you see. And now what happens is it basically will go through the whole process of reading everything, analyzing it and giving me
9:58
9 minutes, 58 seconds
the important stuff that I need to know and it spits out this output. It shows where it started decisions locked and what shipped. It shows key files for the
10:05
10 minutes, 5 seconds
next session. It shows the running state verification deferred and open questions and then pick up from here. So basically
10:12
10 minutes, 12 seconds
now I copy this whole output. I do a /cle and then I just paste in that output and I run it. And now this project is basically completely
10:20
10 minutes, 20 seconds
reoriented on what it needs to do. It says, "Okay, I'm ready. Here are all the files I need to read. Here's where we left off. Give me the next task." And now I have a completely fresh context
10:29
10 minutes, 29 seconds
window. So also this skill will be attached in the free school community.
10:32
10 minutes, 32 seconds
Just the free school community has everything that I ever share ever. So just hop in there. All right. Then we have sub agents. So this is kind of the last main core concept. Each sub aent will get its own fresh context window.
10:42
10 minutes, 42 seconds
It does its own work. It does its own research. It synthesizes results. and then it sends back basically an output to your main session. So if you think
10:50
10 minutes, 50 seconds
about it this like a research intern, if you wanted a research intern to dig through like 50 articles, you wouldn't sit there and watch him or her do it and you wouldn't read the articles as well.
10:59
10 minutes, 59 seconds
You would just say, "Hey, just let me know when you have like a summary or when you have the information I need."
11:02
11 minutes, 2 seconds
And so you're not wasting your head space with all that extra fluff. You're just getting what you want back. Now, you can just explicitly say things like, "Spin up a sub agent to verify this.
11:11
11 minutes, 11 seconds
Spin up a sub agent to review your codebase and summarize me this." And another cool thing is each time you make a sub agent, they can be using a cheaper
11:18
11 minutes, 18 seconds
model. So spin me up a sub aent to summarize this and make sure that sub aent is using haiku. And what ends up happening is that sub aent task was so
11:26
11 minutes, 26 seconds
much cheaper than if opus would have done it. And the performance and quality is about the same. The key there is knowing which tasks to actually be able to delegate. Okay, so let's move into
Chapter 5: Practical Token Tips
11:35
11 minutes, 35 seconds
some other practical tips. So this first one, which sounds really obvious and like why would you say that Nate? That's so obvious. But it's it's huge. Um, it's
11:44
11 minutes, 44 seconds
watching your session limit. Meaning, if you're in the new desktop app, you can see how much session limit you have left. Just watch it constantly. If you
11:51
11 minutes, 51 seconds
have two monitors, have one open on the other tab so you can always watch it.
11:54
11 minutes, 54 seconds
Just being able to actually peek at it every once in a while. It will change the way that you think about the prompt you might send off or should you spin up
12:01
12 minutes, 1 second
that agent team or not, you know, things like that. And just be strategic about it. If you're getting close to the end of your session and it's been a long session, go take a walk or take that
12:09
12 minutes, 9 seconds
opportunity to grab a snack or something like that. And on the flip side, if you've got like 50% of your session left and it's going to reset in like an hour
12:16
12 minutes, 16 seconds
or half an hour, then abuse it. You know, try to make that thing hit the limit. Try to spin up agent teams. Try to work on a heavy codebase that you've
12:24
12 minutes, 24 seconds
been meaning to get to. Try to do things that you know are going to eat a lot of your tokens. So, be strategic about when you're doing little productivity
12:32
12 minutes, 32 seconds
workflows or things or when you're doing some deep coding or deep building. Okay, so this next one's pretty cool.
12:38
12 minutes, 38 seconds
basically the idea of converting everything to markdown. Markdown is so much faster and so much cheaper for AI models, huge token reduction. So like
12:45
12 minutes, 45 seconds
for HTML to markdown, you're getting like 90% fewer tokens. For PDF to markdown, you're getting like 65 to 70%
12:52
12 minutes, 52 seconds
tokens reduction. For DOCX files to markdown, you're getting about 33% token reduction. So this means you can get
12:59
12 minutes, 59 seconds
roughly three times more content into the same context window. So like a 40-page PDF could actually take up the same amount of space as a 130 page
13:08
13 minutes, 8 seconds
markdown file. And you can just use a tool like Dockling or many others to convert these files in seconds because the tokenizers process text really
13:16
13 minutes, 16 seconds
really efficiently. And PDFs and docs and HTML have all of this layout and metadata and formatting noise that the model doesn't need. All the model needs
13:24
13 minutes, 24 seconds
is the content of that doc which is typically just the text. Now, if you need OCR and if you need like vision or something, that's a different story. But
13:31
13 minutes, 31 seconds
if it's textbased, just give Claude the text. All right. This next one is to use slash by the way or slashbtw. This basically opens up a quick overlay for
13:40
13 minutes, 40 seconds
side questions that don't actually enter your conversation history. So, if you're deep into a project and you need to ask a quick question about this project,
13:48
13 minutes, 48 seconds
just do /btw, type the question, and it keeps that context clean, but you can still get your question answered. Okay.
13:53
13 minutes, 53 seconds
Obviously, this next one is about plan mode, which is huge. Boris Churnney, the creator of Claude Code, starts every single session in plan mode. I do the same thing. I'm basically Boris
14:02
14 minutes, 2 seconds
Churnney. But the whole idea is if you use tokens upfront to become clear on the plan before you start building, you're not going to have to correct it.
14:09
14 minutes, 9 seconds
And ultimately, it's going to be cheaper in the long run when it comes to, you know, being efficient with your tokens.
14:14
14 minutes, 14 seconds
So that's why I pour effort into the plan first. Get it right and then let Claude oneshot the implementation because it understands what it needs to do and it understands what you want. So,
14:22
14 minutes, 22 seconds
I use things like Ultra Plan all the time or Superpowers all the time. And I will link videos that I made about both of those right up here. I would definitely recommend you check out that
14:31
14 minutes, 31 seconds
superpowers video first. All right. And this next one, you know that we couldn't get through a token video without talking about claw.md discipline. So,
14:38
14 minutes, 38 seconds
keep this file under 200 lines, roughly 2,000 tokens, because it loads every single session. So, if it's bloated,
14:44
14 minutes, 44 seconds
you're going to pay for that bloat every single conversation. You only get so much space. So, don't cram everything in there. only put in there the stuff that you actually need and only the stuff
14:52
14 minutes, 52 seconds
that Claude needs in order to actually do the job well. You can also do things like moving specialized instructions into context files that get routed to or
15:00
15 minutes
skills that get routed to and that way they only load on demand when they actually are needed. And you could use acloud ignore file to exclude folders or
15:08
15 minutes, 8 seconds
files that you don't want claude to actually read from which could be a big big play if you've got like a a massive repo. All right, as I'm sitting here editing the video, there's one more
15:16
15 minutes, 16 seconds
thing I realized I wanted to say, which was that output tokens cost more than input tokens. So, a lot of people might think that you could say, "Hey, Claude,
15:25
15 minutes, 25 seconds
be super concise and just give me, you know, one sentence responses rather than paragraphs, and that would save you tokens." And in theory, yes. But in the
15:34
15 minutes, 34 seconds
grand scheme of things, that's not what's actually going to be the, you know, deciding factor between if you're hitting your limit or not because there's so many output tokens that are
15:41
15 minutes, 41 seconds
being spent without you even really seeing in your files and things like that. So, you know, there might be I I saw this this uh caveman plugin that
15:49
15 minutes, 49 seconds
people have been using. I actually saw someone do an experiment and tested how much it really saves tokens and it turns out it wasn't actually as much as people thought because once again, there's so
15:57
15 minutes, 57 seconds
many more output tokens than just what Claude actually gives you back in the window. So, I think it's important to understand that output tokens cost more than input tokens, but just simply
Chapter 6: Token Dashboard
16:06
16 minutes, 6 seconds
saying like be concise isn't really going to move the needle. So, just wanted to throw that out there, too. So,
16:10
16 minutes, 10 seconds
another super important thing is just actually knowing where your tokens are going because that will kind of reverse engineer your brain to think about how you can save them better. So, this is a
16:18
16 minutes, 18 seconds
token dashboard that I built. I'm going to make this repo public and you guys will be able to go access it for completely free. Just join my free school community. The link for that will be down in the description and you'll be
16:26
16 minutes, 26 seconds
able to find this in there and get set up. but basically just shows us things like our sessions, our turns, our input tokens, output tokens, cash read, and
16:34
16 minutes, 34 seconds
cash create, which is important to understand. And if you don't understand what these mean, just look right here.
16:38
16 minutes, 38 seconds
They're pretty simple. But anyways, we can see over the past 7 days or past 30 days what's actually been going on with our token usages across models, across
16:46
16 minutes, 46 seconds
different projects, and across different tools that are being called. And it should give you some interesting insights because right here you can see in my Herk 2 project which is kind of like my executive assistant second
16:55
16 minutes, 55 seconds
brain. You can see I have way more input tokens than output tokens. Now obviously output tokens are more expensive but still this should signal to me that there's something going on here. Like
17:03
17 minutes, 3 seconds
why are all my other projects significantly more output than input but over here I've got you know 2 million more input. Why do I think this is because I recently had it read
17:12
17 minutes, 12 seconds
everything and help me reorganize things and help me you know like figure out the best way to optimize that project. So, I know that's why, but it's important to
17:19
17 minutes, 19 seconds
go see this kind of stuff. Now, what else is cool is you can go look at your actual prompts. So, in here, I can see what prompts have actually taken the most tokens, and I can look at this and understand, okay, what did I do here?
17:29
17 minutes, 29 seconds
Did I need to clear my session earlier? Why did I eat up so many tokens here?
17:32
17 minutes, 32 seconds
And how do I make sure this doesn't happen again? So, for example, if I want to open up this project right here, and I can open up this prompt and go to the session, we can see everything that I
17:40
17 minutes, 40 seconds
actually did in here. We can see all the tool calls. So we can see what happened and I could analyze this or even have Claude Code analyze this for me to figure out why this took so many tokens.
17:48
17 minutes, 48 seconds
The sessions tab also shows us all of our different sessions and how many turns and how many tokens. We also have projects so I can see by project how many tokens I'm using and how many
17:56
17 minutes, 56 seconds
sessions I've had. And then I've got a skills section which this really isn't working. It's not exactly super easy to get the tokens per call, but you can see
18:04
18 minutes, 4 seconds
you can at least see how many times your different skills have been invoked. And then also a tip section. Now I haven't really worked too much AI into here, but that would kind of be the goal. But it's
18:12
18 minutes, 12 seconds
going to show you, hey, this file was opened 181 times. This file was opened 166 times. This bash command ran 67 times in the past 7 days. So you might
18:20
18 minutes, 20 seconds
be able to identify patterns that you're not even noticing are happening. So anyways, like I said, GitHub repo in the free school community. All you have to do is take the URL, give it to Cloud
18:28
18 minutes, 28 seconds
Code, and say, "Hey, help me set this up." All right. So before we get into some bigger philosophy stuff about why I don't even think you need to use the 1 million token window model, I want to
Chapter 7: Why I Skip the 1M Window
18:36
18 minutes, 36 seconds
drop some stats on you guys. So real quick, stat one. A developer ran an analysis on GitHub of 18,000 thinking blocks across 7,000 sessions. Thinking
18:44
18 minutes, 44 seconds
depth dropped 67% as sessions got longer, and edit without reading went from 6% all the way up to 34%. So
18:52
18 minutes, 52 seconds
basically, the longer the session, the lazier and sloppier Claude gets. I know we know this, but that stat really makes it stick. Okay, stat two. One user went
19:00
19 minutes
from spending $345 bucks a month on tokens to $42,000 a month. And the output quality stayed completely flat.
19:08
19 minutes, 8 seconds
So, same work, same result, but because of the token habits, I don't know what happened to this poor guy, but the cost increased so so much and the quality
19:16
19 minutes, 16 seconds
didn't even bump up. So, bad context management. Stat three, the retrieval accuracy thing that I mentioned earlier.
19:23
19 minutes, 23 seconds
92% at 256k tokens drops to 78% at 1 million. So just because you can fill a million tokens doesn't mean that you
19:30
19 minutes, 30 seconds
ever should. Which leads very nicely into the next point about why I barely use it. So when people hear 1 million,
19:37
19 minutes, 37 seconds
they think that they have a million tokens to play with and then they start getting wasteful. They stop using sub aents. They stop being intentional. They offload everything into one giant session because they think they have
19:45
19 minutes, 45 seconds
room and because the progress bar, you know, depending on where you use cloud code, is only halfway. So I might as well just keep going. But the rules of how AI models work have not changed.
19:55
19 minutes, 55 seconds
Bigger window doesn't mean better output. It just means more room for context rot and the more room for the model to get distracted and more room for, you know, all this kind of stuff.
20:03
20 minutes, 3 seconds
That 1 million is just insurance. It's not a goal to fill it at all. Really,
20:07
20 minutes, 7 seconds
the first like, you know, 0 to 20% of your session is prime time. And that's when the cloudmd is the freshest. That's when the model is the most primed. When
20:15
20 minutes, 15 seconds
I use Opus with a million context, I never ever go above like 120k tokens or about 12%. And that's not necessarily
20:23
20 minutes, 23 seconds
because if you get to 200k, it's going to be horrible. It's just because like in my mind, I told myself, "Okay, 120K,
20:29
20 minutes, 29 seconds
that's my number. I'm going to get in the habit of always just clearing and just get in this habit of, you know,
20:33
20 minutes, 33 seconds
storing things and having tracker sheets and just doing all these best practices so that I know I'm always just handling my session well." And by the way, on this whole 120K token thing, I mean,
20:44
20 minutes, 44 seconds
take it a little bit with a grain of salt because what's going to happen is there might be times when you're working on a big coding project or you're, you know, using hyperframes to edit a video
20:52
20 minutes, 52 seconds
and you're going to go past 120 and you don't want to stop at midun because it's in the middle of outputting a bunch of tokens. But to me, that's just kind of
20:59
20 minutes, 59 seconds
my baseline. And if you guys are wondering where I got that, it's because when we only had 200,000 tokens in the context window, I was basically always
21:08
21 minutes, 8 seconds
clearing and compacting. when I got to about 60% which was about 120,000 tokens. So I've always just kind of kept that as the baseline of when I get to
21:16
21 minutes, 16 seconds
that point, I'm going to try to do what I can to reset, write back memories,
21:21
21 minutes, 21 seconds
write back progress, and then keep going on a fresh model. You can also do things like session chaining. So if you have a big project, you don't have to do everything in one session. Chain them
21:29
21 minutes, 29 seconds
together. Have one for discovery where you can have Claude read through PDFs and read through the codebase and, you know, just give you a nice summary doc.
21:36
21 minutes, 36 seconds
And then you can move all of that information into a planning session where it reads that and it creates a plan. And then you take that finished plan and you move that into your
21:44
21 minutes, 44 seconds
execution session. So I think you guys get the point. It's kind of like an assembly line. Each session has a specialized task. So like I said, it's really just important to start building
21:52
21 minutes, 52 seconds
these habits. So if you're just starting out, maybe just stick with the 200k context window for a little bit. Learn the discipline, learn how to be intentional, and then you can graduate
22:01
22 minutes, 1 second
to 1 million if you even need it. You might even realize that you don't even need it. Because I think that the more space you have, it just invites worse habits. Like if you're trying to lose
22:08
22 minutes, 8 seconds
weight, but you always have cookies sitting on your desk. You're just going to be tempted all the time to grab more cookies. So why not just throw the cookies away if you don't need them?
Chapter 8: 10 Frameworks to Save Tokens
22:16
22 minutes, 16 seconds
Now, there are also lots of other frameworks that other people have already figured out that you can just put into your project. So I'm going to link this tweet in the description of
22:24
22 minutes, 24 seconds
this video. It's got 10 different GitHub repos to spend 60 to 90% less tokens in Claude Code. I'm not going to go over all of these here. I'm going to run through them real quick. But what's
22:32
22 minutes, 32 seconds
important to keep in mind is it's not like you want to put all 10 of these into a project and just let it run because that's not really going to work.
22:39
22 minutes, 39 seconds
Each one of these does a different thing. They they they tackle context management and token reduction in different ways. So the key is analyze
22:47
22 minutes, 47 seconds
them, maybe even feed them all into your project and say, "Hey, based on what we're doing here in this specific project with this specific end goal,
22:54
22 minutes, 54 seconds
which one of these repos would probably help us out the most?" Now, if any of these seem particularly interesting to you guys, let me know in the comments and I'll make a full deep dive tutorial
23:02
23 minutes, 2 seconds
on it. But for now, let's just take a look real quick. We have Rust token killer, which is a CLI proxy that filters terminal output before it hits your context. We have context mode,
23:11
23 minutes, 11 seconds
which sandboxes raw tool output into SQL light instead of dumping it into the context. So, we've seen some really nice statistics here with context mode. We've
23:19
23 minutes, 19 seconds
got code review graph. We have token savior. Here's the caveman one that I was talking about that makes Claude talk like a caveman. We've got cloud token
23:27
23 minutes, 27 seconds
efficient which is one cloud denmd file that keeps responses tur. We've got token optimizer MCP. We've got claw token optimizer another token optimizer
23:35
23 minutes, 35 seconds
and claude context. So once again you don't need all 10. Pick two or three based on your workflow. Here's some little bit of a decision tree or some
23:43
23 minutes, 43 seconds
guidelines on how to use them. But like I said, the best way to do it is give Claude Code these repos and have it explain in natural language what each
23:52
23 minutes, 52 seconds
one's doing and which one would fit your specific project best. So let me know if you guys want me to deep dive on any of those, but I thought this would be a cool resource to check out. The link
Chapter 9: Final Thoughts
24:00
24 minutes
will be in the description of this YouTube video. And the last thing I wanted to leave you guys with is if you have a bad session, if you feel like Claude's gone off the rails, but maybe
24:08
24 minutes, 8 seconds
you're not even, you know, near that context rot sort of area, but you're just feeling like you're repeating things or whatever, just clear it or
24:15
24 minutes, 15 seconds
just open up a new one. Just sometimes just open up a new one and just start fresh. Both for your sanity, but also for that clawed session sanity. So that is what I've got for you guys today on
24:24
24 minutes, 24 seconds
managing your session limits better than 99% of people using claude code. If you do these things consistently, I guarantee you, you will get more out of your Claude Code subscription than a lot
24:33
24 minutes, 33 seconds
of people will. So, now I think you're ready to dive deeper into those 18 hacks that I've talked about, and you can do so by watching this video that I will put right up here. And I hope to see you
24:41
24 minutes, 41 seconds
guys over there. But if you enjoyed this one and you learned something new,
24:43
24 minutes, 43 seconds
please give it a like. It helps me out a ton. And as always, I appreciate you guys made it to the end of the video and I will see you in the next
Quick Tip for New PC Builders
10M views
