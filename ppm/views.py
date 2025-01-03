from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.views.generic.base import View
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from PPMDB import settings
from .utils import homeSearch, searchMore
from .models import Disease

# Create your views here.
html_dict = {'protein': 'protein.html', 'disease': 'disease.html', 'enzyme': 'enzyme.html',
                     'inhibitor': 'inhibitor.html', 'compound': 'compound.html'}
protein_letters = "ACDEFGHIKLMNPQRSTVWY"

def home(request):
    return render(request, 'home.html', {
        'hoStyle': "color:#09ffff !important;",
    })

class HomeSearch(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('ppm:home'))

    @csrf_exempt
    def post(self, request):
        searchType = request.POST.get('searchType')
        searchTerm = request.POST.get('searchTerm', 'All')
        if searchTerm == '':
            searchTerm = 'ALL'
        res, count = homeSearch(searchType, searchTerm)
        return render(request, html_dict.get(searchType), {
            'seStyle': "color:#09ffff !important;",
            'dataset': res,
            'count': count
        })

class BrowseView(View):
    def get(self, request):
        return render(request, 'ppm/templates/browse.html', {
            'brStyle': "color:#09ffff !important;",
            'title': 'Browse',
        })

    @csrf_exempt
    def post(self, request):
        searchType = request.POST.get('searchType')
        searchTerm = request.POST.get('searchTerm', 'All')
        res, count = homeSearch(searchType, searchTerm)
        return render(request, html_dict.get(searchType), {
            'brStyle': "color:#09ffff !important;",
            'dataset': res,
            'count': count,
            'type': 1
        })

class ContactView(View):
    def get(self, request):
        return render(request, 'ppm/templates/contact.html', {'coStyle': "color:#09ffff !important;"})

    @csrf_exempt
    def post(self, request):
        return render(request, 'ppm/templates/contact.html', {'msg': 'OK'})
        subject = "Deep-B3P Question: "
        name = "Name: " + str(request.POST.get('inputName'))
        email = "Email: " + str(request.POST.get('inputEmail'))
        message = "Message: " + str(request.POST.get('inputMessage'))
        msg = '\r\n'.join([name, email, message])
        send_mail(subject, msg, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=["384767937@qq.com"])
        return render(request, 'ppm/templates/contact.html', {'msg': 'OK'})


class showMore(View):
    def get(self, request):
        # 获取请求参数
        sType = request.GET.get('type')
        uid = request.GET.get('uid')

        # 定义映射关系
        type_to_handler = {
            'protein': ('show-more.html', self.handle_protein),
            'disease': ('show-disease.html', self.handle_disease),
            'enzyme': ('show-enzyme.html', self.handle_enzyme),
            'inhibitor': ('show-inhibitor.html', self.handle_inhibitor),
            'compound': ('compound.html', self.handle_compound),  # 示例模板
        }

        if sType in type_to_handler:
            template, handler = type_to_handler[sType]
            return handler(request, uid, template)

        # 如果 sType 不在映射中，重定向到主页
        return HttpResponseRedirect(reverse('ppm:home'))

    def handle_protein(self, request, uid, template):
        try:
            # 获取数据
            protein, ptase, dis = searchMore('protein', uid)
            seq = protein.sequence
            x = ProteinAnalysis(seq)
            pep_aac = x.get_amino_acids_percent()

            # 处理氨基酸组成
            aac = [one for one in "ACDEFGHIKLMNPQRSTVWY" if pep_aac.get(one, 0) != 0]
            com = [round(pep_aac.get(one, 2), 2) for one in aac]

            # 渲染模板
            return render(request, template, {'protein': protein,'ptase': ptase,'dis': dis,'aac': aac,'com': com})
        except Exception as e:
            return HttpResponse(f"Error processing protein: {str(e)}", status=500)

    def handle_disease(self, request, uid, template):
        try:
            # 获取疾病数据和总数
            disease, total = searchMore('disease', uid)
            return render(request, template, {'dis': disease,'total': total})
        except Exception as e:
            return HttpResponse(f"Error processing disease: {str(e)}", status=500)

    def handle_enzyme(self, request, uid, template):
        try:
            enzyme, total = searchMore('enzyme', uid)
            return render(request, template, {'enzyme': enzyme,'total': total})
        except Exception as e:
            return HttpResponse(f"Error processing enzyme: {str(e)}", status=500)

    def handle_inhibitor(self, request, uid, template):
        try:
            inhibitor, total = searchMore('inhibitor', uid)
            return render(request, template, {'inhibitor': inhibitor,'total': total})
        except Exception as e:
            return HttpResponse(f"Error processing inhibitor: {str(e)}", status=500)

    def handle_compound(self, request, uid, template):
        # 示例处理逻辑，实际可以扩展
        return render(request, template, {'message': "Compound logic not yet implemented"})

def statistics(request):
    return render(request, 'ppm/templates/statistics.html', {'stStyle': "color:#09ffff !important;"})


def document(request):
    return render(request, 'ppm/templates/statistics.html', {'doStyle': "color:#09ffff !important;"})

def updata():
    file = r'E:\database\PPMdb_data\PPMdb\Inhibitor.csv'
    import pandas as pd
    from .models import Inhibitor
    df = pd.read_csv(file, sep='\t')
    for index, row in df.iterrows():
        i_id = row['I_ID']
        e_id = row['E_ID_1']
        ptase = row['PTase']
        name = row['Name']
        state = row['State']
        drugbank_id = row['DrugBank ID']
        disease = row['disease ontology']
        DO_id = row['DOID']
        pubmed_id = row['PubMed ID']
        description = row['Description']
        enzyme = row['enzyme']
        obj = Inhibitor(
            i_id=i_id,
            e_id=e_id,
            enzyme_type=ptase,
            name=name,
            state=state,
            drugbank_id=drugbank_id,
            disease=disease,
            DO_id=DO_id,
            pubmed_id=pubmed_id,
            description=description,
            enzyme=enzyme
        )
        obj.save()
        print(i_id)


def show_disease(request, sid):
    # 使用 s_id 来查询数据库
    disease = get_object_or_404(Disease, s_id=sid)
    return render(request, 'ppm/templates/show-disease.html', {'disease': disease})