from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from pynput.keyboard import Key, Controller
from django.template import loader
import os

keyboard = Controller()

paths = {
    'video': '/media/akv26/AKVINDIAN/Bollywood Video Songs/'
}

curr_displaying = None


def home(request):
    return render(request, 'index.html')


def fetch(request):

    global curr_displaying

    query = request.GET.get('query').lower()

    if 'youtube' in query:

        video_id = play_youtube(query.replace('youtube ', ''))

        success_data = {
            'type': 'youtube',
            'keyword': query,
            'link': 'https://www.youtube.com/watch?v='+video_id+'?&autoplay=1'
        }

        curr_displaying = success_data

        return JsonResponse(success_data)

    elif 'play' in query or 'play video' in query:

        query = query.replace('play video', '')
        query = query.replace('play', '')

        ls_ = os.listdir(paths['video'])

        ls = []
        opened_file = False
        for i in range(len(ls_)):
            ls.append({
                'id': i+1,
                'title': ls_[i]
            })
            if query in ls_[i].lower() and not opened_file:
                os.open(paths['video']+ls_[i], os.O_RDONLY)
                opened_file = True
                print(paths['video']+ls_[i])

        success_data = {
            'type': 'display',
            'html': loader.render_to_string('display_list.html', {'list': ls})
        }

        curr_displaying = success_data

        return JsonResponse(success_data)

    if 'full screen' in query and curr_displaying:

        if curr_displaying['type'] == 'youtube':
            keyboard.press('f')
            keyboard.release('f')

        success_data = {
            'type': 'nothing'
        }

        return JsonResponse(success_data)

    # return JsonResponse({'type': 'error'})


def play_youtube(search_query):

    import urllib.request
    from bs4 import BeautifulSoup

    if search_query:
        search_query = urllib.parse.quote(search_query)
        url = "https://www.youtube.com/results?search_query=" + search_query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            vid_id = vid['href'][9:]
            return vid_id
    else:
        return None
