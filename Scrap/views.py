from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse, Http404
import requests
from bs4 import BeautifulSoup
import os
from django.conf import settings
from django.http import FileResponse

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        # print('paisi')
        # print(os.path.basename(file_path))
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    
        
    # raise Http404


def scrap(request):

    if request.method == 'POST':
        # print('yes')
        find = request.POST.get('search','')
        movie = find
        # print(find)
        url = "https://www.google.com/search?q="
        find = find.strip()
        find+=" english subtitle subscene"
        find = find.split(' ')
        find = [word.lower() for word in find]

        try:
            
            url = url + '+'.join(find)
            # print(url)
            google_url_data = requests.get(url)
            soup = BeautifulSoup(google_url_data.text,'html.parser')
            init_links = soup.find_all('a')
            # print(init_links)
            sub_links = []
            
        except:
            pass
            


        try:
            for link in init_links:
                header_3 = link.find_all('h3')
                count = 0
                for header in header_3:
                    if header:
                        header_text = header.text.lower()
                        # print(header_text)
                        for word in find:
                            # print(word)
                            if word in header_text.split():
                                count+=1
                if count==len(find):
                    sub_links.append(link['href'])
        except:
            pass
            
        
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
            pass
            



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
            return redirect('/scrap')

            

            
        except:
            pass
    

        
        
    

    else:
        return render(request, 'Scrap/scrap.html')