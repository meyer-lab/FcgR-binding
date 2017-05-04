### Generalized Multi-Receptor Model

To account for cells expressing multiple FcγRs, we extended the model to account for binding in the presence of multiple receptors. K~x~ must be proportional to K~a~ to fulfill detailed balance. Under the same assumptions as before, the relative proportion of receptor complexes with N receptors respectively bound i, j, k...-valently is specified as:

$$ \varPhi = \frac{K_x \left( K_a \odot R_{eq} \right)}{K_{a, i}} $$ {#eq:KKRK}

$$ $$ {#eq:}

$$ v_{i,j,eq} = {v \choose i} \frac{L_0 K_{a, i}}{K_x} \prod_{q \in (i, j, ...)} \varPhi_q^{v_{q}} $$ {#eq:vieqTwo}

where K~z~ and R~eq,z~ is the association constant and unbound abundance for receptor z, respectively. As a consequence, $0 \leq i + j ... < v$. Therefore, the amount of ligand bound to either receptor is calculated by:

$$ L_{bound} = \sum_{\forall i + j > 0} v_{i,j,eq}  $$ {#eq:mlbound}

The amount of receptor bound to ligand is calculated differently depending upon the receptor in question:

$$ R_{bnd,i} = \sum_{i=1}^{v} \sum_{\forall j} i v_{i,j,eq} $$ {#eq:mrtot}

$$ R_{bnd,j} = \sum_{j=1}^{v} \sum_{\forall i} j v_{i,j,eq} $$ {#eq:mmrtot}

R~eq~ was solved by solving for:

$$ R_{bnd} + R_{eq} = R_{tot} $$ {#eq:massbal}

As the amount of each receptor binding only weakly interacted, this was solved by iteratively root-finding for each receptor independently, using the Brent routine (`scipy.optimize.brenth`).