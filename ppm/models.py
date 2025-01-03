from django.db import models

# Create your models here.


class Protein(models.Model):
    uniport_id = models.CharField(verbose_name='uniport id', max_length=50,unique=True,primary_key=True)
    reviewed = models.CharField(verbose_name='reviewed', max_length=10, default='unreviewed')
    protein_name = models.CharField(verbose_name='name', max_length=50, default='-')
    gene_symbol = models.CharField(verbose_name='gene', max_length=50, default='-')
    entreze_id = models.CharField(verbose_name='entreze id', max_length=20, default='-')
    ensembl_id = models.CharField(verbose_name='ensmbl id', max_length=30, default='-')
    family = models.CharField(verbose_name='family', max_length=100, default='-')
    organism = models.CharField(verbose_name='organism', max_length=100, default='-')
    organism_id = models.CharField(verbose_name='organism id', default='0', max_length=15)
    sequence = models.TextField(verbose_name='sequence', default='-')
    length = models.IntegerField(verbose_name="seq len", default=0)
    sid = models.CharField(verbose_name='site id', default='-', max_length=20)
    site = models.CharField(verbose_name='site', default='-', max_length=20)
    evidence = models.CharField(verbose_name='evidence', default='-', max_length=100)
    evidence_source = models.CharField(verbose_name='evidence source', default='-', max_length=50)
    database = models.CharField(verbose_name='database', default='-', max_length=20)
    description = models.TextField(verbose_name='description', default='-')
    interpro_id = models.CharField(verbose_name='interpro id', max_length=30, default='-')

    def __str__(self):
        return self.uniport_id


class Site(models.Model):
    sid = models.CharField(verbose_name='site id', unique=True, primary_key=True, max_length=20)
    eid = models.CharField(verbose_name='e id', max_length=10, default='-')
    ptase = models.CharField(verbose_name='PTase', max_length=15, default='-')
    ptm = models.CharField(verbose_name='PTM', max_length=50, default='-')
    donor = models.CharField(verbose_name='Donor', max_length=15, default='-')

    def __str__(self):
        return self.sid


class PTase(models.Model):
    eid = models.CharField(verbose_name='e id', max_length=10, unique=True, primary_key=True)
    ptase = models.CharField(verbose_name='PTase', max_length=15, default='-')
    gene_symbol = models.CharField(verbose_name='gene symbol', default='-', max_length=100)
    uniport_id = models.CharField(verbose_name='uniport id', default='-', max_length=100)
    organism = models.CharField(verbose_name='organism', default='-', max_length=100)
    organism_id = models.IntegerField(verbose_name='organism id', default=0)
    enzyme_database = models.CharField(verbose_name='database', default='-', max_length=20)

    def __str__(self):
        return self.eid


class Inhibitor(models.Model):
    i_id = models.CharField(verbose_name='i id', max_length=8, unique=True, primary_key=True)
    e_id = models.CharField(verbose_name='e id', max_length=20, default='-')
    name = models.CharField(verbose_name='name', max_length=50, default='-')
    state = models.CharField(verbose_name='state', max_length=100, default='-')
    enzyme_type = models.CharField(verbose_name='enzyme type', max_length=100, default='-')
    enzyme = models.CharField(verbose_name='enzyme', max_length=100, default='-')
    drugbank_id = models.CharField(verbose_name='drug id', max_length=10, default='-')
    disease = models.CharField(verbose_name='disease', max_length=50, default='-')
    DO_id = models.CharField(verbose_name='disease id', max_length=20, default='-')
    pubmed_id = models.CharField(verbose_name='pubmed', max_length=50, default='-')
    description = models.TextField(verbose_name='descript', default='-')

    def __str__(self):
        return self.i_id


class Compound(models.Model):
    chembl_id = models.CharField(verbose_name='chembl id', max_length=25, unique=True, primary_key=True)
    e_id = models.CharField(verbose_name='e id', max_length=20, default='-')
    target_id = models.CharField(verbose_name='chembl id', max_length=25, default='-')
    target_uniport_id = models.CharField(verbose_name='target uid', max_length=50, default='-')
    canonocal_smiles = models.CharField(verbose_name='smiles', max_length=200, default='-')
    pchembl_value = models.CharField(verbose_name='value', default='-', max_length=5)
    standard_relation = models.CharField(verbose_name='standard relation', max_length=5, default='=')
    standard_type = models.CharField(verbose_name='type', max_length=20, default='-')
    standard_units = models.CharField(verbose_name='units', max_length=5, default='-')
    standard_value = models.CharField(verbose_name='value', default='-', max_length=5)

    def __str__(self):
        return self.chembl_id


class Disease(models.Model):
    disease_id = models.CharField(verbose_name='disease id', max_length=10, unique=True, primary_key=True)
    protein_id = models.CharField(verbose_name='uniport id', max_length=50, default='-')
    s_id = models.CharField(verbose_name='site id', max_length=50, default='-')
    tissue_cell = models.CharField(verbose_name='tissue/cell', max_length=200, default='-')
    disease_ontology = models.CharField(verbose_name='disease ontology', max_length=200, default='-')
    DO_id = models.CharField(verbose_name='disease id', max_length=20, default='-')
    pubmed_id = models.CharField(verbose_name='pubmed id', max_length=50, default='-')
    description = models.TextField(verbose_name='description')

    def __str__(self):
        return self.disease_id