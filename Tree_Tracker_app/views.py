from json import dumps
import requests
from django.shortcuts import render , redirect
from django.http import JsonResponse,HttpResponse
from .models import Survey
from geopy.geocoders import Nominatim
import random


def index(request):
    if request.method=='POST':
        try:
            place = request.POST.get('Location')
            if not place:
                raise ValueError("Location not provided")
            geolocator = Nominatim(user_agent="MyGeocodingApp/1.0")
            location = geolocator.geocode(place)
            if location:
                latitude = int(location.latitude)
                longitude = int(location.longitude)
            else:
                raise ValueError("Incorrect location")
            survey_data = []
            density_map = {}
            for obj in Survey.objects.all():
                rounded_latitude = int(obj.latitude)
                rounded_longitude = int(obj.longitude)

                if rounded_latitude == latitude and rounded_longitude == longitude:
                    key = (rounded_latitude, rounded_longitude)
                    density_map[key] = density_map.get(key, 0) + 1

                    survey_data.append({
                        'latitude': obj.latitude,
                        'longitude': obj.longitude,
                        'species': obj.species,
                        'tree_height': obj.tree_height,
                        'steam_diameter': obj.steam_diameter,
                        'crown_height': obj.crown_height,
                        'crown_diameter': obj.crown_diameter,
                        'spreading': obj.spreading,
                        'crown_damage': obj.crown_damage,
                        'trunk_damage': obj.trunk_damage,
                    })
            count = len(survey_data)
            unique_species = set()

            for obj in survey_data:
                unique_species.add(obj["species"])
               
            heatmap_data = [{'latitude': key[0], 'longitude': key[1], 'intensity': density_map[key]} for key in density_map]
            heatmap_data = dumps(heatmap_data)
            survey_data = dumps(survey_data)
            return render(request, 'index.html', context={'heatmap_data': heatmap_data, "data": survey_data, 'survey': count, 'species': len(unique_species)})
        
        except Exception as e:
            print(e)
            survey_objects = Survey.objects.all()
            survey_data=[]
            
            density_map = {}
            for obj in survey_objects:
                
                rounded_latitude = int(obj.latitude)
                rounded_longitude = int(obj.longitude)
                
                key = (rounded_latitude, rounded_longitude)
                if key not in density_map:
                    density_map[key] = 0
                density_map[key] += 1
                survey_data.append({
                    'latitude': obj.latitude,
                        'longitude': obj.longitude,
                        'species': obj.species,
                        'tree_height':obj.tree_height,
                        'steam_diameter':obj.steam_diameter,
                        'crown_height':obj.crown_height,
                        'crown_diameter':obj.crown_diameter,
                        'spreading': obj.spreading,
                        'crown_damage': obj.crown_damage,
                        'trunk_damage': obj.trunk_damage,
                })

            heatmap_data = [{'latitude': key[0], 'longitude': key[1], 'intensity': density_map[key]} for key in density_map]
            
            count = len(survey_data)
            getspecies= set(Survey.objects.values_list('species'))
            heatmap_data = dumps(heatmap_data)
            survey_data  = dumps(survey_data)
        return render(request, 'index.html', context={'heatmap_data': heatmap_data , "data" : survey_data ,'survey':count,'species':len(getspecies)})
    else:
        survey_objects = Survey.objects.all()
        survey_data=[]
        density_map = {}
        for obj in survey_objects:
            rounded_latitude = int(obj.latitude)
            rounded_longitude = int(obj.longitude)
            
            key = (rounded_latitude, rounded_longitude)
            if key not in density_map:
                density_map[key] = 0
            density_map[key] += 1
            
            survey_data.append({
                'latitude': obj.latitude,
                    'longitude': obj.longitude,
                    'species': obj.species,
                    'tree_height':obj.tree_height,
                    'steam_diameter':obj.steam_diameter,
                    'crown_height':obj.crown_height,
                    'crown_diameter':obj.crown_diameter,
                    'spreading': obj.spreading,
                    'crown_damage': obj.crown_damage,
                    'trunk_damage': obj.trunk_damage,
            })

        heatmap_data = [{'latitude': key[0], 'longitude': key[1], 'intensity': density_map[key]} for key in density_map]
        
        count = len(Survey.objects.all())
        getspecies= set(Survey.objects.values_list('species'))
        heatmap_data = dumps(heatmap_data)
        survey_data  = dumps(survey_data)
    return render(request, 'index.html', context={'heatmap_data': heatmap_data , "data" : survey_data ,'survey':count,'species':len(getspecies)})

def add(request):
    if request.method == 'POST':
            survey = Survey()
            survey.latitude = request.POST['latitude']
            survey.longitude = request.POST['longitude']
            survey.species = request.POST['species']
            survey.tree_height = float(request.POST['tree_height'])
            survey.steam_diameter = float(request.POST['trunk_diameter'])
            survey.crown_height = float(request.POST['crown_height'])
            survey.crown_diameter = float(request.POST['crown_diameter'])
            survey.spreading = request.POST['spreading']
            survey.crown_damage = request.POST['crown_dmg']
            survey.trunk_damage = request.POST['trunk_dmg']
            survey.reason_crown_damage = request.POST['reason_crown_dmg'] if 'reason_crown_dmg' in request.POST else 'Null'
            survey.reason_trunk_damage = request.POST['reason_trunk_dmg'] if 'reason_trunk_dmg' in request.POST else 'Null'
            survey.save()
        
    else:
        context = {}
    return render(request, 'add.html')

def map1(request):
    survey_objects = Survey.objects.all()
    survey_data=[]
    
    density_map = {}
    for obj in survey_objects:
        rounded_latitude = int(obj.latitude)
        rounded_longitude = int(obj.longitude)
        
        key = (rounded_latitude, rounded_longitude)
        if key not in density_map:
            density_map[key] = 0
        density_map[key] += 1
        
        survey_data.append({
            'latitude': obj.latitude,
                'longitude': obj.longitude,
                'species': obj.species,
                'tree_height':obj.tree_height,
                'steam_diameter':obj.steam_diameter,
                'crown_height':obj.crown_height,
                'crown_diameter':obj.crown_diameter,
                'spreading': obj.spreading,
                'crown_damage': obj.crown_damage,
                'trunk_damage': obj.trunk_damage,
        })
    heatmap_data = [{'latitude': key[0], 'longitude': key[1], 'intensity': density_map[key]} for key in density_map]
    return render(request, 'Analysis.html', context={'heatmap_data': heatmap_data , "data" : survey_data})


def survey_pdf(request):
    with open('media/tree-survey-guide.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
    return response

def facker(request):
    
    """tree_info = [
        ["Banyan Tree (Ficus benghalensis)", [20, 25], [3, 5], [30, 40], [15, 20]],
        ["Neem Tree (Azadirachta indica)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Teak (Tectona grandis)", [25, 30], [1.5, 2.5], [30, 35], [20, 25]],
        ["Mango Tree (Mangifera indica)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Peepal Tree (Ficus religiosa)", [20, 25], [3, 5], [30, 40], [15, 20]],
        ["Jamun Tree (Syzygium cumini)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Coconut Palm (Cocos nucifera)", [20, 30], [0.3, 0.5], [25, 30], [15, 20]],
        ["Tamarind Tree (Tamarindus indica)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Sandalwood (Santalum album)", [8, 10], [0.5, 1], [10, 15], [5, 8]],
        ["Mahogany (Swietenia mahagoni)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Jackfruit Tree (Artocarpus heterophyllus)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Sal Tree (Shorea robusta)", [20, 25], [1, 3], [25, 30], [15, 20]],
        ["Guava Tree (Psidium guajava)", [5, 10], [0.5, 1], [10, 15], [5, 8]],
        ["Gulmohar (Delonix regia)", [10, 15], [0.5, 1], [15, 20], [8, 10]],
        ["Ashoka Tree (Saraca asoca)", [8, 10], [0.5, 1], [10, 15], [5, 8]],
        ["Indian Rosewood (Dalbergia latifolia)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Laurel (Terminalia bellirica)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Gooseberry (Phyllanthus emblica)", [10, 15], [0.5, 1], [15, 20], [8, 10]],
        ["Indian Cork Tree (Millingtonia hortensis)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Indian Almond (Terminalia catappa)", [15, 20], [1, 2], [20, 25], [10, 15]],
        # Additional tree species
        ["Peepul (Ficus religiosa)", [20, 25], [3, 5], [30, 40], [15, 20]],
        ["Pongam (Pongamia pinnata)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Indian Beech (Pongamia glabra)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Indian Kino Tree (Pterocarpus marsupium)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Laurel (Litsea glutinosa)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Himalayan Cedar (Cedrus deodara)", [20, 30], [1.5, 3], [30, 35], [20, 25]],
        ["Silver Oak (Grevillea robusta)", [20, 25], [1, 2], [25, 30], [15, 20]],
        ["Indian Elm (Holoptelea integrifolia)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Indian Redwood (Adenanthera pavonina)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Indian Coral Tree (Erythrina variegata)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Java Plum (Syzygium cumini)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Beechwood (Pongamia glabra)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Indian Laburnum (Cassia fistula)", [20, 25], [1, 2], [25, 30], [15, 20]],
        ["Indian Silk Cotton Tree (Bombax ceiba)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Lilac (Melia azedarach)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Indian Jujube (Ziziphus mauritiana)", [5, 10], [0.5, 1], [10, 15], [5, 8]],
        ["Indian Redwood (Adenanthera pavonina)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Peepul (Ficus religiosa)", [20, 25], [3, 5], [30, 40], [15, 20]],
        ["Bael Tree (Aegle marmelos)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Indian Boxwood (Buxus sempervirens)", [5, 10], [0.5, 1], [10, 15], [5, 8]],
        ["Indian Beech (Pongamia glabra)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Indian Kino Tree (Pterocarpus marsupium)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Laurel (Litsea glutinosa)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Himalayan Cedar (Cedrus deodara)", [20, 30], [1.5, 3], [30, 35], [20, 25]],
        ["Silver Oak (Grevillea robusta)", [20, 25], [1, 2], [25, 30], [15, 20]],
        ["Indian Elm (Holoptelea integrifolia)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Indian Redwood (Adenanthera pavonina)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Indian Coral Tree (Erythrina variegata)", [15, 20], [1, 2], [20, 25], [10, 15]],
        ["Java Plum (Syzygium cumini)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Beechwood (Pongamia glabra)", [10, 15], [1, 2], [15, 20], [8, 10]],
        ["Indian Laburnum (Cassia fistula)", [20, 25], [1, 2], [25, 30], [15, 20]],
        ["Indian Silk Cotton Tree (Bombax ceiba)", [15, 20], [1, 3], [20, 25], [10, 15]],
        ["Indian Lilac (Melia azedarach)", [10, 15], [0.5, 1.5], [15, 20], [8, 10]],
        ["Indian Jujube (Ziziphus mauritiana)", [5, 10], [0.5, 1], [10, 15], [5, 8]]
    ]

    trunk_damage_factors = [
        "Insect infestation",
        "Fungal infection",
        "Physical injury (e.g., vehicle collision)",
        "Improper pruning",
        "Environmental stress (e.g., drought)",
        "Lightning strike",
        "Fire damage",
        "Construction damage (e.g., excavation)",
        "Herbivore damage (e.g., browsing by animals)",
        "Disease (e.g., bacterial infection)"
    ]

    crown_damage_factors = [
        "Storm damage (e.g., high winds)",
        "Heavy snow or ice load",
        "Disease (e.g., fungal infection)",
        "Insect infestation (e.g., defoliators)",
        "Pruning damage (e.g., improper pruning cuts)",
        "Nutrient deficiency",
        "Sunburn or heat stress",
        "Mechanical damage (e.g., from equipment)",
        "Excessive shading from neighboring trees",
        "Pollution (e.g., air pollutants)"
    ]

    spreading = ['oval' , 'cube' , 'fan' , 'columnal' ,'cone']
    # Load Natural Earth dataset for land and country boundaries
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Filter India's land boundary
    india = world[world.name == 'India']

    # Extract India's land boundary geometry
    india_land = india.geometry.values[0]

    forest_cover_data = {
        'Andhra Pradesh': 23.4,    # Hypothetical forest cover percentage for Andhra Pradesh
        'Arunachal Pradesh': 68.9, # Hypothetical forest cover percentage for Arunachal Pradesh
        'Assam': 32.5,             # Hypothetical forest cover percentage for Assam
        'Bihar': 10.7,             # Hypothetical forest cover percentage for Bihar
        'Chhattisgarh': 41.2,      # Hypothetical forest cover percentage for Chhattisgarh
        'Goa': 55.6,               # Hypothetical forest cover percentage for Goa
        'Gujarat': 7.8,            # Hypothetical forest cover percentage for Gujarat
        'Haryana': 3.2,            # Hypothetical forest cover percentage for Haryana
        'Himachal Pradesh': 37.1,  # Hypothetical forest cover percentage for Himachal Pradesh
        'Jharkhand': 29.8,         # Hypothetical forest cover percentage for Jharkhand
        'Karnataka': 22.3,         # Hypothetical forest cover percentage for Karnataka
        'Kerala': 50.2,            # Hypothetical forest cover percentage for Kerala
        'Madhya Pradesh': 34.6,    # Hypothetical forest cover percentage for Madhya Pradesh
        'Maharashtra': 16.5,       # Hypothetical forest cover percentage for Maharashtra
        'Manipur': 55.7,           # Hypothetical forest cover percentage for Manipur
        'Meghalaya': 67.2,         # Hypothetical forest cover percentage for Meghalaya
        'Mizoram': 74.3,           # Hypothetical forest cover percentage for Mizoram
        'Nagaland': 58.9,          # Hypothetical forest cover percentage for Nagaland
        'Odisha': 32.6,            # Hypothetical forest cover percentage for Odisha
        'Punjab': 6.4,             # Hypothetical forest cover percentage for Punjab
        'Rajasthan': 4.1,          # Hypothetical forest cover percentage for Rajasthan
        'Sikkim': 64.8,            # Hypothetical forest cover percentage for Sikkim
        'Tamil Nadu': 21.6,        # Hypothetical forest cover percentage for Tamil Nadu
        'Telangana': 24.7,         # Hypothetical forest cover percentage for Telangana
        'Tripura': 55.1,           # Hypothetical forest cover percentage for Tripura
        'Uttar Pradesh': 16.9,     # Hypothetical forest cover percentage for Uttar Pradesh
        'Uttarakhand': 46.5,       # Hypothetical forest cover percentage for Uttarakhand
        'West Bengal': 15.8        # Hypothetical forest cover percentage for West Bengal
    }

    # Define regions based on forest cover
    regions = {
        'High Greenery': ['Arunachal Pradesh', 'Goa', 'Kerala', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura', 'Uttarakhand'],
        'Moderate Greenery': ['Assam', 'Chhattisgarh', 'Himachal Pradesh', 'Jharkhand', 'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Telangana'],
        'Low Greenery': ['Andhra Pradesh', 'Bihar', 'Gujarat', 'Haryana', 'Karnataka', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Uttar Pradesh', 'West Bengal']
    }

    # Convert forest cover data to probabilities for biasing
    total_forest_cover = sum(forest_cover_data.values())
    forest_cover_probs = {state: cover / total_forest_cover for state, cover in forest_cover_data.items()}

    def generate_random_coords_within_india():
        while True:
            # Choose a region based on forest cover probabilities
            region = random.choices(list(regions.keys()), weights=[sum(forest_cover_probs[state] for state in states) for states in regions.values()])[0]
            
            # Choose a state within the selected region
            state = random.choice(regions[region])
            
            # Generate random coordinates within the bounds of the selected state (simplified for demonstration)
            # You would need more detailed boundaries for accurate results
            min_lat, max_lat = 8.4, 20.0  
        
            # Longitude range: 68.7°E to 89°E (Adjusted for South India)
            min_lon, max_lon = 68.7, 89.0 
            latitude = random.uniform(min_lat, max_lat)
            longitude = random.uniform(min_lon, max_lon)
            
            # Create a Shapely Point object from the coordinates
            point = Point(longitude, latitude)
            
            # Return the coordinates if they fall within the selected state
            if point.within(india_land):
                return latitude, longitude

    for i in range(200):
        survey = Survey()
        
        lat,lon = generate_random_coords_within_india()
        survey.latitude =lat
        survey.longitude=lon
        
        tree = random.choice(tree_info)
        survey.species = tree[0]
        survey.tree_height  = round(random.uniform(tree[1][0] , tree[1][1]),3)
        survey.steam_diameter = round(random.uniform(tree[2][0] , tree[2][1]) , 3)
        survey.crown_diameter = round(random.uniform(tree[3][0] , tree[3][1]) , 3)
        survey.crown_height = round(random.uniform(tree[4][0] , tree[4][1]) , 3)
        survey.spreading = random.choice(spreading)
        survey.trunk_damage = round(random.uniform(0 , 80),3)
        survey.reason_trunk_damage  = random.choice(trunk_damage_factors)
        survey.crown_damage = round(random.uniform(0,80) , 3)
        survey.reason_crown_damage  = random.choice(crown_damage_factors)
        survey.save()"""
        
    return redirect('index')
