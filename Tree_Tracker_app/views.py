from json import dumps
import requests
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Survey
from django.db import models
import geocoder


def index(request):
    if request.method=='POST':
        try:
            place=request.POST['Location']
            location=geocoder.osm(place)
            latitude, longitude=location.latlng
            lat=int(latitude)
            lan=int(longitude)
            print(lat,lan)
            data=[]
            for survey in Survey.objects.all():
                if int(survey.Latitude)==lat and int(survey.Longitude)==lan:
                    data.append({ 
                    'latitude': survey.Latitude,
                    'longitude': survey.Longitude,
                    'species': survey.species,
                    'tree_height':survey.tree_height,
                    'steam_diameter':survey.steam_diameter,
                    'crown_height':survey.crown_height,
                    'crown_diameter':survey.crown_diameter,
                    'spreading': survey.spreading,
                    'crown_damage': survey.crown_damage,
                    'trunk_damage': survey.trunk_damage,
                })
                else:
                    pass
            getspecies= set(Survey.objects.values_list('species'))
            datajson = dumps(data)
        except:
            print('location not found')
            data = []
            for survey in Survey.objects.all():
                data.append({ 
                    'latitude': survey.Latitude,
                    'longitude': survey.Longitude,
                    'species': survey.species,
                    'tree_height':survey.tree_height,
                    'steam_diameter':survey.steam_diameter,
                    'crown_height':survey.crown_height,
                    'crown_diameter':survey.crown_diameter,
                    'spreading': survey.spreading,
                    'crown_damage': survey.crown_damage,
                    'trunk_damage': survey.trunk_damage,
                })
            getspecies= set(Survey.objects.values_list('species'))
            datajson = dumps(data)
            return render(request, 'index.html', {'data': data,'json':datajson,'survey':len(data),'species':len(getspecies)})

            
        try:
            filt=request.POST['filter']
            filt_text=request.POST['filter_text']
            data=[]
            lst=Survey.object.values_list('id',filt)
            for i in lst:
                if lst[1]==filt_text:
                    data.append({ 
                    'latitude': Survey.object.get(id=i).Latitude,
                    'longitude': Survey.object.get(id=i).Longitude,
                    'species': Survey.object.get(id=i).species,
                    'tree_height':Survey.object.get(id=i).tree_height,
                    'steam_diameter':Survey.object.get(id=i).steam_diameter,
                    'crown_height':Survey.object.get(id=i).crown_height,
                    'crown_diameter':Survey.object.get(id=i).crown_diameter,
                    'spreading': Survey.object.get(id=i).spreading,
                    'crown_damage': Survey.object.get(id=i).crown_damage,
                    'trunk_damage': Survey.object.get(id=i).trunk_damage,
                })
            getspecies= set(Survey.objects.values_list('species'))
            datajson = dumps(data)
            return render(request, 'index.html', {'data': data,'json':datajson,'survey':len(data),'species':len(getspecies)})
        except:
            return render(request, 'index.html', {'data': data,'json':datajson,'survey':len(data),'species':len(getspecies)})
        
        
        
    else:
        data = []
        for survey in Survey.objects.all():
            data.append({ 
                'latitude': survey.Latitude,
                'longitude': survey.Longitude,
                'species': survey.species,
                'tree_height':survey.tree_height,
                'steam_diameter':survey.steam_diameter,
                'crown_height':survey.crown_height,
                'crown_diameter':survey.crown_diameter,
                'spreading': survey.spreading,
                'crown_damage': survey.crown_damage,
                'trunk_damage': survey.trunk_damage,
            })
        getspecies= set(Survey.objects.values_list('species'))
        datajson = dumps(data)
        return render(request, 'index.html', {'data': data,'json':datajson,'survey':len(data),'species':len(getspecies)})

def index2(request):
    if request.method=='post':
        location=request.POST['Location']
        filt=request.POST['']

def add(request):
    if request.method == 'POST':
            survey = Survey()
            survey.Latitude = request.POST['latitude']
            survey.Longitude = request.POST['longitude']
            survey.species = request.POST['species']
            survey.tree_height = request.POST['tree_height']
            survey.steam_diameter = request.POST['steam_diameter']
            survey.crown_height = request.POST['crown_height']
            survey.crown_diameter = request.POST['crown_diameter']
            survey.spreading = request.POST['spreading']
            survey.crown_damage = request.POST['crown_dmg']
            survey.trunk_damage = request.POST['trunk_dmg']
            survey.reason_crown_damage = request.POST['reason_crown_dmg']
            survey.reason_trunk_damage = request.POST['reason_trunk_dmg']
            survey.save()
        
    else:
        context = {}
    return render(request, 'map.html')


def species(request):
    tree_species = [
        "Acacia",
        "Adenanthera pavonina",
        "Anogeissus",
        "Azadirachta indica",
        "Bauhinia",
        "Bombax ceiba",
        "Casuarina equisetifolia",
        "Cassia fistula",
        "Ficus",
        "Gmelina arborea",
        "Mangifera indica",
        "Neem",
        "Sal",
        "Ashoka tree (Saraca asoca)",
        "Banyan tree (Ficus benghalensis)",
        "Bodhi tree (Ficus religiosa)",
        "Chorisia speciosa (silk floss tree)",
        "Dhak tree (Butea monosperma)",
        "Jamun tree (Syzygium cumini)",
        "Kikar tree (Prosopis cineraria)",
        "Peepal tree (Ficus religiosa)",
        "Saman tree (Samanea saman)",
        "Aegle marmelos (Bael tree)",
        "Albizia lebbeck (Flamboyant tree)",
        "Alstonia scholaris (Scholar tree)",
        "Amaltas tree (Cassia fistula)",
        "Barringtonia acutangula (Sea almond tree)",
        "Boswellia serrata (Frankincense tree)",
        "Calophyllum inophyllum (Santalum album (Sandalwood tree))**",
        "Cassia siamea (Siamese cassia)",
        "Chloroxylon swietenia (Scented wood tree)",
        "Cissus quadrangularis (Gooseberry vine)",
        "Dalbergia sissoo (Sheesham tree)",
        "Dillenia indica (Indian cork tree)",
        "Eucalyptus globulus (Blue gum)",
        "Ficus benghalensis (Banyan tree)",
        "Grewia robusta (Tamarind tree)",
        "Holoptelea integrifolia (Indian Elm tree)",
        "Hyphaene thebaica (Date palm)",
        "Inga vera (Pithecellobium dulce (Monkeypod tree))**",
        "Jacaranda mimosifolia (Jacaranda tree)",
        "Lagerstroemia indica (Crape myrtle)",
        "Mimusops elengi (Plumeria tree)",
        "Nyctanthes arbor-tristis (Night jasmine tree)",
        "Peltophorum pterocarpum (Flame of the forest tree)",
        "Pinus roxburghii (Chilgoza pine tree)",
        "Pterocarpus santalinus (Red sandalwood tree)",
        "Terminalia arjuna (Arjun tree)",
        "Tamarindus indica (Tamarind tree)",
        "Vitex trifolia (Indian privet tree)",
        "Sterculia guttata (Kapok tree)",
        "Wrightia tinctoria (Indian privet)",
        "Grevillea robusta (Silk oak)",
        "Mimusops elengi (Plumeria tree)",
        "Nyctanthes arbor-tristis (Night jasmine tree)",
        "Peltophorum pterocarpum (Flame of the forest tree)",
        "Pinus roxburghii (Chilgoza pine tree)",
        "Prosopis cineraria (Kikar tree)",
        "Pterocarpus santalinus (Red sandalwood tree)"
    ]
    return JsonResponse(tree_species, safe=False)


def survey_pdf(request):
    with open('media/tree-survey-guide.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
    return response
