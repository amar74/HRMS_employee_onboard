from odoo import models, fields, api
from datetime import date
from odoo.http import request
import re
from odoo.exceptions import ValidationError
class employee_form(models.Model):
        _name="onboard.employee"
	_inherit = ['mail.mail', 'mail.thread']
	name = fields.Char('Name')
	position = fields.Many2one('hr.job', string='Position')
	employee_id = fields.Many2one('hr.employee')
	department = fields.Many2one('hr.department', string='Department')
	parent = fields.Many2one('hr.employee', string='Manager')
	doj = fields.Date('Date of Joining')
	salary = fields.Integer('Salary')
	empmail_id = fields.Char('Personal Email ID')
	phone = fields.Char('Mobile No.')
	Non_disclosure_agreement = fields.Binary('Non Disclosure Agreement')
	NDA = fields.Char('Non Disclosure Agreement')
	Employee_agreement = fields.Binary('Employee Agreement')
	Emp_A = fields.Char('Employee Agreement')
	anti_Sexual = fields.Binary('Anti Sexual')
	Anti_S = fields.Char('Anti Sexual')
	Ethics_policy = fields.Binary('Ethics Policy')
	ET_P = fields.Char('Ethics Policy')
	ESOPs = fields.Binary('ESOPS')
	ESOP = fields.Char('ESOPs')
	PF_form = fields.Binary('PF Form')
	Gratuity_form = fields.Binary('Gratuity Form')
	mac = fields.Boolean('Macbook')
        Laptop = fields.Boolean('Laptop')
        Desktop = fields.Boolean('Desktop')
        Thinkpad = fields.Boolean('Thinkpad')
        sim = fields.Boolean('Sim Card')
        bussiness = fields.Boolean('Bussiness Card')
        parking = fields.Boolean('Parking')
	image = fields.Binary('Image', required=True)
	image_filename = fields.Char("Image Filename")
	GF = fields.Char('GF')
	PF_f = fields.Char('PF_F')
	user_id = fields.Many2one('res.users', string='User')
	state = fields.Selection([
            ('employee_info', 'Employee Information'),
            ('documents', 'Documents'),
            ('assets', 'Assets'),
            ('admin', 'Admin'),
            ],default='employee_info')

	
        def submit(self, values):
		#import pdb; pdb.set_trace() 
		emp_id = self.env['hr.employee'].create(
			               {
					'name': self.name, 
					'job_id': self.position.id,				
					#.id is used because of job_id is Many2one field and realted with hr.job so that .id is used.
					'department_id': self.department.id,
					'parent_id': self.parent.id,
					'work_email': self.empmail_id,
					'work_phone': self.phone,
					'Emsalary': self.salary,
					'user_id': self.user_id.id,
					'DOJ': self.doj	
					})
		user_id1 = self.env['res.users'].create(
				     {
					'name': self.name,
					'login': self.empmail_id,
					'phone': self.phone
				      })
                self.write({
				 'employee_id':emp_id.id,
				 'user_id':user_id1.id, 	
		             })


	@api.onchange('phone')
	def valid_phone(self):
    		if self.phone:
			if not(re.match(r'(^[+0-9]{1,3})*([0-9]{10,11}$)', self.phone)):
				raise ValidationError("Please Enter Valid Phone no.")

	@api.onchange('email')
	def validate_mail(self):
		if self.email:
			if not(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)):
				raise ValidationError('Enter valid E-mail ID')

	@api.one
	def next(self):
		self.write({
			    'state': 'documents',
		  	 })

		
 	@api.one
	def employee_info(self):
		self.write({
			    'state': 'employee_info', })
#This function is triggered when the user clicks on the button 'Assets'
	@api.one
	def next1(self):
    		self.write({
		'state': 'assets'
    		})
 	
	@api.one
	def sav(self):
		self.write({})
	@api.one
	def documents(self):
		self.write({ 'state': 'documents'})
#This function is triggered when the user clicks on the button 'Admin'
	@api.one
	def next2(self):
    		self.write({
		'state': 'admin'
    		})
 	
	@api.one
	def assets(self):
		self.write({ 'state': 'assets' })


	@api.one
	def save(self):
		self.write(
			 {}) 


	@api.one
	def admin(self):
		self.write({ 'state': 'admin' })

#Email Send

	@api.multi
	def mail(self):
		#import pdb; pdb.set_trace()
		mail = self.env.ref('On_Boarding.Onboarding_employee_details')
		self.env['mail.template'].browse(mail.id).send_mail(self.id)


	@api.multi
	def maild(self):
		mail1 = self.env.ref('On_Boarding.Onboarding_empdoc_details')
		self.env['mail.template'].browse(mail1.id).send_mail(self.id)

#Controllers
'''
class contrl(http.Controller):
	@http.route('/employee', type='http', auth='user')
	def render_employee(self):
		return http.request.render('On_Boarding.Employee_form_view', { })

	@http.route('/employee/view', type='http',  auth='user')
		employees = http.request.env['hr.employee'].sudo().search([])
		return http.request.render('On_Boarding.Employee_form_view', {'employees':Employee})	
'''
