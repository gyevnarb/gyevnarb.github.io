---
layout: distill
title: Mathematical Understanding and Artificial Intelligence
date: 2025-11-10 15:40:16
description: "Thoughts and notes from the workshop on the Cognitive Science of Mathematical Understanding"
tags: math, philosophy, cognitive-science, ai
categories: conference-notes
authors:
  - name: Bálint Gyevnár
    url: https://gbalint.me/
    affiliations:
      name: Carnegie Mellon University, Pittsburgh, PA, USA

bibliography: 2025-11-17-math-understand-cogsci.bib
citation: true

toc:
  - name: Knowledge
  - name: Linking
  - name: Intuition
  - name: Externalization
  - name: Aesthetics
  - name: Understanding
---

<!-- <i>This post is a summary of my notes and thoughts after attending the workshop on the Cognitive Science of Mathematical Understanding organized by [Tania Lombrozo](https://www.tanialombrozo.com/) of Princeton University and [Akshay Venkatesh](https://www.math.ias.edu/~akshay/) of the Institute of Advanced Study.</i> -->

<blockquote class="epigraph">
    <div class="epigraph-title">Sneaking around ∞</div>
    <p>
    <i>Dedekind’s idea of infinite sets:</i> <br />
    if you’re one of them you’re simply a set<br />
    admitting 1-to-1 correspondence <br />
    with—wait:— a <i>proper</i> subset <br />
    of yourself!. . . you’re a snake <br />
    that can gobble a snake your size <br />
    with room left over besides. . . <br />
    not worrying that in your meal <br />
    yet another same size snake resides; <br />
    stream upon stream <br />
    of <i>mise en abîme.</i>
    </p>
    <footer>— Barry Mazur; November 5, 2025<d-footnote>As we shall see, thinking about mathematical understanding is much like thinking about infinite sets. A question that requires thinking about questions which require thinking about questions, and so on, until…, we find ourselves rethinking mathematical understanding again.</d-footnote></footer>
</blockquote>

### Knowledge

What does it mean to understand mathematics?

Maybe mathematical understanding is having factual knowledge of mathematical concepts.

Well, that could hardly be <i>it</i>.
As [Bethany Rittle-Johnson](https://www.vanderbilt.edu/psychological_sciences/bio/bethany-rittle-johnson) explained, very young children may know the number words from "one" to "five", but when asked for five coins, they fail to understand the concept of size (i.e. cardinality of a set)<d-cite key="frye1989YoungChildrens" />. In another example, students who had only seen the "equals sign" in expressions such as "5 + 3 = __" thought that they know what the "equals sign" represented, but then failed to answer questions such as “5 + 3 = 2 + __”, thinking that the "equals sign" stood for a sum<d-cite key="rittle-johnson1999ConceptualProcedural" />.

There is an interesting tension in these examples, and more broadly in maths education, so argued [Keith Weber](https://gse.rutgers.edu/faculty/keith-weber/), between reconciling the internal representations we have of concepts (e.g. the relationship between number words and cardinality) with the external, institutional representations imposed on us (e.g. the ways the “equals sign” <i>should</i> be interpreted)<d-cite key="dawkins2017ValuesNorms" />. For maths education, metaphors are of great use here. For example, a proof is a hike through the forest and sets are containers. This may be why, asking mathematicians Akshay Venkatesh and Barry Mazur about the most important aspects of their work, they replied with “examples and analogies”.

Such an internal-external representational conflict is one we also often see in artificial intelligence (AI). The reason a large language model (LLM) cannot answer the question <i>"How many Rs are there in the word strawberry?"</i><d-footnote>AIs on Rs in "strawberry": <a href="https://languagelog.ldc.upenn.edu/nll/?p=65667">https://languagelog.ldc.upenn.edu/nll/?p=65667</a></d-footnote> is (roughly) because LLMs operate on “token-language” not English. Similarly, if you ask an LLM to read a clock, it fails miserably<d-cite key="saxena2025LostTime" />, not because it doesn’t have a representation of temporal concepts, but because those concepts do not seem to be connected to the external structure of a clock. On the other hand, in both maths education and with LLMs, the practice of self-reflection or self-explanation has been shown to improve conceptual understanding.<d-cite key="rittle2006promoting,ji2023towards" /><d-footnote>Although this can backfire with LLMs. If you ask ChatGPT <i>"Is there a seahorse emoji?"</i> you can see the cascading effects yourself.</d-footnote>

Due to the subtle differences in representations, it is important that we stay mindful of the different ways humans and AI represent concepts.

### Linking

Perhaps mathematical understanding is the ability to generalize and interlink the mathematical concepts we know.

Drawing connections between related concepts can be a source of immense insight: just think of the Langlands Program that drew connections between number theory, geometry, and group representations<d-footnote><a href="https://publications.ias.edu/rpl/section/21">https://publications.ias.edu/rpl/section/21</a></d-footnote>. Although, the way we connect concepts and generalize them can subtly differ.

Why do some people think 400 is more even than 326?<d-cite key="dehaene1993MentalRepresentation" /> Why do non-mathematicians think that an equilateral triangle is more “triangle-y” than a common one?<d-cite key="feldman2000BiasRegular" /> And why do mathematicians think the other way around?<d-footnote>This was a remark made by one of the mathematicians in the room at the workshop.</d-footnote> This graded nature of concepts, argued [Marina Dubova](https://www.mdubova.com/), may be because concepts are fluid and context-dependent. Case in point, when people were asked in an experiment to come up with concepts where none exists (by design), they readily made up ad-hoc concepts<d-cite key="little2006AdHoc" />. So it might be very tricky to know a priori about mathematical concepts whether they are novel or useful, rather than just being a result of our tendency to group things. This is also why linking concepts may be so useful: if one concept can be translated to another then, presumably, the original concept had some useful meaning to begin with.

Curiously, when I prompted ChatGPT <i>"Is 400 more even than 326?"</i> it gave a very definite <i>"No."</i> as an answer. Similarly, for the example of triangles. Of course, in either case, the LLM is mathematically correct, but to me, it seems something useful is lost in the answers’ "definiteness". Going back to which triangle is more triangle-y, one mathematician in the workshop claimed that they always try to draw the least regular triangle when thinking about just any triangle. To mathematicians, it seems attaching additional properties (e.g. symmetry) to a concept may be a dangerous distraction that could lead down garden paths. It may seem drawing connections between concepts is not always helpful.

On the other hand, LLMs also seem ready to find ad-hoc concepts where none exists. I asked ChatGPT to group a bunch of random words I just typed out,<d-footnote>These were: cheese, apple, computer, snake, forest, microphone, whiteboard, Hindu, folder.
</d-footnote>and sure enough, it made up some concepts. For example, it grouped {computer, folder, microphone, whiteboard, Apple, snake (Python), forest (random forest in machine learning)} under the concept "computing terms". Now here I am questioning whether I truly just typed out random words to begin with, fitting in nicely with the study of Little et al. <d-cite key="little2006AdHoc" />.

In the end, if we are to use AI in maths, finding the right balance between exploiting these human-like biases versus removing human-like bias from the mathematical research process will be crucial.

### Intuition

It seems mathematical understanding may have to do with having intuitions about a generalizable and connected network of mathematical concepts.

Certainly, this seems important. Knowing intuitively which theorem to apply in a proof without searching through the vast space of all theorems is certainly helpful. So is having an intuition for which theorems can be proven and which are out of reach. However, intuitions aren’t created equal, as explained by [Silvia De Toffoli](https://www.silviadetoffoli.net/).

Some intuitions are plain, as in, they provide an immediate justification to something, but nothing that would reveal why the intuition is true. This is just like having a "bullshit detector" for AI slop. I know intuitively that a video is slop even though I cannot articulate why. So then the second kind of intuition is articulate, which is amenable to epistemic inquiry. Articulate intuition, the one that allows a mathematician to say Theorem X is more “provable” than Theorem Y because of this and that concept, seems much more like mathematical understanding.

Intuition in turn is very related to the ability to actually use our mathematical understanding, as in mathematical inference. As [Jeremy Avigad](https://www.andrew.cmu.edu/user/avigad/) has remarked, I may have all the knowledge of the right mathematical tools and understand their connections, but if I can never apply those tools, or never learn anything from applying those tools, then it feels like I haven’t understood a lot after all. For example, I could have a sense that I understand how one may turn a sphere inside out (i.e. sphere eversion). Maybe a cool animation has even shown how eversion is done, yet I would not be able to tell you why eversion is useful and interesting, or when one could use it to prove something.<d-footnote>This example is not dissimilar from the "3blue1brown effect": that a cool animation leaves you with a sense of understanding that is actually not at all actionable: an illusion of understanding.</d-footnote>

This is a crucial point when it comes to AI. There is a broad recognition in computer science that AI tools are opaque, indecipherable systems. Using these tools repeatedly incurs cognitive debt<d-cite key="lee2025ImpactGenerative" />, and that debt is paid when we need to explain or justify our actions, or wish to build on LLM-generated content. Indeed, communication is a cornerstone of mathematics, as it forces us to externalize our thoughts in an intelligible way. This process, on its own, requires background knowledge about our interlocutors and their knowledge.

### Externalization

So mathematical understanding is having externalizable and intuitive knowledge of generalizable and interconnected concepts?

Well, the way we externalize our knowledge will depend on a range of dimensions about how we can formalize and informalize our thoughts. One such dimension is the degree of constraints imposed by the shared language used between interlocutors. For example, writing a strictly typed formal proof of Fermat’s Last Theorem in Lean4<d-footnote><a href="https://lean-lang.org/use-cases/flt/">https://lean-lang.org/use-cases/flt/</a></d-footnote> has a huge number of constraints: from the syntax of the language to enforcing code compilation. In this case, each communicative action (e.g. writing a line of Lean4 code) bridges only a very small gap in understanding between two interlocutors. On the other hand, two mathematicians arguing in front of a whiteboard filled with to-us-incomprehensible notation may be the most effective exchange of grand ideas. However, this is only made possible by the largely overlapping and immense knowledge of those mathematicians; something that is not required for writing a line of Lean4 code.

<figure>
<img src="https://imgs.xkcd.com/comics/mathematical_symbol_fight.png" alt="XKCD comic depicting increasing more complex mathematical symbols ranked on a numberline from least to most effective in a fight, with stickfigures actually fighting underneath the numberline."/>
<figcaption>XKCD: Mathematical Symbol Fight</figcaption>
</figure>

One might hope here, that LLMs would excel at externalization. After all, their billions of parameters have stored all that the internet can offer in data, so they have the background knowledge. Unfortunately, LLMs are neither great at writing Lean4 code nor communicating complex ideas about proofs. In our preliminary experiments with [Simon DeDeo](https://sites.santafe.edu/~simon/), we compared how mathematicians edit Lean4 code to how LLMs edit the same code, and found that LLMs differ drastically from humans. While humans had more or less stable ontologies keeping the overall proof-dependency structure largely unaltered, LLMs had no qualms about disrupting the structure of a proof by introducing new lemmas or removing existing lines. This raises the important question of how the use of LLMs in mathematical research will steer downstream research.

Fortunately, LLMs don’t write maths unless we ask them to, and even when you ask them, they often simply say: <i>"It can't be done."</i> Just try asking ChatGPT to prove (or provide a next step of) whether $e\pi$ is irrational. It seems to me, that mathematical understanding requires rather a desire to understand, not something AI systems are equipped with. One such desire seems to stem from a sense of aesthetics in maths.

### Aesthetics

Maybe understanding is having externalizable and intuitive knowledge of generalizable and interconnected mathematical concepts in search of beauty.

After all, there is no more intrinsic truth value to Gauss’s pairing proof that $1 + 2 + … + N = N(N+1)/2$ as opposed to a straightforward proof by induction. Similarly, rote application of algebraic manipulations to show that the sum of odd numbers is a square number:

$$\displaylines{(n+1)^2 = n^2 + 2n+1 = (n-1)^2 + 2n-1 +2n+1 = … \\= 1 + 3 + … + 2n-1 + 2n + 1}$$

is equally correct as the below proof without words. So why is it that we each feel one proof may be more beautiful than the other?

<figure>
<img src="/assets/img/grid.png" alt="Grid of alternating odd number of black and white L-shapes that fit into one another producing squares, showing that odd numbers add to square numbers." />
<figcaption>Proof without words of the fact that a 1+3+...+2n+1 add to a square number.</figcaption>
</figure>

When I ask ChatGPT to pick which proof of the formula of the sum of integers (Gauss v. Induction) is more beautiful, it picks what most of us would expect: Gauss’s proof. It appeals to a sense of elegance in noticing a non-trivial pattern; it mentions that the proof uses a "quick, surprising, and deep pattern — the kind of simplicity and insight mathematicians often call beautiful." It also evokes the contrast case of induction, which it refers to as “solid, rigorous, but routine”.

Of course the above qualities are hugely proof dependent. For example, the proof of Fermat’s Last Theorem is anything but quick and surprising, yet there is still much beauty to be found in it. The danger with using AI to make choices for us is to conflate the sycophancy of AI with aesthetic morality, or indeed innate agency. LLM tools are just that: tools that we use in pursuit of our goals.

Maybe there is beauty to be found in using LLMs for maths though. As [Barry Mazur](https://sites.harvard.edu/barry-mazur/) argued, historically much of our mathematical understanding improved when we took our existing set of tools and abstracted shared patterns, thereby opening up new domains for inspection. Perhaps we could understand AI as mathematical tools much like we understand set theory as a tool to talk about collections and their relationships. In turn, we could formulate an abstract theory of LLM-maths, much as category theory abstracts sets and functions into objects and arrows.<d-footnote>It is a pity that so few computer scientists talk to mathematicians. Computer science is currently suffering from a lack of rigor, and often does what one might call “vibe researching”: research that feels correct, is produced quickly, but is flawed. A similarly insidious “vibe proving” phenomenon seems to be at work in mathematics as well (e.g. journals are flooded with incorrect but not crazy looking ideas). I urge that we research how artificial intelligence interacts with and affects our mathematical understanding. This research should play into a broader understanding of the metascience of AI, a research program I will begin to outline in upcoming posts.</d-footnote>

### Understanding

So what <i>is</i> mathematical understanding?

I have dissected the question into yet many more questions, related to knowledge, connections, intuition, externalization, and aesthetics, and I am certain I have missed so many more aspects. For each of these questions, AI systems have a role to play, but it is ever-so-crucial to retain our humanity in doing mathematics. Doing that consciously seems like a grand challenge, and it seems we will have to revisit the question of what is [mathematical understanding](https://gbalint.me/blog/2025/math-understand-cogsci/) year after year, much like a doctor checks up on their patient every year.






