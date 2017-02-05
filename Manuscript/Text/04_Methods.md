# Methods

## Data

All binding measurements were generously provided by Anja Lux of the Nimmerjahn Lab. Binding was measured using ELISA. The quantity of ligand bound in the original data is measured in terms of mean fluorescent intensity (MFI). Four replicates were used in the lab's assays. We normalized the data by replicate in our simulations.


## Equations

### Base model

The equilibrium binding of TNP-X-BSA to FcγRs was modeled using an equilibrium model of multivalent ligand binding to monovalent receptors expressed uniformly on a cell surface [@Stone:2001fm].

According to the model, the number of ligand bound $i$-valently to the cell at equilibrium, $v_{eq}$, can be found using the relation

$$ v_{i,eq} = {v\choose i} (K_X)^{i-1} \frac{L_0}{K_D} (R_{eq})^i $$

Here, $K_X$ is a cross-linking constant with units of # per cell (for our purposes, $K_X$ is assumed to be identical for all combinations of FcγR and IgG,) $L_0$ is the concentration of ligand, and $R_{eq}$ is the number of receptors bound at equilibrium. Consequently,

$$ L_{bound} = \sum_{i=1}^{v} v_{i,eq} = \sum_{i=1}^{v} {v\choose i} (K_X)^{i-1} \frac{L_0}{K_D} (R_{eq})^i $$

where $L_{bound}$ is the total number of ligand bound at equilibrium and $v$ is the effective avidity of the ligand. It is important to distinguish between the effective avidity and the actual avidity of a multivalent ligand, as steric effects might prevent such a ligand from binding to $v_{actual}$ receptors at once. We will later show that this was the case in Lux's experiments. $R_{eq}$ is a function of $v$, $L_0$, $K_D$, $K_X$, and $Rtot$, the total number of receptors expressed on the cell surface, and can be approximated numerically using the following relationship when these parameters are known:

$$ R_{tot} = R_{eq} \Big(1+v \frac{L_0}{K_D} (1+K_X R_{eq})^{v-1}\Big) $$

Let $R_{eq}(R_{tot},v,L_0,K_D,K_X)$ be the numerical approximation of $R_{eq}$ given the parameters listed. Consequent of Equation (1), $R_{multi}$, the number of receptors that are clustered with at least one other receptor at equilibrium, can be found as follows:

$$ R_{multi} = \sum_{i=2}^{v} iv_{i,eq} $$

### Specification for K~x~





## Calculations

### Parameters and Assumptions

Association constants for all combinations of IgG and FcγR were obtained from previous experimental measurements [@Bruhns:2009kg].\textsuperscript{a} In each replicate of Lux's assay, cells were coincubated with 5 µg/ml TNP-X-BSA. Because the molar masses of a 2,4,6-trinitrophenyl groups and of BSA are approximately 173 Da and 66430 Da, respectively, we represented the molar concentrations of TNP-4-BSA and TNP-26-BSA as 74 nM and 70 nM.\textsuperscript{f} For the sake of parsimony, we assumed that the cross-linking constant $K_X$ is identical for all combinations of FcγR and IgG. We also assumed that there was a conversion factor between the number of ICs bound and MFI for both TNP-4-BSA and TNP-26-BSA and that these two conversion factors were likely different. Lastly, we assumed that, due to steric effects, the effective avidities of TNP-4-BSA and (especially) TNP-26-BSA might be different that their actual avidities. This required us, in total, to fit 11 parameters: the total expression level $R_{tot}$ for each FcγR, $K_X$, conversion factors from ligand bound to MFI for both TNP-BSAs ($c_{4}$ and $c_{26}$, respectively), and effective avidities for both TNP-BSAs ($f_{4}$ and $f_{26}$, respectively).

Based on the order of magnitude of cross-linking constant values presented in the aforementioned paper by Stone et al., we assumed that our cross-linking constant $K_X$ should be between

### Model Fitting

We fit the aforementioned parameters by minimizing a log-likelihood function of a form similar to that presented by Kitagawa (1986).\textsuperscript{g} We assume that the standard error of MFI for any combination of FcγR, IgG, and IC (TNP-4-BSA or TNP-26-BSA) is proportional to the mean of the normalized samples from trials involving that combination of conditions. Therefore, as opposed to fitting a standard error $\sigma$ for each combination of FcγR, IgG, and IC, we fit a standard error coefficient $\sigma^*$ for each combination, which, when multiplied by the mean of the corresponding trial sample, equals the standard deviation of the error for that combination. Therefore, we assume that the likelihood function of any set of parameters granted a specific combination $i$ of FcγR, IgG, and IC is of the form:

$$ \mathcal{L}(K_X,c_4,c_{26},f_4,f_{26},\sigma^*|i) = \prod_{j=1}^{n_i}{(\sigma^*\mu_i\sqrt{2\pi})^{-1}\exp{\Big(\frac{(y_{ij}-c_iL)^2}{2(\sigma^*\mu_i)^2}\Big)}} $$

where $n_i$ is the number of samples from the assay for that particular $i$, $y_{ij}$ is the $j$\textsuperscript{th} normalized MFI from the sample representing $i$, and $\mu_i$ is the algebraic mean of the sample representing $i$. The total log-likelihood, then, for particular a set of parameters is:

\begin{equation}
\begin{split}
l_{total}=\sum_i\log(\mathcal{L}(R_{tot,Fc\gamma RIIIA-158V},K_X,c_4,c_{26},f_4,f_{26},\sigma^*|i))
\end{split}
\end{equation}

We integrated under the log-likelihood distribution $l$ over all twelve parameters listed above using the mhsample implementation of the Metropolis-Hastings algorithm in MATLAB.\textsuperscript{e,h} We sampled 10 million points with using a burn-in length of 1000.
