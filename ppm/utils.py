# -- coding: utf-8 --
# author : TangQiang
# time   : 2024/4/10
# email  : tangqiang.0701@gmail.com
# file   : utils.py

from django.db.models import Q
from . models import Protein, Disease, PTase, Inhibitor, Compound, Site


####数据较小，统一处理
def searchProtein(sItem):
    if sItem and sItem.upper() not in ['ALL', 'OTHERS']:
        res = Protein.objects.filter(
            Q(uniport_id=sItem) |
            Q(reviewed=sItem) |
            Q(gene_symbol=sItem) |
            Q(entreze_id=sItem) |
            Q(organism__contains=sItem) |
            Q(organism_id=sItem)|
            Q(family__contains=sItem)
        ).values('uniport_id', 'organism', 'gene_symbol', 'protein_name').distinct()
    elif sItem.upper() == 'ALL':
        res = Protein.objects.all().values('uniport_id', 'organism', 'gene_symbol', 'protein_name').distinct()
    elif sItem.upper() == 'OTHERS': # this is for browse page others
        res = Protein.objects.exclude(
            Q(organism__in=[
                'Hepatitis delta virus (HDV)', 'Homo sapiens (Human)', 'Mus musculus (Mouse)',
                'Arabidopsis thaliana (Mouse-ear cress)', 'Cyprinus carpio (Common carp)',
                'Rattus norvegicus (Rat)', 'Sus scrofa (Pig)', 'Dictyostelium discoideum (Social amoeba)',
                'Bos taurus (Bovine)']
            )
        ).values('uniport_id', 'organism', 'gene_symbol', 'protein_name').distinct()
    result = []
    uid_list = []
    org_list = []
    gene_list = []
    for one in res:
        uid = one.get('uniport_id')
        organism = one.get('organism')
        gene = one.get('gene_symbol')
        uid_list.append(uid)
        org_list.append(organism)
        gene_list.append(gene)
        result.append([uid, one.get('protein_name'), organism, gene])
    uid_list = set(uid_list)
    org_list = set(org_list)
    gene_list = set(gene_list)
    uid_list.discard('-')
    org_list.discard('-')
    gene_list.discard('-')
    count = {'UniPort': len(uid_list), 'Organism': len(org_list), 'Gene': len(gene_list)}
    return result, count

def searchDisease(sItem):
    if sItem and sItem.upper() != 'ALL':
        res = Disease.objects.filter(
            Q(tissue_cell__contains=sItem) |
            Q(disease_ontology__contains=sItem)
        ).values('disease_ontology', 'tissue_cell', 'DO_id', 'protein_id').distinct()
    else:
        res = Disease.objects.all().values('disease_ontology', 'tissue_cell', 'DO_id', 'protein_id').distinct()
    result = []
    name_list = []
    tiss_list = []
    for one in res:
        name = one.get('disease_ontology')
        name_list.append(name)
        tiss_cell = one.get('tissue_cell')
        tiss_list.append(tiss_cell)
        id = one.get('DO_id')
        uid = one.get('protein_id')
        result.append([name, tiss_cell, id, uid])
    name_list = set(name_list)
    tiss_list = set(tiss_list)
    name_list.discard('-')
    tiss_list.discard('-')
    return result, {'disease': len(name_list), 'tiss': len(tiss_list)}

def searchEnzyme(sItem):
    if sItem and sItem.upper() != 'ALL':
        res = PTase.objects.filter(
            Q(ptase__contains=sItem) |
            Q(uniport_id__contains=sItem) |
            Q(organism__contains=sItem)
        ).values('ptase', 'organism', 'uniport_id', 'eid').distinct()
    else:
        res = PTase.objects.all().values('ptase', 'organism', 'uniport_id', 'eid').distinct()
    result = []
    p_list, o_list, pro_list = [], [], []
    for one in res:
        ptase = one.get('ptase')
        organism = one.get('organism')
        p_id = one.get('uniport_id')
        e_id = one.get('eid')
        p_list.append(ptase)
        o_list.append(organism)
        p_id_list = []
        if p_id != '-':
            p_ids = p_id.split(',')
            for one in p_ids:
                pro_list.append(one)
                pstr = '<a href = "https://www.uniprot.org/uniprotkb/{0}/" target = "_blank" >{1}</a>'.format(one, one)
                p_id_list.append(pstr)
        else:
            p_id_list = [p_id]
        result.append([ptase, organism, ','.join(p_id_list), e_id])
    p_list = set(p_list)
    o_list = set(o_list)
    pro_list = set(pro_list)
    p_list.discard('-')
    o_list.discard('-')
    pro_list.discard('-')
    return result, {'Ptase': len(p_list), 'organism': len(o_list), 'protein': len(pro_list)}

def searchInhibitor(sItem):
    if sItem and sItem.upper() != 'ALL':
        res = Inhibitor.objects.filter(
            Q(name__contains=sItem) |
            Q(enzyme__contains=sItem) |
            Q(enzyme_type__contains=sItem) |
            Q(drugbank_id__contains=sItem)
        ).values('name', 'enzyme_type', 'enzyme', 'disease', 'DO_id').distinct()
    else:
        res = Inhibitor.objects.all().values('name', 'enzyme_type', 'enzyme', 'disease', 'DO_id').distinct()
    result = []
    for one in res:
        result.append([one.get('name'), one.get('enzyme'), one.get('enzyme_type'), one.get('disease'), one.get('DO_id')])
    return result, {}

def searchCompound(sItem):
    if sItem and sItem.upper() != 'ALL':
        res = Compound.objects.filter(
            Q(chembl_id=sItem) |
            Q(target_id=sItem) |
            Q(target_uniport_id__contains=sItem)
        ).values('chembl_id', 'target_id', 'target_uniport_id').distinct()
    else:
        res = Compound.objects.all().values('chembl_id', 'target_id', 'target_uniport_id').distinct()
    result = []
    c_list = []
    t_list = []
    u_list = []
    for one in res:
        chembl = one.get('chembl_id')
        c_list.append(chembl)
        target = one.get('target_id')
        t_list.append(target)
        uniport = one.get('target_uniport_id')
        pro_list = []
        if uniport != '-':
            uniports = uniport.split(';')
            for one in uniports:
                u_list.append(one)
                pstr = '<a href = "https://www.uniprot.org/uniprotkb/{0}/" target = "_blank" >{1}</a>'.format(one, one)
                pro_list.append(pstr)
        else:
            pro_list = [uniport]
        result.append([chembl, target, ','.join(pro_list)])
    c_list = set(c_list)
    t_list = set(t_list)
    u_list = set(u_list)
    c_list.discard('-')
    t_list.discard('-')
    u_list.discard('-')
    return result, {'chembl': len(c_list), 'target': len(t_list), 'uniport': len(u_list)}

def homeSearch(sType, sItem):
    if sType == 'protein':
        result, count = searchProtein(sItem)
        return result, count
    elif sType == 'disease':
        result, count = searchDisease(sItem)
        return result, count
    elif sType=='enzyme':
        result, count = searchEnzyme(sItem)
        return result, count
    elif sType == 'inhibitor':
        result, count = searchInhibitor(sItem)
        return result, count
    elif sType == 'compound':
        result, count = searchCompound(sItem)
        return result, count


def format_source_link(source):
    """辅助函数，用于格式化 source 链接"""
    source_list = []
    for one in source:
        id = one.strip().split(':')[-1]
        if one.startswith('PubMed'):
            source_list.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{id}/" target="_blank">{one}</a>')
        elif one.startswith('UniProtKB'):
            source_list.append(f'<a href="https://www.uniprot.org/uniprotkb/{id}/entry" target="_blank">{one}</a>')
        elif one.startswith('PDB'):
            source_list.append(f'<a href="https://www.rcsb.org/structure/{id}" target="_blank">{one}</a>')
    return ', '.join(source_list)


def searchMore(sType, sId):
    if sType == 'protein':
        ptase, dis_list = [], []
        protein = Protein.objects.filter(uniport_id=sId).first()

        if not protein:
            return None, None, None

        sites = protein.site.split(';')  # 位点
        sids = protein.sid.split(';')  # 位点id
        news = list(protein.sequence)

        # 收集 PTase 数据
        for i, site in enumerate(sites):
            id = site.strip()
            pt = [id, protein.sequence[int(id) - 1]]
            news[int(id) - 1] = f'<span style="color:red">{news[int(id) - 1]}</span>'

            sid = Site.objects.filter(sid=sids[i].strip()).first()
            pt.append(sid)
            ptase.append(pt)

        # 收集 Disease 数据
        dis = Disease.objects.filter(protein_id=sId, s_id=protein.sid)
        dis_list = [(protein.sid, one) for one in dis]

        # 格式化 evidence sources
        source = protein.evidence_source.replace(" ", "").split(',')
        protein.evidence_source = format_source_link(source)

        # 更新 protein sequence
        protein.sequence = ''.join(news)

        return protein, ptase, dis_list

    elif sType == 'disease':
        dis_list = [(disease.s_id, disease) for disease in Disease.objects.filter(disease_ontology=sId)]
        return dis_list, len(dis_list)

    elif sType == 'enzyme':
        enzyme = PTase.objects.filter(eid=sId).first()

        if not enzyme:
            return None, None

        enzyme.gene_symbol = enzyme.gene_symbol.replace(" ", "").split(",")
        enzyme.uniport_id = enzyme.uniport_id.replace(" ", "").split(",")

        return enzyme, len(enzyme.uniport_id) + 1

    elif sType == 'inhibitor':
        inhibitors = Inhibitor.objects.filter(name=sId)
        for inhibitor in inhibitors:
            inhibitor.e_id = inhibitor.e_id.split(';')
            inhibitor.enzyme = inhibitor.enzyme.split(';')
            inhibitor.enzyme_type = inhibitor.enzyme_type.split(';')

        return inhibitors, len(inhibitors)




