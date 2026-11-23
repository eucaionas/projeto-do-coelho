class VisitasMiddleware:
    """Usa a SESSÃO para contar as páginas visitadas pelo usuário logado."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.method == 'GET':
            request.session['visitas'] = request.session.get('visitas', 0) + 1
        return self.get_response(request)
