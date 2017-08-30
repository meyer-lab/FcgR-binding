---
title: Dissecting FcγR Regulation Through a Multivalent Binding Model
author:
- name: Ryan A. Robinett
  affiliation: Co-first author; Koch Institute for Integrative Cancer Research, Massachusetts Institute of Technology, Cambridge, MA
- name: Ning Guan
  affiliation: Co-first author; Koch Institute for Integrative Cancer Research, Massachusetts Institute of Technology, Cambridge, MA
- name: Anja Lux
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Markus Biburger
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Falk Nimmerjahn
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Aaron S. Meyer
  affiliation: Department of Bioengineering, University of California, Los Angeles
keywords: [FcγR receptors, immunology, antibodies, effector function]
institute: A
bibliography: ./Manuscript/References.bib
abstract: Many immune receptors transduce activation across the plasma membrane through their clustering. With Fcγ receptors, this clustering is driven by binding to antibodies of differing affinity that are in turn bound to multivalent antigen. As a consequence of this activation mechanism, accounting for and rationally manipulating IgG effector function is complicated by, among other factors, differing affinities between FcγR species and changes in the valency of antigen binding. In this study, we show that a model of multivalent receptor-ligand binding can effectively account for the contribution of IgG-FcγR affinity and immune complex valency. This model in turn enables us to make specific predictions about the effect of immune complexes of defined composition. In total, these results enable both rational immune complex design for a desired IgG effector function and the deconvolution of effector function by immune complexes.
link-citations: true
csl: ./Manuscript/Templates/nature.csl
---

# Summary points

- Avidity most prominently modulates low-affinity FcγR-immune complex binding
- A multivalent binding model can quantitatively predict FcγR-immune complex binding
- Immune complex avidity has an outsized contribution to FcγR multimerization as compared to binding
- A binding model deconvoles and predicts the influence of interventions modulating *in vivo* FcγR-driven effector function

# Introduction

Antibodies are critical and central regulators of the immune response. Antibodies of the IgG isotype interact with FcγR receptors expressed widely on innate immune effector cells. IgGs transduce effector function through multiple cell types—including macrophages, monocytes, neutrophils, and NK cells—and through multiple processes, including promoting antibody-dependent cell-mediated cytotoxicity (ADCC), antigen presentation, and cytokine response. IgG immunotherapies, operating through regulating effector cell function, have been used in the treatment of both cancer and autoimmune diseases. In cancer treatment, IgG therapies can show a synergistic effect when used in combination with checkpoint or cytokine-mediated immunotherapies [@Moynihan:2016jb; @Zhu:2015gy]. These biologic agents are particularly versatile therapeutic agents on account of their immunotherapeutic effects and their ability to operate directly through antigen binding and opsonization.

The ability to quantitatively predict FcγR-IgG function would aid the understanding and treatment of cancer, autoimmune diseases, and infectious diseases. Efforts to engineer IgG treatments with improved effector response have included designing Fc variants with biased FcγR binding, deglycosylating Fc domains (with the effect of modulating FcγR binding), and utilizing alternative IgG subclasses with distinct binding profiles [@Mimoto:2013gf; @Shields:2002bw]. In cases where antigen and antibody are exogenously provided, avidity and binding affinities may be manipulated coordinately in a controlled manner [@Ortiz:2016kc]. With a better understanding of the underlying regulation, endogenous humoral responses might similarly be modulated through adjuvant engineering [@Chung:2015kz].

Previous efforts have sought to improve our understanding of IgG-mediated effector function. These include efforts to carefully quantify the individual, monovalent FcγR-IgG interaction affinities [@Bruhns:2009kg; @Gavin20; @Guilliams:2014cm]. Others have characterized the effects of IgG glycosylation (which serves to modulate FcγR affinity) and immune complex (IC) avidity on the binding of IgG-antigen complexes [@Lux:2013iv; @Ortiz:2016kc]. Genetic models have made it possible to remove certain FcγRs and examine the consequent effect on IgG treatment, including in the treatment of various cancers [@Clynes:2000ga; @Nimmerjahn:2005hu; @Bournazos:2014cw]. By comparing antibodies of matched variable region but differing Fc domains, one can evaluate the influence of effector function, though with necessarily pleiotropic effects on binding to each FcγR class [@Nimmerjahn:2005hu; @Bournazos:2014cw].

Models of multivalent ligand binding to monovalent receptors have been successfully employed to study the function of other immune receptors with corresponding binding models [@Perelson:1980fs; @Perelson:1980ds; @Hlavacek:1999gb]. For example, a two-component binding model can capture the effect of T cell receptor activation or FcεRI binding [@Stone:2001fm; @Hlavacek:1999bb]. Unlike many immune receptor families, distinct members of the FcγR family can be simultaneously expressed within certain cells. Additionally, the multiple FcγRs present, with activating and inhibitory roles, ensure that any manipulation of IC composition will necessarily have multivariate effects. This same challenge of combinatorial receptor regulation exists for other paired receptor-ligand families, including type I cytokines and interferons [@Piehler:2012bx; @Arneja:2014fz]. Thus, while the underlying theoretical models of multivalent binding are long-standing, FcγR-IgG interactions are especially suited for developments in inference approaches to rigorously link these models to experimental observations [@ForemanMackey:2013ux; @Wingate:2011vu; @Graham:2016ws].

In this study, we have employed a model of multivalent IC binding to FcγRs and show that it can capture experimentally measured binding at differing valencies. Applying this model, we show it can quantitatively predict effector response to diverse interventions in a forward manner and can deconvolve the causal factors of response in a reverse fashion. More broadly, these results demonstrate the abilities of both a unified binding model and computational inference techniques to link theory and experimental observation.
