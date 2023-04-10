from django.shortcuts import render, redirect

from .utils import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .decorators import *
from .models import *
from .forms import CreateUserForm

from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout



# Create your views here.

def index(request):
    if request.user.is_authenticated:
        authenticate = True
    else:
        authenticate = False
    return render(request, 'index.html' , {'authenticate':authenticate})


def service(request):
    return  render(request, 'service.html')


def about(request):
    return  render(request, 'about.html')


def prediction(request):
    return render(request, 'prediction.html' ,{'uploaded':True,'file_url':True})

def contact(request):
    return  render(request, 'contact.html')


def after_proccess(request):

    # Getting last uploaded image
    image = upload.objects.last()


    # Removing Background
    print("Removing Image background") 
    removed_bg = Removed_bg_Image(image.image)
    print("Removed Image background")
    
    #Reading RGB Image 
    rgb_image = Read_Image(removed_bg)     


    # Converting to gray
    gray_image = Gray_Scale_Image(rgb_image)

    # Converting to equalized
    eq_hist = Equalized_Hist(gray_image)

    # Plotting histograms
    # plt.hist(gray_image.flatten(), bins=255, range=(0,255))
    # eq_fig = plt.hist(eq_hist.ravel(), bins=256, color='r', alpha=0.5)
    # plt.savefig(f'media/GrayScale_Histogram/{image.image}')
    # eq_fig.savefig(f'media/Equalized_Histogram/{image.image}')

    # Converting to Binary
    binary_image = Binary_Image(gray_image)
    print("Binary Image done") 

    # Converting to Morphology
    Morph_image = Morphology_Image(binary_image)
    print("Morphological Image done") 

    # Figuring out number of infected region
    Contour, leaf_Area, infected_area, Number_of_contour   = Contours(binary_image)
    print("Contours done") 
    print("Total Contours",len(Contour))

    # Drawing image of number of infected region
    spot_on_org_img, black_img = Contours_On_Orinial(rgb_image, Contour)
    
    # Saving Images 
    Save_Images(image.image, removed_bg, gray_image, eq_hist, binary_image, Morph_image, spot_on_org_img, black_img)

    # infected = upload.objects.create(InfectedRegion=spot_on_org_img)
    # infected.save()

    # Mathematical calculation to convert the area of pixels into cm^2
    leaf_Area = round(0.0624583333*leaf_Area,3)
    infected_area = round(0.0624583333*infected_area,3)
    print("Model renders")  
    

    # Mathematical calculation to find the ratio
    Ratio = round(infected_area/leaf_Area,2)*100

    # Indicating the level by number of spots
    if Number_of_contour >= 98:
        Severe = "Severe"
    elif Number_of_contour <= 98 and Number_of_contour >= 50:
        Severe = "Moderate"
    else:
        Severe = "Low"
    found_disease = "Leaf Spot"
    Treatment = """Leaf spot disease in sugarcane can be caused by various fungi, bacteria, and viruses, and its severity can vary depending on the pathogen and environmental conditions. Here are some general steps to manage leaf spot disease in sugarcane:
                    1. Sanitation: Remove and destroy infected plant debris to prevent the spread of the disease.
                    2. Fungicides: Apply fungicides according to the manufacturer's instructions and based on the severity of the disease. Fungicides can help control leaf spot, but they should be used judiciously to avoid the development of resistance.
                    3. Crop rotation: Rotate sugarcane with other crops to break the disease cycle.
                    4. Resistant varieties: Plant sugarcane varieties that are resistant or tolerant to the disease.
                    5. Nutrient management: Properly manage soil fertility to promote healthy plant growth and reduce susceptibility to disease"""
    
    print("Hurrah! Successfully done")

    Disease_classification = [
      { "label": "Red Rot", "y": 5 },
      { "label": "Mosaic Virus", "y": 5 },
      { "label": "Leaf spot", "y": 50 },
      { "label": "Red Rust", "y": 20 },
      { "label": "Bacterial Blight", "y": 10 },
      { "label": "Mite Insect", "y": 10 }
    ]

    context = {'preprocess_url':image.image , 'leaf_Area': leaf_Area , 'Num_of_contour':Number_of_contour,
               'infected_area':infected_area , 'Ratio':Ratio, 'Severe':Severe , 'uploaded':False,
               'found_disease':found_disease,
               'Treatment':Treatment , "Disease_classification" : Disease_classification}
    return  render(request, 'prediction.html', context)

def uploaded(request):
    try:
        print("uploading..........")
        uploaded = request.FILES['original_image']
        upl = upload.objects.create(image=uploaded)
        upl.save()
        print("Sucessfully uploaded Image")
        return after_proccess(request)

    except Exception as error:
        print("error occured: ",error)
        return render(request, 'prediction.html', {'uploaded':True , 'file_url':True})



def piechart(request):
    monthly_expense_data = [
      { "label": "Red Rot", "y": 5 },
      { "label": "Mosaic Virus", "y": 5 },
      { "label": "Leaf spot", "y": 50 },
      { "label": "Red Rust", "y": 20 },
      { "label": "Bacterial Blight", "y": 10 },
      { "label": "Mite Insect", "y": 10 }
    ]

    return render(request, 'piechart.html', {"monthly_expense_data" : monthly_expense_data})  



@unauthenticated_user
def register(request):
    form = CreateUserForm()
    print("created") 
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = CreateUserForm(request.POST)
            print("submit") 
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('email')
                group = Group.objects.get(name='user')
                user.groups.add(group)
        elif 'signin' in request.POST:
            print("login")
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
        
    return render(request, 'authentication.html', {'form': form})

def logout_Page(request):
    logout(request)
    return redirect('home')

def user_page(request):
    context = {}
    return render(request, 'index.html',context)

            

