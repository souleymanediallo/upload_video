from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from pytube import YouTube
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape


# Create your views here.
def home(request):
    videos_folder = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = os.listdir(videos_folder)
    videos = [f for f in video_files if os.path.isfile(os.path.join(videos_folder, f))]

    if request.method == 'POST':
        video_url = request.POST['video_url']
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        download_folder = os.path.join('media', 'videos')
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        video_path = stream.download(output_path=download_folder)
        video_filename = os.path.basename(video_path)
        video_full_path = os.path.join(download_folder, video_filename)
        return FileResponse(open(video_full_path, 'rb'), as_attachment=True)
    context = {'videos': videos}
    return render(request, 'pages/index.html', context)


@csrf_exempt
def delete_video(request):
    if request.method == 'POST':
        video_name = request.POST.get('video_name')
        video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_name)
        if os.path.exists(video_path):
            os.remove(video_path)
            return JsonResponse({'message': 'Video deleted successfully.'})
        else:
            return JsonResponse({'message': 'Video not found.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
