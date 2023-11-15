from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from django.shortcuts import render, redirect


def bus_app_page(request):
    return render(request, 'main.html')
class Conductor(LoginRequiredMixin,View):
    # Especifico la plantilla o template que usaré
    template_name = "index.html"
    def user_is_superuser(self):
        return self.request.user.is_superuser

    

    def get(self, request):
        if self.request.user.is_superuser:
            # Acceder a la base de datos para conductores
            ref_conductores = db.reference('Users/Conductor')
            datos_conductores = ref_conductores.get()

            # Llamar al método estático para obtener los reportes
            datos_reportes = Conductor.lista_reportes()

            # Combinar los datos en un solo contexto
            contexto = {
                "Conductor": datos_conductores,
                "Reportes": datos_reportes
            }

            # Envía los datos combinados a la vista o template
            return render(request, self.template_name, contexto)
        else:
            # Si el usuario no es un superusuario, redirigir a otra página o mostrar un mensaje de error
            return render(request, "no_access.html")
    
    @staticmethod
    def lista_reportes():
        ref_reportes = db.reference('Reporte')
        todos_los_reportes = ref_reportes.get()

        lista_reportes = []
        if todos_los_reportes:
            for tipo, reportes in todos_los_reportes.items():
                for reporte_id, reporte_data in reportes.items():
                    reporte = {
                        'tipoReporte': tipo,
                        'nombreConductor': reporte_data.get('fullName'),
                        'telefono': reporte_data.get('phone'),
                        'patente': reporte_data.get('patentNumber'),
                        'fechahora': reporte_data.get('fechaHoraReporte'),
                        # ... otros campos que necesites ...
                    }
                    lista_reportes.append(reporte)
        return lista_reportes


class AgregarConductor(View):
    template_name = "agregar_conductor.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Obtener datos del formulario
        company = request.POST.get('company')
        email = request.POST.get('email')
        emergencyPhone = request.POST.get('emergencyPhone')
        fullName = request.POST.get('fullName')
        patentNumber = request.POST.get('patentNumber')
        phone = request.POST.get('phone')

        # Nuevos campos: Hora de Inicio, Hora de Fin y Ruta
        horario_inicio = request.POST.get('horario_inicio')
        horario_fin = request.POST.get('horario_fin')
        ruta = request.POST.get('ruta')

        ref = db.reference('Users/Conductor')
        new_conductor_ref = ref.push()
        new_conductor_ref.set({
            'company': company,
            'email': email,
            'emergencyPhone': emergencyPhone,
            'fullName': fullName,
            'patentNumber': patentNumber,
            'phone': phone,
            'horario_inicio': horario_inicio,
            'horario_fin': horario_fin,
            'ruta': ruta
        })

        return redirect('index')  # Redirigir a la lista de conductores


class ModificarConductor(View):
    template_name = "modificar_conductor.html"

    def get(self, request, conductor_id):
        ref = db.reference('Users/Conductor/' + conductor_id)
        conductor = ref.get()

        # Añade el valor del campo "ruta" al contexto
        ruta = conductor.get('ruta', '')  # Si no hay un valor en la base de datos, establece un valor predeterminado vacío
        conductor['ruta'] = ruta

        return render(request, self.template_name, {'conductor': conductor})

    def post(self, request, conductor_id):
        # Obtener referencia al conductor en Firebase
        ref = db.reference('Users/Conductor/' + conductor_id)

        # Obtener datos del formulario
        company = request.POST.get('company')
        email = request.POST.get('email')
        emergencyPhone = request.POST.get('emergencyPhone')
        fullName = request.POST.get('fullName')
        patentNumber = request.POST.get('patentNumber')
        phone = request.POST.get('phone')

        # Nuevos campos: Hora de Inicio, Hora de Fin y Ruta
        horario_inicio = request.POST.get('horario_inicio')
        horario_fin = request.POST.get('horario_fin')
        ruta = request.POST.get('ruta')

        
        # Actualizar los datos en Firebase
        ref.update({
            'company': company,
            'email': email,
            'emergencyPhone': emergencyPhone,
            'fullName': fullName,
            'patentNumber': patentNumber,
            'phone': phone,
            'horario_inicio': horario_inicio,
            'horario_fin': horario_fin,
            'ruta': ruta
        })

        return redirect('index')


    
class EliminarConductor(View):
    def get(self, request, conductor_id):
        ref = db.reference('Users/Conductor/' + conductor_id)
        ref.delete()
        return redirect('index')

