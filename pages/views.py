from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import TemplateView # Import TemplateView

# Create your views here.
def homePageView(request):
	template = loader.get_template("index.html")
	return HttpResponse(template.render())


# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"