from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse, Http404
import requests
from bs4 import BeautifulSoup
import os
from django.conf import settings
from django.http import FileResponse
import re


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        # print('paisi')
        # print(os.path.basename(file_path))
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            # os.remove(file_path)
            return response
    
        
    # raise Http404


def scrap(request):

    if request.method == 'POST':
        
        mydir = settings.MEDIA_ROOT
        for file in os.listdir(mydir):
            os.remove(os.path.join(mydir, file))
        # print('yes')
        find = request.POST.get('search','')
        movie = find
        # print(find)
        url = "https://www.google.com/search?q="
        find = find.strip()
        find = re.sub(r'[^\w\s]', ' ', find)
        # print(find)
        find+=" english subtitle subscene"
        find = ' '.join(find.split())

        try:
            
            url = url + '+'.join(find.split())
            # print(url)
            google_url_data = requests.get(url)
            soup = BeautifulSoup(google_url_data.text,'html.parser')
            init_links = soup.find_all('a')
            # print(init_links)
            sub_links = []
            
        except:
            return render(request, 'Scrap/scrap.html',{'not_found': 'Something Went Wrong! Try Input a Valid Movie Name.'})
            


        try:
            for link in init_links:
                header_3 = link.find_all('h3')
                for header in header_3:
                    count = 0
                    if header:
                        header_text = header.text.lower()
                        header_text = re.sub(r'[^\w\s]', ' ', header_text)
                        header_text = ' '.join(header_text.split())
                        # print(header_text)
                        if 'english subtitle subscene' in header_text and 'search results' not in header_text:
                            count = 1
                    if count>0:
                        sub_links.append(link['href'])
        except:
            return render(request, 'Scrap/scrap.html',{'not_found': 'Something Went Wrong! Try Input a Valid Movie Name.'})
            
        
        try:
            link = sub_links[0]
            link = link.split("&")[0]
            
            link = link.split('=')[1]
            # print(link)
            subscene_page_data = requests.get(link)
            soup_subscene = BeautifulSoup(subscene_page_data.text,'html.parser')
            # print(soup_subscene)
            final_link = "https://subscene.com"
        except:
            return render(request, 'Scrap/scrap.html',{'not_found': 'Something Went Wrong! Try Input a Valid Movie Name.'})
            



        try:
            data = soup_subscene.findAll('div',attrs={'class':'download'})
            # print(data)
            for div in data:
                links = div.findAll('a')
                for a in links:
                    final_link+=a['href']
            # print(final_link)
            r = requests.get(final_link)
            # print(r)
            file = open('media/'+movie+'.zip', 'wb')
            file.write(r.content)
            
            # print('File is saved at ' + file.name)
            response = download(request, movie+'.zip')
            
            # os.remove(file_path)
            return response

            

            
        except:
            return render(request, 'Scrap/scrap.html',{'not_found': 'The Movie Not Found, Please Input A Valid Movie Name.'})
    
        return redirect('/scrap')
        
        
    

    else:
        return render(request, 'Scrap/scrap.html')