import json
import os
import pdfkit
import pydf
import uuid

from django import template
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UploadTemplateSerializer
from .models import UploadTemplate


class UploadDocument(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    # ToDo:Add checks for the file uploaded - Done
    # ToDo:Add checks - Done
    # ToDo:Add User Authentication

    def request_parameters_check(self, request):
        name = request.data.get('name')  # Reading up name from the request
        file = request.data['file']  # Reading up file from the request
        event_name = request.data.get('event_name')
        k = [name, file, event_name]
        if None in k:
            Response.status_code = 400
            return Response({"err": "Enter all parameters properly"})

    def template_converter(self, request, temp):
        parameters = request.data.get('parameters')  # To change file according to the parameters passed to the user
        print(parameters)
        parameters = json.loads(parameters)
        for i in parameters:
            print(i)
            string = '{{ '+i+' }}'
            temp = temp.replace(i, string)
        return temp

    def post(self, request):
        print(request.data)
        # ToDo:To add user authentication here
        check = self.request_parameters_check(request)

        file = request.data['file'].read().decode('utf-8')
        if check:
            return check
        template = self.template_converter(request, file)
        UploadTemplate.objects.create(name=request.data.get('name'),
                                      file=template,
                                      event_name=request.data.get('event_name'),
                                      user=request.user)
        Response.status_code = 201
        return Response({"msg": "done"})


class GeneratePDF(APIView):
    permission_classes = [IsAuthenticated]

    def parameters_check(self, request):

        if 'template_name' not in request.data or 'parameters' not in request.data:
            Response.status_code = 400
            return Response({"err": "template name and parameters need to be provided"})

    def render_content(self, request, file, parameters):
        temp = template.Template(file)
        parameters = json.loads(parameters)
        values = {**parameters}
        context = template.Context(values)

        return temp.render(context)

    def generate_pdf(self, content):
        try:
            name = str(uuid.uuid4())+".pdf"
            #pdfkit.from_string(content, name)  # To be used if nothing works
            pdf = pydf.generate_pdf(content)
            with open(name, 'wb') as f:
                f.write(pdf)

            return os.path.abspath(name)
        except Exception as e:
            print(e)

    def download(self, file_path, filename):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename={}.pdf'.format(filename)
        os.remove(file_path)
        return response

    def post(self, request):
        check = self.parameters_check(request)
        if check:
            return check
        template_name = request.data.get('template_name')
        info = request.data.get('parameters')
        if 'download_file_name' not in request.data:
            download_file_name = 'download'
        else:
            download_file_name = request.data.get('download_file_name')
        file = UploadTemplate.objects.filter(name=template_name)
        if not file:
            Response.status_code = 404
            return Response({"err": "file doesnt exist"})
        content = self.render_content(request, file[0].file, info)+""
        print(content)
        pdf_path = self.generate_pdf(content)
        if pdf_path:
            return self.download(pdf_path, download_file_name)
        else:
            Response.status_code = 500
            return Response({"err": "unable to generate pdf"})


# ToDo: Put the available template for the selected user
class AvailableTemplateViewsForUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = UploadTemplate.objects.filter(user=request.user)
        data = UploadTemplateSerializer(queryset, many=True)
        return Response(data.data)



















