---
geometry: margin=0.75in
fontsize: 11pt
mainfont: Helvetica Neue
---
Reviewers' comments:
## Reviewer #1

*This is a very well written and interesting paper. I have a few concerns that the authors need to address:*

#### 1) Throughout the paper the authors misuse the term avidity. Avidity is the overall binding strength of a multivalent molecule and is distinguished from affinity, which is the strength of binding for a single site. Generally, avidity has the same units as affinity. Old papers by Fred Karush made the distinction between affinity and avidity very clear and simply Googling avidity will make this all clear.

Thank you for pointing out this oversight. We have corrected the text throughout.
TODO: Finish looking through for this.

#### 2) In most places in the text where the authors say avidity the correct term would be valence, average valence or effective valence. TNP-4-BSA does not have an avidity of 4, rather it has a valence (or average valence) of 4. This is somewhat more complex in the current study where the distribution of valences are measured. Also, I am somewhat concerned about the effective valences that were measured and shown in Fig. 2G. The term effective valence was introduced in Perelson Math Biosci 53: 1-39 (1981) in which binding of multivalent ligands to cell surface receptors was modeled. This paper should be cited by the authors, but argues that if one has a molecule say with n TNPs then after the first one binds to a cell surface some of the remaining n-1 TNPs may not have access to cell surface receptors - see Fig 1 in the cited paper. The effective valence f was then defined as the number of function groups, TNPs, that could simultaneously bind cell surface receptors, with f less than or equal to n. Here the authors find f >n, which make me believe their original molecules, TNP-4-BSA and TNP-26-BSA have on average more than 4 and 26 TNPs per molecule and should be renamed. Also, when they estimated the effective valence of TNP-26-BSA they assumed an upper bound of 32 TNPs, but as Fig 2G shows this upper bound needs to be increased and the calculations redone.

We have remove bounds on the effective valence of each TNP-BSA ligand, and corrected the terminology throughout.

Indeed, we observe an effective valence for each molecule higher than the 
TODO: Finish.

#### 3) In the definition of the A/I ratio it was unclear if this is the ratio of the highest affinity activating receptor to the highest affinity inhibitory receptor as the wording is unclear.

We have adjusted the wording for this in the text to hopefully clarify this definition.

#### 4) For Fig. 3A add a definition of the symbol f to the caption.

We have clarified this in the figure.

#### 5) An analysis of the base model appears in Perelson (1981) and an explicit formula is given for what the authors call R_multi. Generalizations of the base model where all the crosslinking constants are different also appear in this paper, which should be cited here.

We have added this reference, as this is indeed very relevant.

#### 6) In the discussion of the base model the authors when they mention before Eq. (3) the number of unbound receptors or the total number of ligands (NOT LIGAND) bound at equilibrium they mean number per cell and they should be clearer about this. The same applies when the generalized multireceptor model is introduced. Also, the authors should note that Perelson and C.A. Macken wrote a monograph entitled "Branching Processes applied to Cell Surface Aggregation Phenomena". Lecture Notes in Biomathematics, vol 58, Springer 1985 that shows how one can use branching processes to solve these more complex models.


TODO: Fix all ligand/ligands


#### 7) In defining the activity index the authors assume all activating (inhibitory) receptors have the same activity and that activities are additive. Is there any biological support for these assumptions?

We do make this assumption. Notably, we show this assumption largely recapitulates features of the A/I ratio successfully used before, and is better able to predict *in vivo* response in particular cases where the two metrics diverge. There is not detailed evidence for the relative role of individual FcgRs when activated in combination, and we believe this to be an exciting area of inuiry outside the scope of the current study. 

FcgR effector function is signaled through the ITIM and ITAM domains of the receptors. These domains are quite similar between receptors, suggesting that the receptors may be considered interchangable in their intracellular signaling. Additionally, in the absence of evidence to the contrary, we maintain that this assumption of additivity is most parsimonious.


## Reviewer #2

*Effector function of antibodies depends on FcγR class, IgG-FcγR affinity and immune complex valency. The description and prediction of effectiveness of natural or engineered IgG are complicated, due to lack of experimental and mathematics models. In this study, Dr. Meyer and colleagues showed a unique model of multivalent receptor-immune complex. Moreover, this model could make specific predictions about the responses of immune complex with defined FcγRs. Though it is not surprising that this model could be applied in accounting for the immune complex-FcγR binding, it is worthy and interesting to explore the more complicated IgG-effector function by further improving this method. This study will be helpful for developing new concept of therapeutic antibodies/regimens for cancer and autoimmune diseases and for understanding the mechanism of immune-complex induced immune responses.*

Concerns:

#### 1. There is no description for Fig.3E in the text.

We have added this to the relevant point in the text.

#### 2. The definition of effectiveness in Fig.4C is not clear.



#### 3. The IgG effector function is complicated. ADCC or ADCP is not the only pathway for tumor regression in some instance. Is this model limited to accounting for IgG mediated ADCC or ADCP effect in this manuscript？

Indeed, effector function is a complex mix of processes, including ADCC, ADCP, and CDC. Our model only uses the affinity of each antibody species to determine the efficacy of a treatment. Therefore, we are assuming that other contributory factors, such as binding to C1q, have a constant or relatively lesser contribution. This assumption is supported by XXX for the *in vivo* model used here.

#### 4. The author should provide more information about how to calculate the predicted effectiveness of mIgG in Fig.4C and the predicted effectiveness quantified by activity index in Fig.4F.



#### 5. Some of the reagents or methods are not described clearly in detail, such as the construction of TRP1(TA99) antibodies with different mIgG constant region and the method of melanoma lung metastasis model.

TODO: Add
