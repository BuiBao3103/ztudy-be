from django.shortcuts import render

def chat_room(request, code_invite):
    return render(request, 'chat/index.html', {'code_invite': code_invite})
