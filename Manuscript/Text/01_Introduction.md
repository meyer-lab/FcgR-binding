---
title: Dissecting FcγR Regulation Through a Multivalent Binding Model
author:
- name: Ryan A. Robinett
  affiliation: Koch Institute for Integrative Cancer Research
- name: Ning Guan
  affiliation: Koch Institute for Integrative Cancer Research
- name: Anja Lux
  affiliation: Friedrich-Alexander-University of Erlangen-Nürnberg
- name: Aaron S. Meyer
  affiliation: Koch Institute for Integrative Cancer Research
keywords:
- FcγR receptors
- Immunology
institute: A
bibliography: ./Manuscript/References.bib
abstract: Many immune receptors transduce activation across the plasma membrane through their clustering. With Fcγ receptors, this clustering is driven by binding to antibodies of differing affinity in turn bound to multivalent antigen. As a consequence of this activation mechanism, accounting for and rationally manipulating IgG effector function is complicated by, among other factors, the contribution of differing affinities to multiple FcγRs and changes in the valency of antigen binding. In this study, we show that a model of multivalent receptor-ligand binding can effectively account for the contribution of IgG-FcγR affinity and immune complex valency. This model in turn enables us to make specific predictions about the effect of immune complexes of defined composition. In total, these results enable rationally designed IgG effector function, or deconvolution of function, in both a forward and reverse manner.
link-citations: true
csl: ./Manuscript/Templates/nature.csl
---

# Summary points

- Avidity most prominently modulates low-affinity FcγR-immune complex binding
- A multivalent binding model can quantitatively predict FcγR-immune complex binding
- Immune complex avidity has an outsized contribution to FcγR multimerization as compared to binding
- A binding model deconvoles the influence of interventions modulating *in vivo* FcγR-driven effector function

# Introduction

Antibodies are critical and central regulators of the immune response. Antibodies of the IgG isotype interact with FcγR receptors expressed widely on innate immune effector cells. Regulation of effector cell function is a critical component of the IgG therapy's use in cancer and autoimmune diseases. Effector function operates through multiple cell types—including macrophages, monocytes, neutrophils, and NK cells—and through multiple process including promoting antibody-dependent cell-mediated cytotoxicity (ADCC), promoting antigen presentation, and cytokine response. In addition to their effect in isolation, IgG therapies can show synergistic effect in cancers in combination with checkpoint and cytokine-mediated immunotherapies [@Moynihan:2016jb] [@Zhu:2015gy]. These immunotherapeutic effects in combination with antibodies' ability to operate as signaling modulators through competitive binding and opsonization make IgG biologic agents particularly versatile therapeutic agents.

An ability to quantitatively predict IgG-FcγR function would aid understanding and treatment of cancer and autoimmune diseases. Efforts to engineer improved effector responses to IgG treatment include mutated Fc variants with biased FcγR binding, deglycosylated Fc domains with the effect of modulating FcγR binding, and alternative IgG subclasses with distinct binding profiles. In addition, particularly in cases where antigen and antibody are exogenously provided, avidity and binding affinities may be manipulated coordinately in a controlled manner [@Ortiz:2016kc].

Multiple efforts have sought to improve our understanding of IgG-mediated effector function. These include efforts to carefully quantify the individual, monovalent FcγR-IgG affinities [@Bruhns:2009kg]. In addition, previous studies have characterized the effects of IgG glycosylation (which serves to modulate FcγR affinity) and immune complex avidity on the binding of IgG-antigen complexes [@Lux:2013iv]. Genetic models have made it possible to remove certain FcγRs and examine the consequent effect on IgG treatment in various cancer models [@Clynes:2000ga]. Finally, comparison of antibodies with matched variable regions but differing Fc domains has allowed the effects to be compared, through with necessarily pleiotropic effects on binding to each FcγR class [@Nimmerjahn:2005hu].

Models of multivalent ligand binding to monovalent receptors have been successfully employed to study function of other immune receptors with known, corresponding binding models [@Perelson:1980fs] [@Perelson:1980ds] [@Hlavacek:1999gb]. For example, a two-component binding model can capture the effect of T cell receptor activation [@Stone:2001fm]. However, the FcγR family presents the considerable additional challenge of multiple distinct receptor classes expressed simultaneously within cells. Additionally, the multiple FcγRs present, with activating and inhibitory roles, ensure that any manipulation of immune complex composition will necessarily have multivariate effects. The same challenge exists for other paired receptor-ligand families, including other immunoglobulin classes and the many phosphatidylserine receptors. Thus, while the underlying theoretical models of multivalent binding are long-standing, FcγR-IgG interactions are especially suited for developments in inferrence approaches to rigorously link these models to experimental observations.

In this study, we have employed a model of multivalent immune complex binding to FcγR receptors and show that it can capture the experimentally measured binding at differing valencies. Applying this model, we show it can quantitatively predict effector response in response to diverse interventions in a forward manner, and can deconvolve the causal factors of response in a reverse fashion. More broadly, these results demonstrate the power of a unified binding model tied to computational inference techniques linking theory and experimental observation.
