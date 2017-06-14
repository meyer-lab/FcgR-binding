## Model

### Base model

TNP-BSA equilibrium binding to FcγRs was modeled using a two-parameter equilibrium model of multivalent ligand binding to monovalent receptors expressed uniformly on a cell surface [@Stone:2001fm; @Perelson:1980fs]. This model assumes an excess of ligand. Within the model, binding is assumed to occur first according to a monovalent binding interaction governed by the individual binding site affinity $K_a$, and then through subsequent cross-linking events with equilibrium partitioning $K_x$. Therefore, according to the model, the number of ligand bound $i$-valently to the cell at equilibrium, $v_{i,eq}$, can be found using the relation

$$ v_{i,eq} = {f\choose i} (K_x)^{i-1} {L_0}{K_a} \left(R_{eq}\right)^i. $$ {#eq:vieq}

Here, $f$ is the effective avidity of the ligand, $K_x$ is a cross-linking parameter with units of # per cell, $L_0$ is the concentration of ligand, and $R_{eq}$ is the number of unbound receptors at equilibrium. Consequently, the total number of ligand bound at equilibrium is

$$ L_{bound} = \sum_{i=1}^{f} v_{i,eq} = \sum_{i=1}^{f} { f\choose i } (K_x)^{i-1} {L_0}{K_a} (R_{eq})^i. $$ {#eq:lbound}

$R_{eq}$ represents the quantity of unbound receptors, and is a function of $f$, $L_0$, $K_a$, $K_x$, and $R_{tot}$, the total number of receptors expressed on the cell surface. $R_{eq}$ can be solved for numerically using the relationship

$$ R_{tot} = R_{eq} \left(1+f {L_0}{K_D} (1+K_x R_{eq})^{f-1}\right) $$ {#eq:rtot}

when these parameters are known. As a consequence of [@eq:vieq], the number of receptors that are clustered with at least one other receptor at equilibrium ($R_{multi}$) is equal to

$$ R_{multi} = \sum_{i=2}^{f} iv_{i,eq}. $$ {#eq:rmulti}

### Specification for $K_x$

$K_x$ cannot be constant across different combinations of FcγR and IgG, as a constant value of $K_x$ makes this model invalid under certain regimes. Specifically, a constant value for $K_x$ is consistent with a high local concentration of ligand, leading to receptor-ligand binding determined more so by receptor accessibility via cell surface diffusion than other factors. However, for low-affinity FcγR-IgG binding, $K_x$ must ultimately be reduced, and $K_x$ for interactions with zero affinity must equal zero. Further, detailed balance is only satisfied for cases with multiple receptors of differing affinity present when allowed to vary with affinity. Therefore, we represented $K_x$ for any given crosslinking interaction as the product of $K_a$, the affinity of the epitope being bound for the receptor species to which it binds, and a crosslinking coefficient, $K_x^*$, that is uniform for all combinations of FcγR and IgG. For any given crosslinking interaction between an epitope-receptor pair with affinity $K_a$,

$$ K_x = K_x^* K_a. $$ {#eq:kx}

As a consequence of this construction, $K_x$ becomes zero in the absence of binding and satisfies detailed balance.

### Parameters and assumptions

Association constants for all combinations of hIgG and hFcγR were obtained from previous experimental measurements [@Bruhns:2009kg]. In each replicate of the binding assay, cells were coincubated with 5 µg/ml TNP-4-BSA or TNP-26-BSA. Because the molar masses of 2,4,6-trinitrophenyl groups and of BSA are approximately 173 Da and 66430 Da, respectively, we represented the molar concentrations of TNP-4-BSA and TNP-26-BSA as 74 nM and 70 nM [@Lux:2013iv]. We also assumed that there were two different conversion factors for TNP-4-BSA and TNP-26-BSA between the number of ICs bound and the mean fluorescent intensities (MFIs) measured in the assay, due to IC detection occuring through TNP quantitation. Lastly, we assumed that, due to steric effects, the effective avidities of TNP-4-BSA and (especially) TNP-26-BSA might be different than their actual avidities. This required us to fit the following eleven parameters: the total expression level $R_{tot}$ for each hFcγR, $K_x^*$, conversion factors from ligand bound to MFI measured for both TNP-BSAs, and effective avidities for both TNP-BSAs ($f_{4}$ and $f_{26}$, respectively). In our simulation, receptor expression levels were allowed to vary between $10^3$ and $10^8$, $K_x^*$ between $10^{-25}$ and $10^3$ (in order to provide no constraint on possible values), the conversion factors between $10^{-10}$ and $10^5$, $f_4$ between one and twenty, and $f_{26}$ between twelve and thrity-two.

### Model fitting and deviation parameters

We fit our model to binding measurements for each hFcγR-hIgG pair using an affine invariant Markov chain Monte Carlo sampler as implemented within the `emcee` package [@ForemanMackey:2013ux]. Therefore, we additionally fit a standard deviation parameter $\sigma_1^*$. The likelihood for each combination of predicted values for $K_x^*$, the two conversion factors, $f_4$, and $f_{26}$ for each hFcγR-hIgG-TNP-BSA combination was calculated by comparison of our experimental data to a normal distribution with mean equal to our model's predicted binding and standard deviation equal to the predicted binding times $\sigma_1^*$.

In addition to IC binding, the receptor expression of each cell line was quantitatively measured. We assumed that the receptor expression measurements were log-normally distributed, with the standard deviation of the log-normal distribution being proportional to the common logarithm of the actual expression. We fit a second standard deviation parameter, $\sigma_2^*$, such that the likelihood of each receptor measurement was calculated using a normal distribution with mean equal to the common logarithm of the predicted receptor expression and standard deviation equal to this value times $\sigma_2^*$. The overall likelihood of the model at each parameter set was calculated as the product of all individual likelihoods. The priors for each parameter were therefore otherwise specified to be uniform within their lower and upper bounds. $\sigma_1^*$ and $\sigma_2^*$ were allowed to vary between $10^{-4}$ and $10$.

We assayed the convergence of the Markov chain using the Geweke diagnostic and chain autocorrelation [@Geweke:1991tk]. The Geweke diagnostic was used to determine whether early and late segments of the Markov chain could have been sampled from the same probability distribution. Each walker's series of values for a particular parameter was treated as a single chain, upon which the diagnostic was evaluated.

### Generalized Multi-Receptor Model

To account for cells expressing multiple FcγRs, we extended the model to account for binding in the presence of multiple receptors. $K_x$ must be proportional to $K_a$ to fulfill detailed balance. Under the same assumptions as before, the relative proportion of receptor complexes with $N$ receptors respectively bound $i$, $j$, $k$,...-valently is specified as:

$$ \varPhi = \frac{K_x \left( K_a \odot R_{eq} \right)}{K_{a, i}} $$ {#eq:KKRK}

$$ $$ {#eq:}

$$ v_{i,j,eq} = {v \choose i} \frac{L_0 K_{a, i}}{K_x} \prod_{q \in (i, j, ...)} \varPhi_q^{v_{q}} $$ {#eq:vieqTwo}

where $K_{a,z}$ and $R_{eq,z}$ are the association constant and unbound abundance for receptor $z$, respectively. As a consequence, $0 \leq i + j + ... < v$. As the amount of each receptor binding only weakly interacted, this was solved by iteratively root-finding for mass balance of each receptor independently, using the Brent routine (`scipy.optimize.brenth`). The amount of bound ligand or bound receptor was calculated by summing over each multimerization state, weighted by its probability.

### Activity Index

To account for the combined effects of activating, inhibitory, and decoy receptors, we defined an activity index. To do so, we defined the activity multimerization state as being the dot product of the vector $v$ indicating the number of each receptor, and $w$ consisting of the activity for each receptor. Activating receptors were given an activity of 1, decoy receptors 0, and inhibitory receptors -1. Multimerization states that resulted in activities of less than 0 were set to zero. This definition satisfied our expectations that activity increase with a greater number of activating receptors, decrease with more inhibitory receptors, and not change with variation in the number of decoy receptors. After the activity of each state was calculated each was summed, weighted according to the relative probability of each state. Only states in which more than one receptor was bound were considered, implicitly assuming that monovalent binding does not elicit activity. This produced the overall activity index value for a given condition at equilibrium.
