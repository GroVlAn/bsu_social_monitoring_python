def create_organization(request, form) -> None:
    form.save()
    form.save(user=request.user)
