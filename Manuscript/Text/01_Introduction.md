---
title: Dissecting FcγR Regulation Through a Multivalent Binding Model
author:
- name: Ryan A. Robinett
  affiliation: Koch Institute for Integrative Cancer Research, Massachusetts Institute of Technology, Cambridge, MA
- name: Ning Guan
  affiliation: Koch Institute for Integrative Cancer Research, Massachusetts Institute of Technology, Cambridge, MA
- name: Anja Lux
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Falk Nimmerjahn
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Aaron S. Meyer
  affiliation: Koch Institute for Integrative Cancer Research, Massachusetts Institute of Technology, Cambridge, MA; Department of Bioengineering, University of California, Los Angeles
keywords:
- FcγR receptors
- Immunology
institute: A
bibliography: ./Manuscript/References.bib
abstract: Many immune receptors transduce activation across the plasma membrane through their clustering. With Fcγ receptors, this clustering is driven by binding to antibodies of differing affinity that are in turn bound to multivalent antigen. As a consequence of this activation mechanism, accounting for and rationally manipulating IgG effector function is complicated by, among other factors, differing affinities of between FcγR species and changes in the valency of antigen binding. In this study, we show that a model of multivalent receptor-ligand binding can effectively account for the contribution of IgG-FcγR affinity and immune complex valency. This model in turn enables us to make specific predictions about the effect of immune complexes of defined composition. In total, these results enable both rationally design of immune complexes for a desired IgG effector function and the deconvolution of effector function by immune complexes.
link-citations: true
csl: ./Manuscript/Templates/nature.csl
---

# Summary points

- Avidity most prominently modulates low-affinity FcγR-immune complex binding
- A multivalent binding model can quantitatively predict FcγR-immune complex binding
- Immune complex avidity has an outsized contribution to FcγR multimerization as compared to binding
- A binding model deconvoles and predicts the influence of interventions modulating *in vivo* FcγR-driven effector function

# Introduction

Antibodies are critical and central regulators of the immune response. Antibodies of the IgG isotype interact with FcγR receptors expressed widely on innate immune effector cells, and effector cell function regulation is a critical component of the IgG therapy's use in cancer and autoimmune diseases. IgGs transduce effector function through multiple cell types—including macrophages, monocytes, neutrophils, and NK cells—and through multiple processes including promoting antibody-dependent cell-mediated cytotoxicity (ADCC), antigen presentation, and cytokine response. In addition to their effect in isolation, IgG therapies can show a synergistic effect in cancers in combination with checkpoint and cytokine-mediated immunotherapies [@Moynihan:2016jb; @Zhu:2015gy]. These immunotherapeutic effects in combination with antibodies' ability to operate directly through antigen binding and opsonization make IgG biologic agents particularly versatile therapeutic agents.

An ability to quantitatively predict FcγR-IgG function would aid the understanding and treatment of cancer, autoimmune diseases, and infectious diseases. Efforts to engineer IgG treatments with improved effector response have included designing Fc variants with biased FcγR binding, deglycosylated Fc domains with the effect of modulating FcγR binding, and alternative IgG subclasses with distinct binding profiles [@Mimoto:2013gf; @Shields:2002bw]. In addition, particularly in cases where antigen and antibody are exogenously provided, avidity and binding affinities may be manipulated coordinately in a controlled manner [@Ortiz:2016kc]. With a better understanding of the underlying regulation, endogenous humoral responses might be modulated through adjuvant engineering [@Chung:2015kz].

Previous efforts have sought to improve our understanding of IgG-mediated effector function. These include efforts to carefully quantify the individual, monovalent FcγR-IgG affinities seen _in vivo_ [@Bruhns:2009kg; @Gavin20; @Guilliams:2014cm]. Others have characterized the effects of IgG glycosylation (which serves to modulate FcγR affinity) and immune complex (IC) avidity on the binding of IgG-antigen complexes [@Lux:2013iv; @Ortiz:2016kc]. Genetic models have made it possible to remove certain FcγRs and examine the consequent effect on IgG treatment, including in various cancer models [@Clynes:2000ga; @Nimmerjahn:2005hu; @Bournazos:2014cw]. By comparing antibodies of matched variable regions but differing Fc domain, one can evaluate the influence of effector function, though with necessarily pleiotropic effects on binding to each FcγR class [@Nimmerjahn:2005hu; @Bournazos:2014cw].

Models of multivalent ligand binding to monovalent receptors have been successfully employed to study the function of other immune receptors with known, corresponding binding models [@Perelson:1980fs; @Perelson:1980ds; @Hlavacek:1999gb]. For example, a two-component binding model can capture the effect of T cell receptor activation or binding to FcεRI [@Stone:2001fm; @Hlavacek:1999bb]. However, the FcγR family presents the considerable additional challenge of multiple distinct receptor classes expressed simultaneously within cells. Additionally, the multiple FcγRs present, with activating and inhibitory roles, ensure that any manipulation of IC composition will necessarily have multivariate effects. This same challenge of combinatorial receptor regulation exists for other paired receptor-ligand families, including type I cytokines and interferons [@Piehler:2012bx; @Arneja:2014fz]. Thus, while the underlying theoretical models of multivalent binding are long-standing, FcγR-IgG interactions are especially suited for developments in inference approaches to rigorously link these models to experimental observations [@ForemanMackey:2013ux; @Wingate:2011vu; @Graham:2016ws].

In this study, we have employed a model of multivalent IC binding to FcγR receptors and show that it can capture the experimentally measured binding at differing valencies. Applying this model, we show it can quantitatively predict effector response to diverse interventions in a forward manner and can deconvolve the causal factors of response in a reverse fashion. More broadly, these results demonstrate both the power of a unified binding model and the ability of computational inference techniques to link theory and experimental observation.
