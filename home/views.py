from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from pynput.keyboard import Key, Controller
from django.template import loader

keyboard = Controller()

curr_displaying = None
order = 0
result_no = 0
_order = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}


def home(request):
    return render(request, 'index.html')


def fetch(request):

    global curr_displaying

    query = request.GET.get('query').lower()

    if 'full screen' in query and curr_displaying:
        if curr_displaying['type'] == 'youtube':
            keyboard.press('f')
            keyboard.release('f')

        success_data = {
            'type': 'nothing'
        }

        return JsonResponse(success_data)

    else:

        # youtube_video
        video_id = play_youtube(query)

        success_data = {
            'type': 'youtube',
            'keyword': query,
            'link': 'https://www.youtube.com/watch?v='+video_id+'?&autoplay=1'
        }

        curr_displaying = success_data

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
