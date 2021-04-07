import io
import mimetypes
import os
import posixpath
from pathlib import Path
from PIL import Image

import wget
from django.http import (
    FileResponse, Http404, HttpResponse, HttpResponseNotModified,
)
from django.shortcuts import redirect, render
from django.utils._os import safe_join
from django.utils.http import http_date
from django.utils.translation import gettext as _
from django.views.static import directory_index, was_modified_since

from mysite.settings import BASE_DIR
from pill.forms import Images


def index(request):
    if request.method == 'POST':
        image = Images(request.POST, request.FILES)
        if image.is_valid():
            file_field = image.cleaned_data["file"]
            url_field = image.cleaned_data["url"]
        if (file_field is None and len(url_field) == 0) or (file_field is not None and len(url_field) > 0):
            return HttpResponse('Select only one method or fill in only one field')
        elif file_field is not None and len(url_field) == 0:
            image.save()
            return redirect('index')
        else:
            image_filename = wget.download(url_field, out=os.path.join(BASE_DIR, 'media/images'))
            image.save()
            return redirect('index')
    else:
        image = Images()
        return render(request, 'index.html', {'form': image})


def home(request):
    img_list = os.listdir('media/images/')
    return render(request, 'home.html', {'imgs': img_list})


def resize(request, filename):
    width = request.GET.get('width')
    height = request.GET.get('height')
    return render(request, 'resize_img.html', {'image_name': filename,
                                               'image_src': f'{filename}?w={width}&h={height}'})


def serve_static(request, path, document_root=None, show_indexes=False):
    path = posixpath.normpath(path).lstrip('/')
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_dir():
        if show_indexes:
            return directory_index(path, fullpath)
        raise Http404(_("Directory indexes are not allowed here."))
    if not fullpath.exists():
        raise Http404(_('“%(path)s” does not exist') % {'path': fullpath})
    # Respect the If-Modified-Since header.
    statobj = fullpath.stat()
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(str(fullpath))
    content_type = content_type or 'application/octet-stream'

    image = Image.open(fullpath)

    width, height = image.size

    try:
        req_width = int(request.GET.get('w'))
    except Exception:
        req_width = None
    try:
        req_height = int(request.GET.get('h'))
    except Exception:
        req_height = None

    if req_width is not None:
        req_height = int(req_width * height / width)
    elif req_height is not None:
        req_width = int(req_height * width / height)
    else:
        req_width = width
        req_height = height

    image = image.resize((req_width, req_height), Image.ANTIALIAS)
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    response = FileResponse(output, content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response["Content-Encoding"] = encoding
    return response

