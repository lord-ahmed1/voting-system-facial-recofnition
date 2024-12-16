from django.shortcuts import render ,HttpResponse , HttpResponseRedirect
from .models import VotesCollection,VotesAndVoters , Checker
import json
from django.contrib.auth.decorators import login_required 
from users.models import Profile
from .forms import CheckerForm
from django.contrib import messages
import face_recognition
import cv2 as cv
import os

def encoder(img_path):
    img=face_recognition.load_image_file(img_path)
    img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
 
    face_encoding=face_recognition.face_encodings(img)[0]
    return face_encoding


def compare(img1,img2):
    img1_encoding=encoder(img1)
    img2_encoding=encoder(img2)
    result=face_recognition.compare_faces([img1_encoding],img2_encoding)
    return result[0]



def home(request):
    votes=VotesCollection.objects.values('title')
    VotesAndVoters.objects
    votes=[vote["title"] for vote in votes]
    return render(request,'mainpage.html',{'all_elements':votes})
@login_required

def current_vote_handler(request,current_vote):
    
    data=VotesCollection.objects.get(title=current_vote)
    candidates=data.candidates
    candidates_json=json.loads(candidates)
        
    if request.method=="GET":
        check_face=CheckerForm()
        return render(request,'voting.html',{'all_elements':candidates_json,"vote_title":current_vote,'check_face':check_face})


    if request.method=="POST":

        

       
        


        username=request.user.username
        user=Profile.objects.get(id=request.user.id)
        contact_number=user.contact_number
        cpf=user.cpf
        original_person=request.user.profile.avatar.url[1:]
        
        if contact_number=='' or cpf=='' or original_person=="media/default.jpg":
            messages.warning(request,'incomplete profile')
            return HttpResponseRedirect('/profile/')
            
        voted_before=VotesAndVoters.objects.filter(vote_title=current_vote,voter_username=username).first()
            

        if voted_before != None:
            messages.info(request,"you voted here already!")
            return HttpResponseRedirect('/votes/')
            

            
            
       

        check_face=CheckerForm(request.POST, request.FILES)
        check_face.save()
        image_filename=check_face.files['img']
        check_image_path=f'media/check/{image_filename}'
        
       
        compare_result=compare(check_image_path,original_person)
        os.remove(check_image_path)


        if compare_result:

            save_voter=VotesAndVoters(vote_title=current_vote,voter_username=username)
            save_voter.save()
        
            chosen=request.POST.get("chosen")
            
            candidates_json[chosen]+=1
            string=json.dumps(candidates_json)
            candidates=string
            data.candidates=string
            data.save()
        else:
            messages.warning(request,"we didn't recognize your face !")
            return HttpResponseRedirect("/")
            
        

        messages.success(request,"your choice has been recorded")
        return HttpResponseRedirect("/votes/")
        

        
    
    

# Create your views here.
