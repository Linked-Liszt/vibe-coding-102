# Preface

Author's note: The live presentation was a little rushed, both since the event was running behind and just being on stage. Here's some more detailed notes from the presentation. 

The slides are accessible internally via the event box folder, or the link posted in the slack chat.

# Notes

### Slide 1: Title
* 102: this is a step beyond just vibe coding
* Here to make vibe coding boring (with engineering principals)
* Explore some ideas into how to more rigorously this into our day-to-day work.

### Slide 2: Tutorial Link
* Slide is self-descriptive

### Slide 3: Background
* Quick background so you know where I'm coming from.

* Split background – SWE & ML research. Intersection between EC and deep learning

* Been tracking this technology for a while. Largely unimpressed until Claude 3.7

* Deliberately used heavily for this presentation. People who haven't talked to me in a while might be surprised at how quickly my mind has changed on the topic.


### Slide 4: Anthropic Survey

* Graph from Anthropic showing Claude usage vs representation in US workforce
* Wear a lot of hats at ANL but today I'll be wearing my SWE hat.
* SWE is an interesting place to be right now as the first real profession to adopt these tools.
* Secondary fields in content creation, sciences, and education

### Slide 5: Tooling Considerations
* Very much a believer of the tools depend on the job.

* General recommendations when it comes to tooling

* Using the latest models is a must. We'll come back to this later in the presentation

* Agentic capabilities are required at a minimum. (Likely will be demonstrated in previous talk)

* Direct integrations are nice to have, but the LLM is competent at bash and could call tools directly via CLI.
* Field is moving quickly. Anticipate tools will change dramatically in the next 6-12 months. Don't get too attached. 

### Slide 6: A Note on Vibe Coding

* Most people define vibe coding now as specifically not reading/understanding the output code.

* Don't let this presentation scare you away from vibe coding.

* Vibe coding is a powerful paradigm. Especially if you are a non programmer, domain scientist, admin/leadership etc.

### Slide 7: Section Break: Building Software with LLM Assistance
* Getting into the core of the talk.

* How do we more deeply integrate this new technology into our day-to-day work?

* Building engineering practices around tthis technology.

* How do we go beyond vibe-coding?

### Slide 8: Why Vibe Coding is Bad at Engineering
* Tech debt is a good angle to lens to view the effect of vibe coding

* To try to categorize some concrete examples of tech debt that’s produced by using these tools

### Slide 9: Paradigms
* I’d like people to think of this as a separate paradigm.

* There are multiple ways to use these tools and both are appropriate for different situations

* Closet analogy to the one I want to introduce is to pair programming

* You probably already do this while vibe-coding, especially if you are a programmer

### Slide 10: Keep a Tight Loop
* How can we make this process easier on each other

* Just like you want to keep PR’s small it’s good to keep LLM changes small. It’s easier to review

* Will justify solve rates later

* Allows you to be in more control of the architecture and design.

### Slide 11: Some Data to Back This Up
* Measure of human time taken to solve a benchmark compared to success rate

* Focus on the left graph first: Notice the steep drop-off after a few minutes.

* I like to operate around here (5-15m) as the models generally have a higher success rate.

* Humans have a drop-off but it's nowhere near as steep.
* Secondary, want to highlight the difference between the frontier and older models, the model on the right. 

### Side 12: Module 1
* Slide is self-descriptive 

### Slide 13: Controlling the Context
* Models fail at DRY often due to context issues. 
* Will happily reimplement code it is not aware of
* Accuracy is much more valuable than the token cost of adding more context
* Some academic literature about "context rot" but often better to go over than under

### Slide 14: Agents.MD Files
* A technique that has been settled on by multiple providers. 
* Let the agents.md files evolve with the project. 
* Example of a mature agents.md file: https://github.com/julep-ai/julep/blob/main/AGENTS.md

### Slide 15: Module 2: Context
* Slide is self-descriptive 

### Slide 16: Section Break: Non-Generative Tasks
* Something that's often underrated 
* Could mention self-improvement/learning in the age of LLMs

### Slide 17: Code Review
* Missed being able to do code review from a corporate environment 
* A second pair of eyes is always nice to have, even if they are LLM eyes
* Catches mistakes AND helps you learn
* Can adjust the review depending on what you want out of it via prompting


### Slide 18: Reading Code
* Reading code you didn't write is one of the more challenging and time-consuming tasks of the job. 
* LLMs are VERY good at this. Original NLP tasks involve QA/summary/sentiment analysis before big models hit the scene

### Slide 19: Module 3
* Slide is self-descriptive 


### Slide 20: Section Break: Assorted Notes
* Going to be going fast

### Slide 21: Infrastructure
* Collaborative infra has always had value
* In the age of agents, the value proposition is much higher
* Apply it to small projects you wouldn't have before
* "You'll never be a solo developer again"

### Slide 22: Ecosystem
* Fun to use the latest and greatest, but "boring" tools work best for LLMs. 
* See the Gemini CLI system prompt for a concrete example: https://github.com/google-gemini/gemini-cli/blob/2096f971cd57a2a1d5d8fb5438be1ea77b01f3c6/packages/core/src/core/prompts.ts#L70 

### Slide 23: Tests
* Seen some strong opinions in this area
* Use your judgement when it comes to allowing or disallowing LLMs from writing tests. 
* Haven't had the opportunity to try out TDD, but could be interesting in this space

### Slide 24: Further Reading
* Lot more opinions here than I can fit into a 30m presentation

* Many senior engineers trying to fit these tools into their work all across the world.

* Worth seeing their initial opinions & also reading the opinions of the people who don't like this technology.

### Slide 25: Section Break: The Future
* Field is changing fast
* Will undermine a lot of what I've presented on assuming trends hold

### Slide 26: Room to Grow: Technicals
* Want to make the case that it's likely that this tech will improve soon
* Compute, algorithmic improvements
* Lots of low-hanging fruit, especially when it comes to scaling up many of these techniques

### Slide 27: Room to Grow: Motivation 
* Arguably, just as important as the technicals, the companies in this are are strongly motivated to keep pushing at programming and research itself. 
* Not quite a coincidence that we are the first field that this tech is applicable to. 
* Lots of interesting work in the world of automating research itself. See the paper corner for some works in this area. 

### Slide 28: Current Trends in Improvement
* Headline results from the previously cited study.

* Doubling time of 7 months, 4 months for reasoning models

* We may soon have models capable of doing 2h, 4h of work with decent success rates.

* How may tooling change under these conditions? I anticipate a lot.

### Slide 29: LLM Usage Paradigms 2
* If you noticed a suspiciously shaped white-space good on you!

* Third paradigm, the agentic contributer.

### Slide 30: Key Features of Agentic Contributors
* Productivity gains will come mostly from parallelism.
* Right now a strong programmer may not get much benefit by the current process of babysitting a single agent but parallelism changes everything
* Would look a lot like being a repo maintainer with agents contributing instead of users

### Slide 31: Tooling in the Future
* I didn't entirely come up with these predictions.

* These tools already exist.

* Google: Unified UI for rapid context switching. Launches jobs in containers on the cloud.

* Microsoft: Building UI directly into Github. Assign the copilot agent directly to issues.

* Would recommend checking out Google. Free while in beta and have heard US folks get into beta pretty quickly.

### Slide 32: Closing Thoughts
* Whirlwind of a talk
* The mental levers of our time. Little amount of force for a lot of leverage.
* Good time to be thinking big
* Pose to the audience: What would you solve with these tools
