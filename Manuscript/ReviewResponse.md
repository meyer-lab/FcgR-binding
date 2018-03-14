---
geometry: margin=0.75in
fontsize: 11pt
mainfont: Helvetica Neue
---

# Reviewers' comments:

## Reviewer #1

*This is a very well written and interesting paper. I have a few concerns that the authors need to address:*

*1) Throughout the paper the authors misuse the term avidity. Avidity is the overall binding strength of a multivalent molecule and is distinguished from affinity, which is the strength of binding for a single site. Generally, avidity has the same units as affinity. Old papers by Fred Karush made the distinction between affinity and avidity very clear and simply Googling avidity will make this all clear.*

Thank you for pointing out this oversight. We have corrected the text throughout.

*2) In most places in the text where the authors say avidity the correct term would be valence, average valence or effective valence. TNP-4-BSA does not have an avidity of 4, rather it has a valence (or average valence) of 4. This is somewhat more complex in the current study where the distribution of valences are measured. Also, I am somewhat concerned about the effective valences that were measured and shown in Fig. 2G. The term effective valence was introduced in Perelson Math Biosci 53: 1-39 (1981) in which binding of multivalent ligands to cell surface receptors was modeled. This paper should be cited by the authors, but argues that if one has a molecule say with n TNPs then after the first one binds to a cell surface some of the remaining n-1 TNPs may not have access to cell surface receptors - see Fig 1 in the cited paper. The effective valence f was then defined as the number of function groups, TNPs, that could simultaneously bind cell surface receptors, with f less than or equal to n. Here the authors find f > n, which make me believe their original molecules, TNP-4-BSA and TNP-26-BSA have on average more than 4 and 26 TNPs per molecule and should be renamed. Also, when they estimated the effective valence of TNP-26-BSA they assumed an upper bound of 32 TNPs, but as Fig 2G shows this upper bound needs to be increased and the calculations redone.*

We have removed bounds on the effective valence of each TNP-BSA ligand and corrected the terminology throughout.

Indeed, the marginal distribution for effective valence in each case is centered higher than the average valence. Importantly, these are marginal distributions of the posterior distribution after fitting, and so a reflection of our uncertainty in the estimate of these quantities. In the TNP-26-BSA case, f=26 is well within this distribution, and so the fitting is consistent with this as a possible effective valency. In the TNP-4-BSA case, the marginal distribution is shifted upward to such an extent that it does not include f=4. As we mention in the text, these molecules, due to their synthesis technique, will have a (likely Poisson) distribution of valencies. Especially for TNP-4-BSA, the higher valency molecules may preferentially bind.

Our decision to include an effective valency was motivated by Perelson Math Biosci 53: 1-39 (1981) mentioned, and we did expect that the effective valency would be lower due to the effects mentioned here. We have expended discussion of these factors in the text along with reference to this paper.

> Both TNP-4-BSA and TNP-26-BSA showed a preference toward higher effective valency, TNP-4-BSA significantly so ([@Fig:Fit]G). The method for coupling TNP to BSA creates a (likely Poisson) distribution of valencies and so deviation from the average is not surprising. A preference toward higher effective valency than the average is perhaps consistent with our earlier measurements that valency has a potent effect on the level of binding ([@Fig:Binding]).

*3) In the definition of the A/I ratio it was unclear if this is the ratio of the highest affinity activating receptor to the highest affinity inhibitory receptor as the wording is unclear.*

We have adjusted the wording for this in the text to hopefully clarify this definition.

> ...earlier work examining interventions of antibodies with constant variable regions but of differing IgG subclass identified that the ratio of the highest affinity activating receptor $K_a$ to that of the sole inhibitory receptor (A/I ratio) could predict the influence of each intervention.

*4) For Fig. 3A add a definition of the symbol f to the caption.*

We have done this.

*5) An analysis of the base model appears in Perelson (1981) and an explicit formula is given for what the authors call R_multi. Generalizations of the base model where all the crosslinking constants are different also appear in this paper, which should be cited here.*

We have added this reference, as this is indeed very relevant.

*6) In the discussion of the base model the authors when they mention before Eq. (3) the number of unbound receptors or the total number of ligands (NOT LIGAND) bound at equilibrium they mean number per cell and they should be clearer about this. The same applies when the generalized multireceptor model is introduced. Also, the authors should note that Perelson and C.A. Macken wrote a monograph entitled "Branching Processes applied to Cell Surface Aggregation Phenomena". Lecture Notes in Biomathematics, vol 58, Springer 1985 that shows how one can use branching processes to solve these more complex models.*

We have adjusted the text within the methods to clarify the units of these quantities, and fix the use of ligand versus ligands.

Many thanks for pointing out this monograph. While we calculate the probability of all states in this generalized model, we're very interested in building on this work to explore polyclonal antibody combinations. We look forward to applying the methods here.

*7) In defining the activity index the authors assume all activating (inhibitory) receptors have the same activity and that activities are additive. Is there any biological support for these assumptions?*

We do make this assumption. Notably, we show this assumption largely recapitulates features of the A/I ratio successfully used before and is better able to predict *in vivo* response in particular cases where the two metrics diverge. We are not aware of detailed accounting for the relative contribution of individual FcγRs when activated in combination, and we believe this to be an exciting area of inquiry outside the scope of the current study. 

FcγR effector function is signaled through the ITIM and ITAM domains of the receptors. These domains are quite similar in sequence between receptors, supporting that the receptors may be considered interchangeable in their intracellular signaling. Additionally, in the absence of evidence to the contrary, we maintain that assuming additivity is most parsimonious.


## Reviewer #2

*Effector function of antibodies depends on FcγR class, IgG-FcγR affinity and immune complex valency. The description and prediction of effectiveness of natural or engineered IgG are complicated, due to lack of experimental and mathematics models. In this study, Dr. Meyer and colleagues showed a unique model of multivalent receptor-immune complex. Moreover, this model could make specific predictions about the responses of immune complex with defined FcγRs. Though it is not surprising that this model could be applied in accounting for the immune complex-FcγR binding, it is worthy and interesting to explore the more complicated IgG-effector function by further improving this method. This study will be helpful for developing new concept of therapeutic antibodies/regimens for cancer and autoimmune diseases and for understanding the mechanism of immune-complex induced immune responses.*

*Concerns:*

*1. There is no description for Fig.3E in the text.*

We have added this to the relevant point in the text.

*2. The definition of effectiveness in Fig.4C is not clear.*

Effectiveness is defined throughout the manuscript as the fractional reduction in lung metastases (e.g. no reduction is 0.0, while a full reduction in metastases is 1.0). We have adjusted the wording in this figure to emphasize that this definition applies to all the subfigures.

> Effectiveness is the fractional reduction in lung metastases observed with treatment throughout (e.g. no reduction is 0.0, while a full reduction in metastases is 1.0).

*3. The IgG effector function is complicated. ADCC or ADCP is not the only pathway for tumor regression in some instance. Is this model limited to accounting for IgG mediated ADCC or ADCP effect in this manuscript?*

Indeed, effector function is a complex mix of processes, including ADCC, ADCP, and CDC. Our model is only dependent on the affinity of each antibody-FcγR pair to determine the overall ability of an antibody to reduce the ultimate number of lung metastases. Therefore, the model does not distinguish these processes. Separately modeling each individual pathway would require more detailed information regarding the each pathway's engagement by each Fc class.

> Our model is dependent upon FcγR abundance and the quantitative relationship between binding state and cell response; therefore, further refinement of where these receptors are expressed and how they sense IC engagement will improve our ability to study the *in vivo* environment. In particular, effector function is a complex mix of processes, including ADCC, ADCP, and CDC. More detailed information about the activity of each of these processes with each treatment would allow for more narrowly targeted design. The versatility of antibody-based therapies ensure broad applicability of this approach to many diseases in which IgG effector function plays a key role, including the design of therapeutic antibodies for the treatment of infectious disease, autoimmune disorders, and other cancers. 

*4. The author should provide more information about how to calculate the predicted effectiveness of mIgG in Fig.4C and the predicted effectiveness quantified by activity index in Fig.4F.*

We have added additional discussion of how this is done within the methods text describing this figure.

> Regression against *in vivo* effectiveness of mIgG treatments was performed by non-linear least-squares (`scipy.optimize.least_squares`). Association constants for all combinations of mIgG and mFcγR were obtained from previous experimental measurements. Each effectiveness was represented as the percent reduction in the number of lung metastases quantified. Using an assumed ligand concentration and valency, as well as mFcγR expression, activities of each cell population were calculated using the multi-receptor model as independent variables. To account for the limited range of this quantity (e.g. one cannot have a reduction of 200%), the regression was transformed by tanh such that the predicted effectiveness: $y = tanh (X \cdot p)$ so that $\lim_{x\to\infty} y(x) = 1$. $X$ is the predicted mFcγR activity for each cell line according to our model, and $p$ is the regression weights.

*5. Some of the reagents or methods are not described clearly in detail, such as the construction of TRP1(TA99) antibodies with different mIgG constant region and the method of melanoma lung metastasis model.*

We use the measurements found in the studies cited where applicable, but did not use these regents ourselves. Therefore, we believe it is best to reference these papers for the construction and application of these reagents. We have done so where we use these data.
