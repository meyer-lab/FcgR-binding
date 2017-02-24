# Results

## IgG-FcγR binding varies with affinity and avidity

![**FcγR binding changes with FcγR-IgG pair and avidity.** A) Quantification of human IgG subclass TNP-4-BSA and TNP-26-BSA immune complex binding to CHO cells expressing the indicated human FcγRs (N = 4). Background binding of the immune complexes to CHO cells expressing no human FcγR was subtracted from the mean fluorescence intensity (MFI) obtained for binding to CHO cells expressing individual human FcγRs. B) Receptor expression quantification for each CHO cell line expressing individual FcγRs. C) Measured TNP-4-BSA immune complex binding, normalized to the receptor expression within each CHO cell line, as a function of the measured FcγR-IgG subclass affinity [@Bruhns:2009kg]. D) Measured TNP-26-BSA immune complex binding, normalized to the receptor expression within each CHO cell line, as a function of the measured FcγR-IgG subclass affinity [@Bruhns:2009kg].](./Figures/Figure1.png){#fig:Binding}

Building upon earlier work, we wished to examine the influence of immune complex avidity and composition on binding and activation of different FcγRs [@Lux:2013iv]. In a similar manner to before, we assessed the immune complex binding for each pair of four IgG and six FcγR subclasses at a single concentration. To do so, we utilized a panel of CHO cell lines stably expressing each FcγR and immune complexes assembled by use of BSA with 2,4,6-trinitrophenol (TNP) covalently attached at an average avidity of 4 or 26. anti-TNP antibodies of differing IgG class were then bound to the BSA complexes before treatment.

We measured receptor abundance quantitatively for each FcγR expressing cell line to account for this source of potential variation in binding between cell lines. This measurement revealed 20-fold variation in the amount of each FcγR expressed ([@Fig:Binding]A). To interpret these measurements, we normalized the amount of binding measured to the amount of FcγR expressed, and plotted each measurement against the measured affinity of the individual FcγR-IgG monovalent interaction ([@Fig:Binding]B). The measured binding and variation in binding with avidity recapitulated that measured before, with variation as a function of IgG class, FcγR, and avidity [@Lux:2013iv].

By comparing the normalized binding to the affinity of each FcγR-IgG interaction, we observed a strong correlation between the affinity of the relevant FcγR-IgG pair and measured binding ([@Fig:Binding]C-D). Each relationship was plotted against log-transformed measurements to emphasize the wide range in measured binding. Comparing the output of each TNP-26 and TNP-4 measurement showed that the former consistently yielded X-fold greater signal ([@Fig:Binding]E). However, the variation in binding varied from that predicted by monovalent binding ([@Fig:Binding]C-D) and the effect of avidity on binding relied on the affinity of the interaction ([@Fig:Binding]E). Each of these factors indicated that the effect of avidity on binding must be accounted for directly.

## A multivalent binding model accounts for variation in IgG-FcγR binding

![**A multivalent binding model accounts for IgG-FcγR binding.** A) Schematic of the multivalent binding model for interaction of an immune complex with FcγRs. B) Trace for MCMC chain during fitting process. C) Predicted versus measured binding for each FcγR-IgG pair at each avidity. D) Marginal distribution for the crosslinking constant Kx. E) Marginal distribution for the constants to convert immune complex binding to normalized fluorescence signal. F) Marginal distribution for the avidity of TNP-4-BSA and TNP-26-BSA. G) Marginal distribution for each distribution spread parameter. H) The marginal distributions for receptor expression within each cell line expressing a signal FcγR. Experimental measurements of receptor expression are individually overlaid. I) Marginal distribution of Kx.](./Figures/Figure2.png){#fig:Fit}

To interpret the complex variation in binding we observed with IgG-FcγR pair (i.e. affinity), receptor expression, and immune complex avidity, we employed an equilibrium model of multivalent ligand/monovalent receptor binding [@Stone:2001fm]. Within the model, an initial binding event occurs with the kinetics of the monovalent interaction. Subsequent multivalent binding events occur with a partition coefficient K~x~. Thus, K~x~ values much greater than 1 lead to highly multivalent interactions while K~x~ values much less than 1 lead to predominantly monovalent binding.









## The parameterized binding model provides specific predictions for the coordinate effects of immune complex abundance, avidity, and class

![**Specific predictions regarding the coordinate effects of immune complex parameters.** A) Predicted binding versus concentration of immune complex for varying avidity. B) Predicted multimerized FcgR versus concentration of immune complex for varying avidity. C) The number of receptor crosslinks versus concentration of immune complex for varying avidity. D) The amount of binding versus number of crosslinks for two different affinities, with varied avidities. E) The predicted amount of multimerized receptor versus avidity for a cell expressing XXXX and XXXX simultaneously. F) The predicted ratio of multimerized activating to inhibitory FcgR for a cell expressing XXXX and XXXX simultaneously.](./Figures/Figure3.png){#fig:ParamModel}











## An IgG-FcγR binding model deconvolves *in vivo* function

![**.** A) XXX. B) XXX. C) XXX.](./Figures/Foo.png){#fig:InVivoResults}
