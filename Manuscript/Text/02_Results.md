# Results

## IgG-FcγR binding varies with affinity and avidity

![**FcγR binding changes with FcγR-IgG pair and avidity.** A) Quantification of human IgG subclass TNP-4-BSA and TNP-26-BSA immune complex binding to CHO cells expressing the indicated human FcγRs (N = 4). Background binding of the immune complexes to CHO cells expressing no human FcγR was subtracted from the mean fluorescence intensity (MFI) obtained for binding to CHO cells expressing individual human FcγRs. B) Receptor expression quantification for each CHO cell line expressing individual FcγRs. C) Measured TNP-4-BSA immune complex binding, normalized to the receptor expression within each CHO cell line, as a function of the measured FcγR-IgG subclass affinity [@Bruhns:2009kg]. D) Measured TNP-26-BSA immune complex binding, normalized to the receptor expression within each CHO cell line, as a function of the measured FcγR-IgG subclass affinity [@Bruhns:2009kg].](./Figures/Figure1.svg){#fig:Binding}

Building upon earlier work, we wished to examine the influence of immune complex avidity and composition on binding and activation of different FcγRs [@Lux:2013iv]. In a similar manner to before, we assessed the immune complex binding for each pair of four IgG and six FcγR subclasses at a single concentration. To do so, we utilized a panel of CHO cell lines stably expressing each FcγR and immune complexes assembled by use of BSA with 2,4,6-trinitrophenol (TNP) covalently attached at an average avidity of 4 or 26. anti-TNP antibodies of differing IgG class were then bound to the BSA complexes before treatment.

We measured receptor abundance quantitatively for each FcγR expressing cell line to account for this source of potential variation in binding between cell lines. This measurement revealed 20-fold variation in the amount of each FcγR expressed ([@Fig:Binding]A). To interpret these measurements, we normalized the amount of binding measured to the amount of FcγR expressed, and plotted each measurement against the measured affinity of the individual FcγR-IgG monovalent interaction ([@Fig:Binding]B). The measured binding and variation in binding with avidity recapitulated that measured before, with variation as a function of IgG class, FcγR, and avidity [@Lux:2013iv].

By comparing the normalized binding to the affinity of each FcγR-IgG interaction, we observed a strong correlation between the affinity of the relevant FcγR-IgG pair and measured binding ([@Fig:Binding]C-D). Each relationship was plotted against log-transformed measurements to emphasize the wide range in measured binding. Comparing the output of each TNP-26 and TNP-4 measurement showed that the former consistently yielded X-fold greater signal ([@Fig:Binding]E). However, the variation in binding varied from that predicted by monovalent binding ([@Fig:Binding]C-D) and the effect of avidity on binding relied on the affinity of the interaction ([@Fig:Binding]E). Each of these factors indicated that the effect of avidity on binding must be accounted for directly.

## A multivalent binding model accounts for variation in IgG-FcγR binding

![**A multivalent binding model accounts for IgG-FcγR binding.** A) Schematic of the multivalent binding model for interaction of an immune complex with FcγRs. B) Trace for MCMC chain during fitting process. C) Predicted versus measured binding for each FcγR-IgG pair at each avidity. D) Marginal distribution for the crosslinking constant Kx. E) Marginal distribution for the constants to convert immune complex binding to normalized fluorescence signal. F) Marginal distribution for the avidity of TNP-4-BSA and TNP-26-BSA. G) Marginal distribution for each distribution spread parameter. H) The marginal distributions for receptor expression within each cell line expressing a signal FcγR. Experimental measurements of receptor expression are individually overlaid. I) Marginal distribution of Kx.](./Figures/Figure2.svg){#fig:Fit}

To interpret the complex variation in binding we observed with IgG-FcγR pair (i.e. affinity), receptor expression, and immune complex avidity, we employed an equilibrium model of multivalent ligand/monovalent receptor binding [@Stone:2001fm]. Within the model, an initial binding event occurs with the kinetics of the monovalent interaction ([@Fig:Fit]A). Subsequent multivalent binding events occur with a partition coefficient K~x~. Thus, K~x~ values much greater than 1 lead to highly multivalent interactions while K~x~ values much less than 1 lead to predominantly monovalent binding.

While previous applications of this model have assumed K~x~ to be constant, those have not dealt with large variation in the affinity of the receptor-ligand interaction [@Stone:2001fm]. Treating this parameter as constant for interactions of different affinity may be reasonable for interactions of similar affinity, but clearly breaks down at the extremes. For example, for an FcγR-IgG interaction of barely measurable affinity, one would not expect to see multimer binding to occur with the same partitioning as an extremely high affinity interaction. Most concerning given the assumption of equilibrium, an assumption of constant K~x~ violates detailed balance when this model is extended to include expression of two FcγRs. Therefore, to solve these issues we assumed that K~x~ is proportional to K~a~. With this assumption, detailed balance is preserved (see methods), and at the limit of low K~a~, K~x~ is reduced as expected.

We utilized Markov Chain Monte Carlo to fit the model to our measurements of FcγR-IgG binding. Both inspection of the sample autocorrelation and Geweke diagnostic indicated convergence ([@Fig:Fit]B). Comparing the prediction of each condition to our measured values, we observed extremely close agreement ([@Fig:Fit]C). Inspecting the fit of each parameter revealed that all of the parameters were well-specified, and that many of the parameter fits closely agreed with prior expectations. The fit values of each conversion coefficient indicated a 1.6-fold difference in the relationship between the number of immune complexes bound and output fluorescence signal ([@Fig:Fit]E).












## The parameterized binding model provides specific predictions for the coordinate effects of immune complex abundance, avidity, and class

![**Specific predictions regarding the coordinate effects of immune complex parameters.** A) Predicted binding versus concentration of immune complex for varying avidity. B) Predicted multimerized FcgR versus concentration of immune complex for varying avidity. C) The number of receptor crosslinks versus concentration of immune complex for varying avidity. D) The amount of binding versus number of crosslinks for two different affinities, with varied avidities. E) The predicted amount of multimerized receptor versus avidity for a cell expressing XXXX and XXXX simultaneously. F) The predicted ratio of multimerized activating to inhibitory FcgR for a cell expressing XXXX and XXXX simultaneously.](./Figures/Figure3.svg){#fig:ParamModel}











## An IgG-FcγR binding model deconvolves *in vivo* function

![**.** A) XXX. B) XXX. C) XXX.](./Figures/Foo.png){#fig:InVivoResults}
