from django.utils import formats
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
#
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
#
from django.contrib.auth.models import User
from apps.tickets.models import *
from apps.historico.models import *
from django.db.models import Q, Count
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import datetime
#necesaria para que matplotlib funcione en entorno grafico
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.core.files.storage import default_storage
#
from weasyprint import HTML
#
from apps.usuarios.models import Departamentos,Empleado
# Create your views here.

@login_required
def ticketViews (request):
    if request.method == 'POST' and request.is_ajax():
        
        try:
            data = []
            with transaction.atomic():
                #========================   select   =========================
                action = request.POST['action']
                id_user = request.user.id
                query = Q(status="OPEN")
                query.add(Q(status="IN_PROGRESS"),Q.OR)
                query.add(Q(user_id=id_user),Q.AND)

                if action =='buscardatos':
                    for i in Ticket.objects.filter(query):
                        data.append(i.toJSON())
                        print(i.created_at)
                        #========================   Crear   =========================
                elif action =='crear':
                    usuario_registro = User.objects.get(pk=id_user)
                    dato_Ticket = Ticket()
                    if int(request.POST['categoria'])>0:
                        dato_Ticket.categoria = categoria_ticket.objects.get(pk=request.POST['categoria'])
                    dato_Ticket.title = request.POST['title']
                    dato_Ticket.description = request.POST['description']

                    dato_Ticket.user_id = usuario_registro
                    dato_Ticket.updated_by = usuario_registro
                    dato_Ticket.save()
                    if request.FILES:
                        imagen = request.FILES.get("imagen")
                        imagen.name = str(dato_Ticket.pk)+"_"+imagen.name
                        dato_Ticket.img_ticket = imagen
                        dato_Ticket.save()
                        #Actualizamos la ruta de la imagen con la concatenacion del id recien creado

                    historial_accion = 'Se creo el ticket num. (' + str(dato_Ticket.pk) + ') con asunto (' + str(dato_Ticket.title) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=True,created_by=User.objects.get(pk=id_user))

                    #Envio de correo de confirmacion de que se registro el ticket
                    asunto = f"Ticket # {dato_Ticket.pk} <{dato_Ticket.title}> generado exitosamente"

                    mensaje_html = render_to_string('tickets/confirmacion_correo.html', {'dato_Ticket': dato_Ticket})
                    mensaje_txt = strip_tags(mensaje_html)
                    
                    email = EmailMultiAlternatives(asunto, mensaje_txt, 'it@cuasa.hn', [usuario_registro.email])
                    email.attach_alternative(mensaje_html, "text/html")
                    email.send()

                    data = {'tipo_accion': 'crear', 'correcto': True}
        except Exception as e:
            data['error'] = str(e)
            print("Error--->",e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        categoria = categoria_ticket.objects.all()
        return render(request, 'tickets/ticket_home.html',{'categorias': categoria})


@login_required
def AdminTicketViews (request,id):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data = []
        try:
            with transaction.atomic():
                estado = 'NADA'
                if int(id) == 1:
                    estado = 'OPEN'
                elif int(id) == 2:
                    estado = 'IN_PROGRESS'
                elif int(id) == 3:
                    estado = 'DONE'
                #========================   select Tickets Abiertos  =========================
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()
                if action =='buscardatos':
                    if estado == 'OPEN' or estado == 'IN_PROGRESS':
                        for i in Ticket.objects.filter(status=estado):
                            data.append(i.toJSON())
                    elif estado == 'DONE':
                        fecha_ini = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_ini'],'%Y-%m-%d')) 
                        fecha_final_1 = timezone.make_aware(datetime.datetime.strptime(request.POST['fecha_final'], '%Y-%m-%d'))
                        fecha_final = fecha_final_1.replace(hour=23, minute=59, second=59, microsecond=999)
                        for i in Ticket.objects.filter(status=estado, created_at__range=[fecha_ini, fecha_final]):
                            data.append(i.toJSON())
                        #========================   Crear   =========================
                elif action =='actualizarOpen':
                    dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                    
                    dato_Ticket.status = "IN_PROGRESS"
                    dato_Ticket.updated_by = User.objects.get(pk=id_user)
                    dato_Ticket.updated_at = formats.date_format(date_up)

                    if int(request.POST['assignee_id'])>0:
                        dato_Ticket.assignee_id = User.objects.get(pk=request.POST['assignee_id'])
                        
                        usuario_registro = dato_Ticket.user_id.email
                        asunto = f"Ticket # {dato_Ticket.pk} <{dato_Ticket.title}> asignado exitosamente"

                        mensaje_html = render_to_string('tickets/asignacion_correo.html', {'dato_Ticket': dato_Ticket})
                        mensaje_txt = strip_tags(mensaje_html)
                        
                        email = EmailMultiAlternatives(asunto, mensaje_txt, 'it@cuasa.hn', [usuario_registro])
                        email.attach_alternative(mensaje_html, "text/html")

                        dato_Ticket.save()
                        
                        historial_accion = 'Se asigno el ticket num. (' + str(dato_Ticket.pk) + ') a el usuario (' + str(dato_Ticket.assignee_id.username) + ')'
                        historial = historico.objects.create(accion=historial_accion,tipo_accion=False,created_by=User.objects.get(pk=id_user))

                        email.send()
                        data = {'tipo_accion': 'actualizarOpen', 'correcto': True}

                elif action =='actualizarProgress':
                    dato_Ticket = Ticket.objects.get(pk=request.POST['id'])
                    dato_Ticket.status = "DONE"
                    dato_Ticket.updated_by = User.objects.get(pk=id_user)
                    dato_Ticket.updated_at = formats.date_format(date_up)

                    usuario_registro = dato_Ticket.user_id.email
                    #Envio de correo de confirmacion de que se registro el ticket
                    asunto = f"Ticket # {dato_Ticket.pk} <{dato_Ticket.title}> cerrado"

                    mensaje_html = render_to_string('tickets/cerrado_correo.html', {'dato_Ticket': dato_Ticket})
                    mensaje_txt = strip_tags(mensaje_html)
                    
                    email = EmailMultiAlternatives(asunto, mensaje_txt, 'it@cuasa.hn', [usuario_registro])
                    email.attach_alternative(mensaje_html, "text/html")

                    dato_Ticket.save()
                    
                    historial_accion = 'Se cerro el ticket num. (' + str(dato_Ticket.pk) + ') a el usuario (' + str(dato_Ticket.assignee_id.username) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=False,created_by=User.objects.get(pk=id_user))
                    email.send()

                    data = {'tipo_accion': 'actualizarProgress', 'correcto': True}
        except Exception as e: 
            data['error'] = str(e)
            data = {'tipo_accion': 'error','correcto': False, 'error': str(e)}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data,safe=False)
    elif request.method =="GET":
        users = User.objects.filter(is_staff=True, is_superuser=False)
        return render(request, 'tickets/ticket_admin.html',{'users':users})

@login_required
def categoria_ticket_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.view_categoria_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method == 'POST' and request.is_ajax():
        data =[]
        try:
            with transaction.atomic():
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()

                if action == 'buscardatos':
                    for i in categoria_ticket.objects.all():
                        data.append(i.toJSON())

                elif action == 'crear':
                    ca = categoria_ticket()
                    ca.tittle = request.POST['tittle']
                    ca.description = request.POST['description']
                    ca.created_by = User.objects.get(pk=id_user)
                    ca.updated_by = User.objects.get(pk=id_user)
                    ca.save()

                    historial_accion = 'Se creo la categoria de ticket num. (' + str(ca.pk) + ') con el nombre (' + str(ca.tittle) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=True,created_by=User.objects.get(pk=id_user))
                    
                    data = {'tipo_accion':'crear', 'correcto':True}
                elif action == 'editar':
                    ca = categoria_ticket.objects.get(pk=request.POST['id'])
                    ca.tittle = request.POST['tittle']
                    ca.description = request.POST['description']
                    ca.updated_by = User.objects.get(pk=id_user)
                    ca.updated_at = formats.date_format(date_up)
                    ca.save()

                    historial_accion = 'Se modifico la categoria de ticket num. (' + str(ca.pk) + ') con el nombre (' + str(ca.tittle) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=False,created_by=User.objects.get(pk=id_user))

                    data = {'tipo_accion':'editar', 'correcto':True}
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
            data = {'tipo_accion':'error', 'correcto':True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    elif request.method =="GET":
        return render(request, 'tickets/categorias.html')


@login_required
def commentTicket_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('commentTicket.view_comentticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":
        id_t = request.GET['id_ticket']
        return render(request, 'tickets/comentarios.html',{'ticket':id_t})
    elif request.method == 'POST' and request.is_ajax():
        data =[]
        try:
            with transaction.atomic():
                action = request.POST['action']
                id_user = request.user.id
                date_up = timezone.now()
                id_t = int(request.POST['ticket'])
                if action == 'buscardatos':
                    for i in commentTicket.objects.filter(id_ticket = id_t):
                        data.append(i.toJSON())
                elif action == 'crear':
                    # print('lol ',id_t)
                    coment = commentTicket.objects.create(
                        id_ticket=Ticket.objects.get(pk=id_t),
                        title = request.POST['title'],
                        comment = request.POST['comments'],
                        created_by = User.objects.get(pk=id_user),
                        updated_by = User.objects.get(pk=id_user),
                    )

                    historial_accion = 'Se creo el comentario num. ('+str(coment.pk) +') a el ticket num. (' + str(coment.id_ticket.pk) + ') con el asunto (' + str(coment.title) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=True,created_by=User.objects.get(pk=id_user))

                    data = {'tipo_accion':'crear', 'correcto':True}
                elif action == 'editar':
                    commentTicket.objects.filter(pk=request.POST['id_comment']).update(
                        title = request.POST['title'],
                        comment = request.POST['comments'],
                        updated_by = User.objects.get(pk=id_user),
                        updated_at = date_up
                    )
                    coment = commentTicket.objects.get(pk=request.POST['id_comment'])
                    historial_accion = 'Se modifico el comentario num. ('+str(coment.pk) +') a el ticket num. (' + str(coment.id_ticket.pk) + ') con el asunto (' + str(coment.title) + ')'
                    historial = historico.objects.create(accion=historial_accion,tipo_accion=False,created_by=User.objects.get(pk=id_user))

                    data = {'tipo_accion':'editar', 'correcto':True}
                else:
                    data['error'] = 'Ha ocurrido un error.'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
            data = {'tipo_accion':'error', 'correcto':True}
            transaction.rollback()
        else:
            transaction.commit()
        return JsonResponse(data, safe=False)
    

@login_required
def ticket_categorias_view(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":
        categorias = categoria_ticket.objects.annotate(num_tickets=Count('ticket_categoria_ticket'))
        labels = [c.tittle for c in categorias]
        data = [c.num_tickets for c in categorias]
        
        return render(request, 'tickets/reportes_ticket.html',{'labels':labels, 'data':data})


@login_required
def ticket_categorias_pdf(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":

        fecha_inicial = timezone.make_aware(datetime.datetime.strptime(request.GET['f_in'],'%Y-%m-%d'))
        fecha_final_1 = timezone.make_aware(datetime.datetime.strptime(request.GET['f_fin'],'%Y-%m-%d'))
        fecha_final = fecha_final_1.replace(hour=23, minute=59, second=59, microsecond=999)
        # Grafico
        categorias = categoria_ticket.objects.filter(ticket_categoria_ticket__created_at__range=(fecha_inicial, fecha_final)).annotate(num_tickets=Count('ticket_categoria_ticket'))
        # redireccion si no se encuentran datos
        if not categorias:
            return render(request, 'reportes/no_hay_datos.html')
        labels = [c.tittle for c in categorias]
        data = [c.num_tickets for c in categorias]

        df = pd.DataFrame({'num_tickets': data}, index=labels)
        plot = df.plot.pie(y='num_tickets', figsize=(9, 9),autopct='%1.1f%%',labels=None)
        plot.set_ylabel('')
        fig = plot.get_figure()
        fig.savefig(os.path.join(settings.MEDIA_ROOT, 'grafico_pie.png'))
        plt.close()
        
        # Tabla
        tabla = [(c.tittle, c.num_tickets) for c in categorias]
        fecha_inicial_str = fecha_inicial.strftime('%b. %d, %Y')
        fecha_final_str = fecha_final.strftime('%b. %d, %Y')

        filename = 'grafico_pie.png'
        html_string = render_to_string('reportes/reporte_categoria_pdf.html', {'filename': filename, 'tabla': tabla,'f_inicial': fecha_inicial_str, 'f_final': fecha_final_str})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        response = HttpResponse(html.write_pdf(), content_type='application/pdf')
        return response
    
@login_required
def reportes_views(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":
        deptos = Departamentos.objects.all()
        return render(request, 'reportes/reportes.html', {'deptos': deptos})
    

@login_required
def ticket_departamento_pdf(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":

        try:
            with transaction.atomic():
                fecha_inicial = timezone.make_aware(datetime.datetime.strptime(request.GET['f_in'],'%Y-%m-%d'))
                fecha_final_1 = timezone.make_aware(datetime.datetime.strptime(request.GET['f_fin'],'%Y-%m-%d'))
                fecha_final = fecha_final_1.replace(hour=23, minute=59, second=59, microsecond=999)
                tickets_por_depto = Ticket.objects.filter(user_id__empleado_usuario__depto__isnull=False, created_at__range=[fecha_inicial, fecha_final]).values('user_id__empleado_usuario__depto','user_id__empleado_usuario__depto__nombre_depto').annotate(total_tickets=Count('id'))
                # redireccion si no se encuentran datos
                if not tickets_por_depto:
                    return render(request, 'reportes/no_hay_datos.html')
                # Convertir los resultados de la consulta en un dataframe de pandas
                df = pd.DataFrame(list(tickets_por_depto))
                
                # Ordenar el dataframe por número de tickets de forma descendente
                df = df.sort_values(by='total_tickets', ascending=False)

                # Crear el gráfico de barras
                plt.figure(figsize=(8,8))
                sns.set(style="whitegrid")
                ax = sns.barplot(x='user_id__empleado_usuario__depto__nombre_depto', y='total_tickets', data=df)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                ax.set_xlabel('Departamentos') 
                ax.set_ylabel('Número de Tickets')
                plt.tight_layout()
                plt.savefig(os.path.join(settings.MEDIA_ROOT, 'tickets_por_depto.png'))
                # plt.close()
                # Guardar la imagen en la ruta de media
                # image_path = default_storage.path('tickets_por_depto.png')
                # plt.savefig(image_path)
                plt.close()

                
                tabla_dict = []
                for ticket in tickets_por_depto:
                    ticket_asg={}
                    ticket_asg['depto_id'] = ticket['user_id__empleado_usuario__depto']
                    ticket_asg['depto_nombre'] = ticket['user_id__empleado_usuario__depto__nombre_depto']
                    ticket_asg['total_tickets'] = ticket['total_tickets']
                    tabla_dict.append(ticket_asg)
                
                fecha_inicial_str = fecha_inicial.strftime('%b. %d, %Y')
                fecha_final_str = fecha_final.strftime('%b. %d, %Y')
                tabla_dict_short = sorted(tabla_dict, key=lambda k: k['total_tickets'], reverse=True)

                filename = 'tickets_por_depto.png'
                html_string = render_to_string('reportes/reporte_incidencias_depto_pdf.html', {'filename': filename, 'tabla': tabla_dict_short,'f_inicial': fecha_inicial_str, 'f_final': fecha_final_str})
                html = HTML(string=html_string,base_url=request.build_absolute_uri())
                
                response = HttpResponse(html.write_pdf(), content_type='application/pdf')
                # return response
        except Exception as e:
            print('Error -->', e)
            transaction.rollback()
        else:
            transaction.commit()
            return response
            # return render(request, 'reportes/reporte_incidencias_depto_pdf.html', {'filename': filename, 'tabla': tabla_dict_short,'f_inicial': fecha_inicial_str, 'f_final': fecha_final_str})
        
@login_required
def categoria_departamento_pdf(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.has_perm('tickets.delete_ticket')):
        return redirect('usuarios_app:error_view')
    if request.method =="GET":

        try:
            with transaction.atomic():
                fecha_inicial = timezone.make_aware(datetime.datetime.strptime(request.GET['f_in'],'%Y-%m-%d'))
                fecha_final_1 = timezone.make_aware(datetime.datetime.strptime(request.GET['f_fin'],'%Y-%m-%d'))
                fecha_final = fecha_final_1.replace(hour=23, minute=59, second=59, microsecond=999)
                depto = Departamentos.objects.get(id=request.GET['dpt'])

                
                tickets_por_depto_y_categoria = Ticket.objects.filter(user_id__empleado_usuario__depto=Departamentos.objects.get(id=request.GET['dpt']), created_at__range=[fecha_inicial, fecha_final]).values('categoria__tittle').annotate(total_tickets=Count('id'))
                if not tickets_por_depto_y_categoria:
                    return render(request, 'reportes/no_hay_datos.html')
                # Convertir los resultados de la consulta en un dataframe de pandas
                df = pd.DataFrame(list(tickets_por_depto_y_categoria))
                
                # Ordenar el dataframe por número de tickets de forma descendente
                df = df.sort_values(by='total_tickets', ascending=False)
                
                # Crear el gráfico de barras
                plt.figure(figsize=(8,8))
                sns.set(style="whitegrid")
                ax = sns.barplot(x='categoria__tittle', y='total_tickets', data=df)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                ax.set_xlabel('Categorías') 
                ax.set_ylabel('Número de Tickets')
                plt.tight_layout()
                plt.savefig(os.path.join(settings.MEDIA_ROOT, 'tickets_por_categoria.png'))
                plt.close()
                
                # Crear la tabla de resultados
                tabla_dict = []
                for ticket in tickets_por_depto_y_categoria:
                    ticket_asg={}
                    ticket_asg['categoria'] = ticket['categoria__tittle']
                    ticket_asg['total_tickets'] = ticket['total_tickets']
                    tabla_dict.append(ticket_asg)
                # Obtener la ruta de la imagen generada
                tabla_dict_short = sorted(tabla_dict, key=lambda k: k['total_tickets'], reverse=True)

                fecha_inicial_str = fecha_inicial.strftime('%b. %d, %Y')
                fecha_final_str = fecha_final.strftime('%b. %d, %Y')

                filename = 'tickets_por_categoria.png'
                
                html_string = render_to_string('reportes/reporte_categorias_departamentos_pdf.html', {'filename': filename, 'tabla': tabla_dict_short, 'f_inicial': fecha_inicial_str, 'f_final': fecha_final_str, 'depto': depto})
                html = HTML(string=html_string,base_url=request.build_absolute_uri())
                response = HttpResponse(html.write_pdf(), content_type='application/pdf')
                # return response
        except Exception as e:
            print('Error -->', e)
            transaction.rollback()
        else:
            transaction.commit()
            print('holaa asdads')
            return response