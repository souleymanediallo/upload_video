from django.shortcuts import render, redirect
from django.http import FileResponse
from pytube import YouTube
import os


# Create your views here.
def home(request):
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
    return render(request, 'pages/index.html')


def video_list(request):
    video_folder = os.path.join('templates', 'videos')
    videos = os.listdir(video_folder)
    videos_path = [os.path.join('videos', video) for video in videos]
    context = {'videos': videos, 'videos_path': videos_path}
    return render(request, 'pages/video_list.html', context)
