# ==============================================================================
# Imports
# ==============================================================================
from pandas import DataFrame, read_csv
from networkx import DiGraph
from libsbml import SBMLReader, XMLNode, GeneProductRef

from typing import Dict, List, Tuple, Union, Set

# ==============================================================================
# Parser
# ==============================================================================

def parse_sbml(sbml_filepath: str) -> Tuple[Dict,Dict,Dict,Set,Dict]:
    sbmld = SBMLReader().readSBML(sbml_filepath) # type: ignore
    sbmlm = sbmld.getModel()
    sbml_fbc = sbmlm.getPlugin("fbc")
    
    input_mets = set()
    inputs = {}
    matrix = {}
    capacities = {}
    genes_association = {}
    genes = set()
    
    capacities_id = {}
    for parameter in sbmlm.getListOfParameters():
        capacities_id[parameter.id] = parameter.value
    
    for metabolite in sbmlm.getListOfSpecies():
        name = metabolite.getId()
        if metabolite.boundary_condition:
            input_mets.add(name)
    
    for reaction in sbmlm.getListOfReactions():
        name = reaction.getId()

        for a in reaction.getListOfReactants():
            coeff = a.getStoichiometry()
            species = a.getSpecies()
            matrix[(species, name)] = -coeff
            if species in input_mets:
                inputs[species] = name
        for a in reaction.getListOfProducts():
            coeff = a.getStoichiometry()
            species = a.getSpecies()
            matrix[(species, name)] = coeff
            if species in input_mets:
                inputs[species] = name
        
        xml_attributes = XMLNode.getAttributes(reaction.toXMLNode())
        lower_bound = capacities_id[xml_attributes.getValue('lowerFluxBound')]
        upper_bound = capacities_id[xml_attributes.getValue('upperFluxBound')]
        capacities[name] = (lower_bound, upper_bound)
        
        r_fbc = reaction.getPlugin("fbc")
        ga = r_fbc.getGeneProductAssociation() if r_fbc else None
        if ga:
            # fetch referenced genes
            # TODO? parse logic
            def resolve_gref(e):
                gp = e.getGeneProduct()
                gp = sbml_fbc.getGeneProduct(gp)
                return gp.getMetaId()
            r_genes = {resolve_gref(e) for e in ga.getListOfAllElements()
                             if isinstance(e, GeneProductRef)}
            genes_association[name] = r_genes
    
    for g in sbml_fbc.getListOfGeneProducts():
        id = g.getId()
        genes.add(id)

    return matrix, capacities, genes_association, genes, inputs

def parse_pkn(pkn_filepath: str) -> DiGraph:
    pkn = DiGraph()
    with open(pkn_filepath) as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            split_line = line.split()
            u = split_line[0]
            v = split_line[1]
            s = int(split_line[2]) if len(split_line) > 2 else 0
            pkn.add_edge(u, v, sign=s)
    return pkn

def parse_timeseries(csv_filepath: str) -> DataFrame:
    df = read_csv(
        csv_filepath,
        header=0, 
        index_col=['Time'],
        sep=','
    )
    return df

# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':
    pass
