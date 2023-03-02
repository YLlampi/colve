from django import forms
from .models import Doctor, Pago


class PagoForms(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'num_cuotas']
        widgets = {
            'monto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'S/'
                }
            ),
            'num_cuotas': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': '1'
                }
            ),
        }


class PayForms(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['fecha_mes', ]

        widgets = {
            'fecha_mes': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'month',
                }
            ),
        }


class UpdateCMVPForms(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['num_CMVP', 'fecha_registro', 'fecha_emision', 'fecha_mes']

        widgets = {
            'num_CMVP': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'ingrese CMVP'
                }
            ),
            'fecha_registro': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_emision': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_mes': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }

    def clean_num_CMVP(self):
        num_CMVP = self.cleaned_data['num_CMVP']
        #if len(num_CMVP) != 8:
        #    raise forms.ValidationError('Ingrese 8 digitos')

        if num_CMVP and len(num_CMVP) != 4:
            raise forms.ValidationError('Ingrese 4 dígitos')

        if num_CMVP and not num_CMVP.isdigit():
            raise forms.ValidationError('Ingrese solo numeros')
        return num_CMVP


class DoctorForms(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['nombres', 'apellidos', 'dni']
        """
        exclude = [
            'num_CMVP',
            'fecha_registro',
            'fecha_emision',
            'fecha_caducidad',
            'es_activo',
            'fecha_pagado',
            'fecha_activo',
        ]
        """

        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'DNI',
                }
            ),

        }
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        #if len(num_CMVP) != 8:
        #    raise forms.ValidationError('Ingrese 8 digitos')
        if len(dni) != 8:
            raise forms.ValidationError('Ingrese 8 dígitos')
        if dni and not dni.isdigit():
            raise forms.ValidationError('Ingrese solo numeros')
        return dni


"""
widgets = {
            'departamento': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Arequipa',
                }
            ),
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': '02234527',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'apellidos',
                }
            ),
            'nacionalidad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'nacionalidad',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'nacimiento_distrito': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Distrito',
                }
            ),
            'nacimiento_provincia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Privincia',
                }
            ),
            'nacimiento_departamento': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Departamento',
                }
            ),
            'estado_civil': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'nombre_conyuge': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Nombre Cónyuge',
                }
            ),
            'num_hijos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }
            ),
            'direccion_actual': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Av. Ejercito',
                }
            ),
            'direccion_distrito': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Cayma',
                }
            ),
            'direccion_provincia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Arequipa',
                }
            ),
            'direccion_departamento': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Arequipa',
                }
            ),
            'telefono_fijo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': '',
                }
            ),
            'celular': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. 951541537',
                }
            ),
            'operador': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Movistar',
                }
            ),
            'email_uno': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. alguien@email.com',
                }
            ),
            'email_dos': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. alguien_2@email.com',
                }
            ),
            'universidad_procedencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Universidad Católica de Santa María',
                }
            ),
            'fecha_egreso_bachiller': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_obtencion_titulo': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'especialidad_postgrado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }
            ),
            'area_ejercicio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }
            ),
            'centro_laboral': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Municipio',
                }
            ),
            'direccion_trabajo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. Av Venezuela',
                }
            ),
            'telefono_trabajo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'Ej. 915234589',
                }
            ),
            'num_CMVP': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }
            ),
            'fecha_registro': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_emision': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_caducidad': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_pagado': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'fecha_activo': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

        }
        """