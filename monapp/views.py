

from django.shortcuts import render

from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect


def accueil(request):
    # Forcer l'affichage non connecté pour les tests
    context = {
        'titre': 'Bienvenue',
        'message': 'Contenu public'
    }
    return render(request, 'monapp/accueil.html', context)
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'monapp/inscription.html', {'form': form})
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès.")
        return redirect('accueil')
    return render(request, 'monapp/logout.html')


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'monapp/login.html'
    redirect_authenticated_user = True
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('accueil')
    def form_valid(self, form):
        remember = self.request.POST.get('remember', False)
        if not remember:
            self.request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
            self.request.session.modified = True
        return super().form_valid(form)
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipment
from .forms import EquipmentForm

def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'monapp/list.html', {'equipments': equipments})

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipments')
    else:
        form = EquipmentForm()
    return render(request, 'monapp/form.html', {'form': form})

def edit_equipment(request, N):
    equipment = get_object_or_404(Equipment, N=N)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipments')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'monapp/form.html', {'form': form})

def delete_equipment(request, N):
    equipment = get_object_or_404(Equipment,N=N)
    if request.method == 'POST':
        equipment.delete()
    return redirect('equipments')

# code pour la page de personnel########################################################################

from django.shortcuts import render
from .models import Personnel
from django.shortcuts import render, redirect
from .forms import PersonnelForm

def personnel_list(request):
    personnel = Personnel.objects.all().order_by('nom')
    return render(request, 'monapp/personnel.html', {'personnel': personnel})

def add_personnel(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('personnel_list')
    else:
        form = PersonnelForm()

    return render(request, 'monapp/add.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect


def edit_personnel(request, N ):
    personnel = get_object_or_404(Personnel, N=N)

    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('personnel_list')
    else:
        form = PersonnelForm(instance=personnel)

    return render(request, 'monapp/edit.html', {
        'form': form,
        'personnel': personnel
    })


def delete_personnel(request, N):
    personnel = get_object_or_404(Personnel, N=N)

    if request.method == 'POST':
        personnel.delete()

    return redirect('personnel_list')



from django.shortcuts import render
from .models import Historique_de_pannes
import json
from django.utils.timezone import datetime

from django.db.models import Count, Avg
from django.utils import timezone
import json


def list_equipment(request):
    # Récupération des données de pannes
    current_year = timezone.now().year
    pannes = Historique_de_pannes.objects.filter(date_panne__year=current_year)

    # Calcul des occurrences
    stats = pannes.values('equipment__name').annotate(count=Count('id')).order_by('-count')

    # Calcul du total et pourcentages cumulés
    total = sum(item['count'] for item in stats)
    cumulative = 0
    pareto_data = []

    for item in stats:
        cumulative += item['count']
        pareto_data.append({
            'equipment': item['equipment__name'],
            'count': item['count'],
            'percentage': round((cumulative / total) * 100, 2) if total > 0 else 0
        })

    return render(request, 'monapp/list.html', {
        'equipments': Equipment.objects.all(),
        'pareto_data': json.dumps(list(pareto_data)),  # Conversion explicite
        'selected_year': current_year
    })

#################  diagramme pareto ######################

from django.shortcuts import render
from .models import Historique_de_pannes
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

def pareto_chart(request):
    annee = request.GET.get('annee', 2025)  # Par défaut, 2025
    try:
        annee = int(annee)
    except ValueError:
        annee = 2025

    # Récupération des données filtrées
    pannes = Historique_de_pannes.objects.filter(annee_panne=annee)

    if not pannes.exists():
        return render(request, 'monapp/pareto.html', {
            'plot_html': "<p>Aucune donnée pour l'année sélectionnée.</p>",
            'annee': annee
        })

    # Regroupement des pannes par type avec comptage
    df = pd.DataFrame(list(pannes.values('equipment_id')))
    df = df['equipment_id'].value_counts().reset_index()
    df.columns = ['equipment_id', 'Fréquence']
    df['Cumul'] = df['Fréquence'].cumsum()
    df['Cumul %'] = 100 * df['Cumul'] / df['Fréquence'].sum()


    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['equipment_id'],
        y=df['Fréquence'],
        name='Fréquence',
        marker_color='lightsalmon',
        yaxis='y1'
    ))
    fig.add_trace(go.Scatter(
        x=df['equipment_id'],
        y=df['Cumul %'],
        name='Cumul %',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(color='blue'),
        line=dict(width=2)
    ))
    fig.update_layout(
        title=f'Diagramme de Pareto - Année {annee}',
        xaxis=dict(title='Type de panne'),
        yaxis=dict(title='Fréquence', side='left'),
        yaxis2=dict(title='Pourcentage cumulé', overlaying='y', side='right', range=[0, 110]),
        margin=dict(t=50, b=50)
    )

    plot_html = pio.to_html(fig, full_html=False)

    return render(request, 'monapp/pareto.html', {'plot_html': plot_html, 'annee': annee})

################# Historique  ############################

from .models import Historique_de_PDR
from .models import Historique_de_pannes
from .models import HistoriquePlanning
def Historique(request):
    historique = Historique_de_pannes.objects.all()
    historiquePDR = Historique_de_PDR.objects.all()
    historiqueplanning=HistoriquePlanning.objects.all()
    return render(request, 'monapp/historique.html',{'historique': historique,'historiquePDR': historiquePDR,'historiqueplanning':historiqueplanning})

###############  diagramme de performance ##############

from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Historique_de_pannes, Personnel
import plotly.graph_objects as go

def personnel_avec_radar(request):
    personnel = Personnel.objects.all()
    selected_agent = request.GET.get('agent')
    chart_div = None

    if selected_agent:
        try:
            agent_obj = Personnel.objects.get(pk=selected_agent)
            full_name = f"{agent_obj.nom} {agent_obj.prenom}"
            pannes = Historique_de_pannes.objects.filter(agent=full_name)

            grouped = pannes.values('panne').annotate(
                count=Count('id'),
                avg_ttr=Avg('ttr')
            )

            labels = [item['panne'] for item in grouped]
            values_count = [item['count'] for item in grouped]
            values_ttr = [round(item['avg_ttr'], 2) for item in grouped]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values_count, theta=labels, fill='toself', name='Nombre de Pannes'))
            fig.add_trace(go.Scatterpolar(r=values_ttr, theta=labels, fill='toself', name='TTR Moyen'))

            fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
            chart_div = fig.to_html(full_html=False)

        except Personnel.DoesNotExist:
            pass

    return render(request, 'monapp/personnel.html', {
        'personnel': personnel,
        'agents': personnel,
        'chart_div': chart_div,
        'selected_agent': selected_agent,
    })
######################### page de PDR ###############################################################################
# views.py
from django.shortcuts import render
from .models import Historique_de_PDR
from .forms import EquipmentSelectForm
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from matplotlib.patches import Rectangle


def abc_analysis(df):
    df_sorted = df.sort_values(by='consommation_annuelle', ascending=False).copy()
    total_consommation = df_sorted['consommation_annuelle'].sum()
    df_sorted['consommation_cumulee'] = df_sorted['consommation_annuelle'].cumsum()
    df_sorted['pourcentage_cumule'] = (df_sorted['consommation_cumulee'] / total_consommation) * 100
    df_sorted['rang'] = list(range(1, len(df_sorted) + 1))
    df_sorted['pourcentage_rang'] = (df_sorted['rang'] / len(df_sorted)) * 100

    sum_pourcentage_cumule = df_sorted['pourcentage_cumule'].sum()
    n = len(df_sorted)
    nombre = str(n)
    chiffres = nombre.replace('-', '').replace('.', '')
    nn = len(chiffres)
    pas = 10 ** nn / n
    area_curve = sum_pourcentage_cumule * pas
    gini = (area_curve - 5000) / 5000
    gini = round(gini, 4)

    if gini >= 0.90:
        bins = [0, 10.0000000000001, 20.0000000000001, float('inf')]
    elif gini >= 0.85:
        bins = [0, 10.0000000000001, 30.0000000000001, float('inf')]
    elif gini >= 0.78:
        bins = [0, 20.0000000000001, 45.0000000000001, float('inf')]
    else:
        bins = [0, 20.0000000000001, 50.0000000000001, float('inf')]

    labels = ['A', 'B', 'C']

    df_sorted['classification'] = pd.cut(
        df_sorted['pourcentage_rang'],
        bins=bins,
        labels=labels,
        right=False
    )

    return df_sorted, gini


def plot_abc_rectangles(df_sorted, gini):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_ylim(0, 120)
    ax.set_xlim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.3)

    # Définition des intervalles pour les rectangles
    if gini >= 0.90:
        a_range, b_range, b_rangge, c_range = 10, 10, 20, 80
    elif gini >= 0.85:
        a_range, b_range, b_rangge, c_range = 10, 20, 30, 70
    elif gini >= 0.78:
        a_range, b_range, b_rangge, c_range = 20, 25, 45, 55
    else:
        a_range, b_range, b_rangge, c_range = 20, 30, 50, 50

    class_bins = df_sorted.groupby('classification')['pourcentage_cumule'].max()
    a_max = class_bins.get('A', 0)
    b_maxx = class_bins.get('B', a_max)
    b_max = b_maxx - a_max

    ax.add_patch(Rectangle((0, 0), a_range, a_max, facecolor='#FFC3C3', edgecolor='black'))
    ax.add_patch(Rectangle((a_range, a_max), b_range, b_max, facecolor='#FFF0C3', edgecolor='black'))
    ax.add_patch(Rectangle((b_rangge, b_maxx), c_range, 100 - b_maxx, facecolor='#E5F3D5', edgecolor='black'))

    ax.plot(df_sorted['pourcentage_rang'], df_sorted['pourcentage_cumule'],
            marker='o', color='navy', linewidth=2, label='Courbe ABC')

    for _, row in df_sorted.iterrows():
        ax.text(row['pourcentage_rang'] + 1, row['pourcentage_cumule'] + 1.5,
                f"{int(row['consommation_cumulee'])}", fontsize=9)

    plt.xlabel('% Rang')
    plt.ylabel('% Consommation cumulée')
    plt.title('Courbe ABC avec classification dynamique (Gini = {:.2f})'.format(gini))
    plt.legend()

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def dashboard(request):
    from .models import Equipment
    form = EquipmentSelectForm(request.GET or None)
    data = []
    chart = None

    if form.is_valid():
        equipement = form.cleaned_data['equipement']
        data_qs = Historique_de_PDR.objects.filter(equipement=equipement)

        if data_qs.exists():
            df = pd.DataFrame.from_records(data_qs.values('PDR', 'consomation'))
            df = df.groupby('PDR').sum().reset_index()
            df.columns = ["Numéro d'article", "consommation_annuelle"]
            df_sorted, gini = abc_analysis(df)
            chart = plot_abc_rectangles(df_sorted, gini)
            data = data_qs

    return render(request, 'monapp/dashboard.html', {
        'form': form,
        'data': data,
        'chart': chart
    })
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import pandas as pd

def export_pdf(request):

    form = EquipmentSelectForm(request.GET or None)
    chart = None
    df_sorted = None

    if form.is_valid():
        equipement = form.cleaned_data['equipement']
        data_qs = Historique_de_PDR.objects.filter(equipement=equipement)

        if data_qs.exists():
            df = pd.DataFrame.from_records(data_qs.values('PDR', 'consomation'))
            df = df.groupby('PDR').sum().reset_index()
            df.columns = ["Numéro d'article", "consommation_annuelle"]
            df_sorted_obj, gini = abc_analysis(df)
            chart = plot_abc_rectangles(df_sorted_obj, gini)
            df_sorted = df_sorted_obj[['Numéro d\'article', 'consommation_annuelle', 'classification']].values.tolist()

    template = get_template("monapp/pdf_template.html")
    html = template.render({'df_sorted': df_sorted, 'chart': chart})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_ABC.pdf"'
    pisa.CreatePDF(src=html, dest=response)
    return response

########### page de plannification ##################################################
from django.shortcuts import render
from django.http import JsonResponse
from .forms import HistoriquePlanningForm
from datetime import datetime
import json

def planning_view(request):
    form = HistoriquePlanningForm()
    eve = HistoriquePlanning.objects.all()
    return render(request, 'monapp/planning.html', {'form': form,'eve': eve })

def save_planning(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = HistoriquePlanningForm(data)
        if form.is_valid():
            date = datetime.strptime(data['date'], '%Y-%m-%d')
            planning = form.save(commit=False)
            planning.jour = date.day
            planning.mois = date.month
            planning.ans = date.year
            planning.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)
############# page de bon travail ############################################################
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from .forms import BonTravailForm
from .models import BonTravail
from xhtml2pdf import pisa
import io

def bon_form_view(request):
    if request.method == 'POST':
        form = BonTravailForm(request.POST)
        if form.is_valid():
            bon = form.save()
            return redirect('bon_pdf', pk=bon.pk)
    else:
        form = BonTravailForm()
    return render(request, 'monapp/bon_form.html', {'form': form})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def bon_pdf_view(request, pk):
    bon = BonTravail.objects.get(pk=pk)
    pdf = render_to_pdf('monapp/bon_pdf.html', {'bon': bon})
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BonTravail_{bon.numero}.pdf"'
    return response
##### Dashboard ################################################################################
def accueil(request):
    # Forcer l'affichage non connecté pour les tests
    historique2 = Historique_de_pannes.objects.all()

    # Calcul du MTTR (Mean Time To Repair)
    MTTR = sum([h.ttr for h in historique2])
    TRS= '60 %'

    context = {
        'titre': 'Bienvenue',
        'message': 'Contenu public',
        'MTTR': MTTR,
        'TRS' : TRS ,
    }
    notifs = Notification.objects.filter(user_id=request.user).order_by('-date')[:10]

    return render(request, 'monapp/accueil.html', {'context':context,'notifications': notifs })

##############page de declaration ###############################################
# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import PanneForm
from .models import Historique_de_pannes
from .models import Notification
@login_required
def declarer_panne(request):
    type_panne = request.GET.get("type_panne")

    if request.method == 'POST':
        if request.POST.get("selected_panne_id"):
            # Cas : panne existante
            from datetime import datetime
            panne_id = request.POST.get("selected_panne_id")
            original = Historique_de_pannes.objects.get(id=panne_id)

            # Crée une nouvelle instance avec les mêmes valeurs
            Historique_de_pannes.objects.create(
                panne=original.panne,
                ttr=original.ttr,
                criticite=original.criticite,
                agent=request.user.username,
                annee_panne=datetime.now().year,
                equipment=original.equipment,
            )
            message = f"{request.user.username} a déclaré la panne '{original.panne}' sur l’équipement {original.equipment.name}"
            for user in User.objects.filter(is_superuser=False):  # ou tous les utilisateurs selon votre besoin
                Notification.objects.create(message=message, user=user, date=datetime.now(), is_read=0)

            return redirect('success_page')

        else:
            # Cas : nouvelle panne
            form = PanneForm(request.POST)
            if form.is_valid():
                panne = form.save(commit=False)
                panne.agent = request.user.username
                from datetime import datetime
                panne.annee_panne = datetime.now().year
                panne.save()
                message = f"{request.user.username} a déclaré la panne '{panne.panne}' sur l’équipement {panne.equipment.name}"
                # Créer une notification pour chaque superadmin ou utilisateur concerné
                for user in User.objects.filter(is_superuser=False):  # ou tous les utilisateurs selon votre besoin
                    Notification.objects.create(message=message, user=user,date=datetime.now(),is_read=0)
                # Notif admin
                admins = User.objects.filter(is_superuser=True)
                for admin in admins:
                    send_mail(
                        subject='Nouvelle panne déclarée',
                        message=f"Panne déclarée sur l’équipement {panne.equipment.nom} par {request.user.username}.",
                        from_email='gmao@exemple.com',
                        recipient_list=[admin.email],
                        fail_silently=True,
                    )
                return redirect('success_page')
    else:
        form = PanneForm()

    pannes_existantes = Historique_de_pannes.objects.all()
    return render(request, 'monapp/declarer_panne.html', {
        'form': form,
        'type_panne': type_panne,
        'pannes_existantes': pannes_existantes
    })

from django.shortcuts import render

def success_page(request):
    return render(request, 'monapp/success_page.html')






