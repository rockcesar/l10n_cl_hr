from odoo import api, fields, models, tools, _
from datetime import datetime
import logging
import requests


_logger = logging.getLogger(__name__)
MONTH_LIST= [('1', 'Enero'), 
        ('2', 'Febrero'), ('3', 'Marzo'), 
        ('4', 'Abril'), ('5', 'Mayo'), 
        ('6', 'Junio'), ('7', 'Julio'), 
        ('8', 'Agosto'), ('9', 'Septiembre'), 
        ('10', 'Octubre'), ('11', 'Noviembre'),
        ('12', 'Diciembre')]


class hr_indicadores_previsionales(models.Model):

    _name = 'hr.indicadores'
    _description = 'Indicadores Previsionales'

    name = fields.Char('Nombre')
    asignacion_familiar_primer = fields.Float(
        'Asignación Familiar Tramo 1', 
        help="Asig Familiar Primer Tramo")
    asignacion_familiar_segundo = fields.Float(
        'Asignación Familiar Tramo 2', 
        help="Asig Familiar Segundo Tramo")
    asignacion_familiar_tercer = fields.Float(
        'Asignación Familiar Tramo 3', 
        help="Asig Familiar Tercer Tramo")
    asignacion_familiar_monto_a = fields.Float(
        'Monto Tramo Uno', help="Monto A")
    asignacion_familiar_monto_b = fields.Float(
        'Monto Tramo Dos',  help="Monto B")
    asignacion_familiar_monto_c = fields.Float(
        'Monto Tramo Tres',  help="Monto C")
    contrato_plazo_fijo_empleador = fields.Float(
        'Contrato Plazo Fijo Empleador', 
        help="Contrato Plazo Fijo Empleador")
    contrato_plazo_fijo_trabajador = fields.Float(
        'Contrato Plazo Fijo Trabajador', 
        help="Contrato Plazo Fijo Trabajador")    
    contrato_plazo_indefinido_empleador = fields.Float(
        'Contrato Plazo Indefinido Empleador', 
        help="Contrato Plazo Fijo")
    contrato_plazo_indefinido_empleador_otro = fields.Float(
        'Contrato Plazo Indefinido 11 anos o mas', 
        help="Contrato Plazo Indefinido 11 anos Empleador")
    contrato_plazo_indefinido_trabajador_otro = fields.Float(
        'Contrato Plazo Indefinido 11 anos o mas', 
        help="Contrato Plazo Indefinido 11 anos Trabajador")
    contrato_plazo_indefinido_trabajador = fields.Float(
        'Contrato Plazo Indefinido Trabajador', 
        help="Contrato Plazo Indefinido Trabajador")
    caja_compensacion = fields.Float(
        'Caja Compensación', 
        help="Caja de Compensacion")
    deposito_convenido = fields.Float(
        'Deposito Convenido', help="Deposito Convenido")
    fonasa = fields.Float('Fonasa',  help="Fonasa")
    mutual_seguridad = fields.Float(
        'Mutualidad',  help="Mutual de Seguridad")
    isl = fields.Float(
        'ISL',  help="Instituto de Seguridad Laboral")
    pensiones_ips = fields.Float(
        'Pensiones IPS',  help="Pensiones IPS")
    sueldo_minimo = fields.Float(
        'Trab. Dependientes e Independientes',  help="Sueldo Minimo")
    sueldo_minimo_otro = fields.Float(
        'Menores de 18 y Mayores de 65:', 
        help="Sueldo Mínimo para Menores de 18 y Mayores a 65")
    tasa_afp_cuprum = fields.Float(
        'Cuprum',  help="Tasa AFP Cuprum")
    tasa_afp_capital = fields.Float(
        'Capital',  help="Tasa AFP Capital")
    tasa_afp_provida = fields.Float(
        'ProVida',  help="Tasa AFP Provida")
    tasa_afp_modelo = fields.Float(
        'Modelo',  help="Tasa AFP Modelo")
    tasa_afp_planvital = fields.Float(
        'PlanVital',  help="Tasa AFP PlanVital")
    tasa_afp_habitat = fields.Float(
        'Habitat',  help="Tasa AFP Habitat")
    tasa_sis_cuprum = fields.Float(
        'SIS', help="Tasa SIS Cuprum")
    tasa_sis_capital = fields.Float(
        'SIS', help="Tasa SIS Capital")
    tasa_sis_provida = fields.Float(
        'SIS',  help="Tasa SIS Provida")
    tasa_sis_planvital = fields.Float(
        'SIS',  help="Tasa SIS PlanVital")
    tasa_sis_habitat = fields.Float(
        'SIS',  help="Tasa SIS Habitat")
    tasa_sis_modelo = fields.Float(
        'SIS',  help="Tasa SIS Modelo")
    tasa_independiente_cuprum = fields.Float(
        'SIS',  help="Tasa Independientes Cuprum")
    tasa_independiente_capital = fields.Float(
        'SIS',  help="Tasa Independientes Capital")
    tasa_independiente_provida = fields.Float(
        'SIS',  help="Tasa Independientes Provida")
    tasa_independiente_planvital = fields.Float(
        'SIS',  help="Tasa Independientes PlanVital")
    tasa_independiente_habitat = fields.Float(
        'SIS',  help="Tasa Independientes Habitat")
    tasa_independiente_modelo = fields.Float(
        'SIS',  help="Tasa Independientes Modelo")
    tope_anual_apv = fields.Float(
        'Tope Anual APV',  help="Tope Anual APV")
    tope_mensual_apv = fields.Float(
        'Tope Mensual APV',  help="Tope Mensual APV")
    tope_imponible_afp = fields.Float(
        'Tope imponible AFP',  help="Tope Imponible AFP")
    tope_imponible_ips = fields.Float(
        'Tope Imponible IPS',  help="Tope Imponible IPS")
    tope_imponible_salud = fields.Float(
        'Tope Imponible Salud')
    tope_imponible_seguro_cesantia = fields.Float(
        'Tope Imponible Seguro Cesantía', 
        help="Tope Imponible Seguro de Cesantía")
    uf = fields.Float(
        'UF',  required=True, help="UF fin de Mes")
    utm = fields.Float(
        'UTM',  required=True, help="UTM Fin de Mes")
    uta = fields.Float('UTA',  help="UTA Fin de Mes")
    uf_otros = fields.Float(
        'UF Otros',  help="UF Seguro Complementario")
    mutualidad_id = fields.Many2one('hr.mutual', 'MUTUAL')
    ccaf_id = fields.Many2one('hr.ccaf', 'CCAF')
    month = fields.Selection(MONTH_LIST, string='Mes', required=True)
    year = fields.Integer('Año', required=True, default=datetime.now().strftime('%Y'))
    gratificacion_legal = fields.Boolean('Gratificación L. Manual')
    mutual_seguridad_bool = fields.Boolean('Mutual Seguridad', default=True)
    ipc = fields.Float(
        'IPC',  required=True, help="Indice de Precios al Consumidor (IPC)")


    @api.multi
    @api.onchange('month')
    def get_name(self):
        self.name = str(self.month).replace('10', 'Octubre').replace('11', 'Noviembre').replace('12', 'Diciembre').replace('1', 'Enero').replace('2', 'Febrero').replace('3', 'Marzo').replace('4', 'Abril').replace('5', 'Mayo').replace('6', 'Junio').replace('7', 'Julio').replace('8', 'Agosto').replace('9', 'Septiembre') + " " + str(self.year)

    def find_between_r(self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_month(self, s):
        if s == '1':
            return 'Enero'
        if s == '2':
            return 'Febrero'
        if s == '3':
            return 'Marzo'
        if s == '4':
            return 'Abril'
        if s == '5':
            return 'Mayo'
        if s == '6':
            return 'Junio'
        if s == '7':
            return 'Julio'
        if s == '8':
            return 'Agosto'
        if s == '9':
            return 'Septiembre'
        if s == '10':
            return 'Octubre'
        if s == '11':
            return 'Noviembre'
        if s == '12':
            return 'Diciembre'



    def clean_string(self, s):
        s = s.replace("<strong>", "")
        s = s.replace("</strong>", "")
        s = s.replace("</td>", "")
        s = s.replace("<td>", "")
        s = s.replace("$ ", "")        
        s = s.replace("</div>", "")
        s = s.replace("<div>", "")
        s = s.replace(".", "")
        s = s.replace(" ", "")
        s = s.replace("%", "")
        s = s.replace("RI", "")
        s = s.replace("</tr>", "")
        s = s.replace("<tr>", "")
        s = s.replace('<tdwidth="20">', '')
        s = s.replace("<tbody>", "")
        s = s.replace("</tbody>", "")
        s = s.replace("</table>", "")
        s = s.replace("<table>", "")
        s = s.replace('<tdwidth="80">', '')
        s = s.replace('colspan="2">', '')
        s = s.replace("width", "")
        s = s.replace('"', '')

        
        return s


    @api.one
    def update_document(self):
        url = "https://www.previred.com/web/previred/indicadores-previsionales"
        response = requests.get(url,params="nombre")
        if response and response.status_code!=200:
            _logger.warning("error %s" %(response))
            vals= {'detail':"Not found."}
        else:
            vals = response.text
            vals = self.clean_string(vals)
            fecha = self.find_month(self.month) + str(self.year)
            fecha = "de" + fecha.strip()
            try:
                _logger.warning(vals)
                self.uf = self.find_between_r( vals, fecha, '<' ).replace(",", ".")[:8]
                self.utm = self.find_between_r( vals, '2018<tdalign=center>', '<' )[:5]
                self.uta = self.find_between_r( vals, '2018<tdalign=center>', '<divclass=entry-links>' )[21:27]
                #self.tope_imponible_afp = self.find_between_r( vals, 'ParaafiliadosaunaAFP(', 'UF):' )[:5]

            except ValueError:
                return ""


            


