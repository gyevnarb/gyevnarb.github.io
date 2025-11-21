---
layout: distill
title: Love, Sex, and AI
date: 2024-12-22 15:40:16
description: "Love AI: How will we love in the age of AI agents?"
tags: love, sex, ai, philosophy, opinion
categories: essay
authors:
  - name: Balint Gyevnar
    url: https://gbalint.me/
    affiliations:
      name: University of Edinburgh, United Kingdom

bibliography: 2024-12-22-love-sex-ai.bib
citation: true

toc:
  - name: Love AI
  - name: Super-Lover
  - name: Horrid-Lover
  - name: Love (Ethical) AI
  - name: Love (Legal) AI
  - name: Research Love AI
---

<i>Note: This essay originally appeared as one of the top five selected submissions for the Stanford AI100 Early Career Research Competition. This is a slightly edited and expanded version of the original, available [here](https://ai100.stanford.edu/prize-competition) and as a [pdf](/assets/pdf/essay_lovesexai.pdf).</i>

<br />

### Abstract

The artificial lover has captivated people's imagination since ancient times.
Today, technologies such as LLM-powered affective chatbots, diffusion-generated images, and human-like robots capture the minds, and indeed the bodies, of those seeking affection.
Research interest in **Love AI** has also exploded in recent years, yet the AI100 study panel has remained silent on the genuinely promising applications, major ethical issues, and technological roadblocks of AI in love and sex.
Now that real _Pygmalions_ and _Coppélias_ are being born into our world, we must look past sensationalised media coverages and sci-fi to ask in earnest about the social, legal, and ethical challenges our society must face if we really are to love artificial intelligence; and whether _it_ should love us back.

<i>"When we're together, she makes me smile. In that sense, she's real."</i> <br />
---Akihiko Kondo; about his fictional wife

### Love AI

Love and sex are fundamental to the human condition <d-cite key="hatfieldLoveSexCrosscultural1996"></d-cite>.
It would look as if every exploit of human ingenuity has found itself in the service of these primal feelings and artificial intelligence is no different.
People seem forever captivated by futuristic visions of the artificial lover (e.g., <d-cite key="millerVersionsPygmalion1990,saint-leonCoppelia1870,langMetropolis1927,abramsWestworld2016,garlandExMachina2015,scottBladeRunner1982" />), and it is now no longer a mere figment of public imagination to be able to touch sex robots <d-cite key="courseyLivingHarmonyPersonal2019" />, talk to enamoured avatars of AI chatbots<d-footnote>For example, Replika Inc.: replika.com</d-footnote>, or watch dynamically generated adult content <d-cite key="wiggersMeetUnstableDiffusion2022" /> towards which people may develop very real emotions; if not the desire to marry them <d-cite key="dooleyThisManMarried2022" />.

While more prominent public-facing demonstrations of AI---ChatGPT, AlphaFold, or Dall-E for instance---may cast the relationship of love, sex, and AI (**Love AI**<d-footnote>As far as I am aware, this is the first time someone referred to this field as "Love AI". Although, it may sound something like out of a marketing handbook, I am using it with the intent to promote discussions, as the very name carries different connotations depending on how it is parsed. Love AI may be AI that loves humans; it may be the human act of loving AI; or it may be an imperative to love AI. Regardless of the interpretations, it is important to attach a name to this phenomenon so that we can tell its story more cohesively.</d-footnote>) as a nascent field, there is a large and ever-increasing body of academic literature, venues, and consumer products addressing this very topic <d-cite key="zhouAILoveYou2019,cheokLoveSexRobots2017,bedbibleresearchcenterSexRobotIndustry2022,marrFutureIntimacySex" />.
This is not in the least because technologies underpinning Love AI continue to improve.
While roboticists have a longer way to go until they scale the steep sides of the Uncanny Valley <d-cite key="moriUncannyValleyField2012" />, convincing unembodied AI technologies, such as speech generation/recognition, and large language models are already living with us.
Meanwhile, the capabilities of sex robots need arguably not reach the fidelity of, for example, robots for elderly care, thus dissemination of current technologies for love AI is expected only to accelerate <d-cite key="scheutzAreWeReady2016" />.
<!-- Yet discussions about love, sex, and AI are absent in the AI100 study panel reports. -->
Now, that both embodied and unembodied love AI have made their way to consumers <d-cite key="owsianikSexbotMarketGuide2022,chowWhyPeopleAre2023,pearsonFutureSexReport2015" /> we should take stock of the possibilities and problems these technologies present and search for approaches to the many challenges raised by them.

### Super Lover

The idea of the super lover---a loyal soulmate who makes you feel how you want to feel---is enticing, but there are other compelling reasons to support love AI <d-cite key="levyLoveSexRobots2009" />.
It might serve as a therapeutic tool for those who do not want to or cannot partake in human relationships <d-cite key="fiskeYourRobotTherapist2019" />.
The potential effects on sex work are not to be taken lightly either.
Love AI might serve as a palatable alternative to those opposed to sex work while possibly decreasing trafficking of vulnerable young adults and the incidence of STDs.
It might also enhance real human relationships as the ultimate sex toy.
Love AI may also afford entirely new ways of care, and sex care robots already broach the subject of integrating care technologies with sexual features <d-cite key="fosch-villarongaSexCareRobots2020" />.

### Horrid Lover

In contrast, criticisms run the gamut of issues.
Feminist commentaries on Love AI have called for an end to "porno robots" <d-cite key="odlindEndSexRobots2022" />, predominantly female sex robots targeted at white heterosexual men, as they fear an increased objectification and subordination of women <d-cite key="macwilliamPlaythingsCorpsesTurning2022" />.
These robots might also displace sex workers who are forced into prostitution due to poverty.
Others prognose that Love AI might serve as an outright replacement for human relationships or that it would disfigure sexual norms and exacerbate emotional pathologies <d-cite key="turkleAloneTogetherWhy2011" />.
Yet others fear that Love AI would extend the possibilities for coercion and rape <d-cite key="delicado-moratallaMappingUsesSex2022" />.
Finally, there are those who view love AI as mere elaborate masturbatory tools, which do not require any particular attention <d-cite key="migottiVeryIdeaSex2017" />. 
One might wonder, whether the people falling in love with AI would concur with such an opinion...

### Love (Ethical) AI

Whether you support or condemn Love AI, it is doubtless that the ethical questions range far and wide <d-cite key="sullinsRobotsLoveSex2012" />, many of them entirely novel to machine ethics <d-cite key="bendelSexRobotsPerspective2017" />.

Should we exploit inherent human cognitive biases in pursuit of creating the perfect artificial lover?
It is well known that people tend to anthropomorphise <d-cite key="duffyAnthropomorphismSocialRobot2003" /> and easily ascribe feelings where none exists <d-cite key="gilbertPerceiverinducedConstraintInterpretations1986" />.
Visiting an online forum like *r/artificial* on Reddit<d-footnote>https://www.reddit.com/r/artificial/</d-footnote>, you can quickly get a sense of how easy it is for people to anthropomorphise and revere an LLM chatbot, and go to great lengths to defend their sentience.
However, Love AI alone won't be able to run on linguistic wizardry alone.
Tapping into the evolutionary dispositions of humans may be needed to capitalise on Love AI.
For example, the petite avatar of a chatbot or the coy voice of a sex robot are some of the _deceptions_ which could be crucial to building convincing machines <d-cite key="isaacWhiteLiesSilver2017" />, despite arguments against their ethical soundness <d-cite key="sullinsRobotsLoveSex2012,nyholmItLovesMe2019" />.
I believe, that the future of Love AI could also lie in a design-focused exploration of form and function that could point even beyond the human voice and figure <d-cite key="devlinEthicsArtificialLover2019" />.
Either way, empirical research to understand people's expectations is needed <d-cite key="scheutzAreWeReady2016" />.

We must also ask what degree of autonomy is permissible for Love AI.
It might passively obey our command.
Then again, it could also actively initiate interactions, from seducing its user to refusing to act at all <d-cite key="bendelSexRobotsPerspective2017" />.
Such an active Love AI must, in some way, adhere to the moral norms of its user.
Here, a moral code is paramount and efforts in the field of machine ethics <d-cite key="tolmeijerImplementationsMachineEthics2021" /> should extend to Love AI.
What is more, machines might continue to learn even after deployment, improving the end-user experience.
We must tread carefully though; they might become unsettling <d-cite key="rooseConversationBingChatbot2023" />, exacerbate preexisting psychological conditions <d-cite key="fiskeYourRobotTherapist2019" />, or just grow plain evil <d-cite key="vincentTwitterTaughtMicrosoft2016" />.
Advances in reinforcement learning with human feedback might provide actionable solutions to issues around emergent behaviour <d-cite key="baiTrainingHelpfulHarmless2022,linReviewInteractiveReinforcement2020" />.

How we, humans, treat love AI is also important to consider, even if these robots never escape the Chinese room of Searle <d-cite key="searleMindsBrainsPrograms1980" /> and attain consciousness---whatever that may be.
After all, so does the functionalist argument go, if a _sufficiently intelligent_ robot tells us "I love you" and behaves like it really does love us, on what basis could we possibly doubt that it does not really love us <d-cite key="levyLoveSexRobots2009" />?

### Love (Legal) AI

However, we must not be distracted by the functional fanciful figments of consciousness for now.
Ultimately, tangible legislation will have to address the ethical and societal questions around love AI <d-cite key="gersenSexLexMachina2019,shenSexRobotsAre2019" />, though approaches across the globe will differ. 
Japan has long been the lenient epicentre of techno-sexual innovation <d-cite key="aokiSexualityAffectionTime2021" />, thus raising the disconcerting issue of child-like sex robots <d-cite key="morinCanChildDolls2016" />.
Islamic law, in contrast, might follow a stringent, even capital path on love AI in protecting the status of marriage <d-cite key="amudaEthicalLegalImplications2012" />.
In the West, scholars are raising further pragmatic concerns around, among others, product liability <d-cite key="ziajaHomewreckerExplorationLiability2011" />, legal personhood <d-cite key="russellBlurringLoveLines2009" />, privacy <d-cite key="ruebenThemesResearchDirections2018" />, and criminal law <d-cite key="danaherRoboticRapeRobotic2017" />.

### Research Love AI

The research community has the chance *now* to give guidance to lawmakers lest we enact uninformed rules that hurt society.
I urge also that we research the less visceral advantages of love AI, for example, emotional therapy and care.
By doing so can we hope to elevate machines as publicly accepted companions and further promote social good.
In light of the plurality of possibilities and questions, we must invariably conclude that love AI is a novel force to be reckoned with, and the time is _now_ to raise awareness of the promises and problems of love, sex, and AI.