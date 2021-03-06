# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt 

from __future__ import unicode_literals
"""
	Utilities for using modules
"""
import webnotes, os
from webnotes import conf

lower_case_files_for = ['DocType', 'Page', 'Report', 
	"Workflow", 'Module Def', 'Desktop Item', 'Workflow State', 'Workflow Action']

def scrub(txt):
	return txt.replace(' ','_').replace('-', '_').replace('/', '_').lower()

def scrub_dt_dn(dt, dn):
	"""Returns in lowercase and code friendly names of doctype and name for certain types"""
	ndt, ndn = dt, dn
	if dt in lower_case_files_for:
		ndt, ndn = scrub(dt), scrub(dn)

	return ndt, ndn
			
def get_module_path(module):
	"""Returns path of the given module"""
	m = scrub(module)
	
	app_path = webnotes.utils.get_base_path()
	
	if m in ('core', 'website'):
		return os.path.join(app_path, 'lib', m)
	else:
		return os.path.join(app_path, 'app', m)
		
def get_plugin_path(plugin):
	from webnotes.utils import get_site_path
	return get_site_path(webnotes.conf.get("plugins_path"), scrub(plugin))

def get_doc_path(module, doctype, name):
	dt, dn = scrub_dt_dn(doctype, name)
	return os.path.join(get_module_path(module), dt, dn)

def reload_doc(module, dt=None, dn=None, force=True):
	from webnotes.modules.import_file import import_files
	return import_files(module, dt, dn, force)

def export_doc(doctype, name, module=None, plugin=None):
	"""write out a doc"""
	from webnotes.modules.export_file import write_document_file
	import webnotes.model.doc

	if not module: module = webnotes.conn.get_value(doctype, name, 'module')
	write_document_file(webnotes.model.doc.get(doctype, name), module, plugin=plugin)

def get_doctype_module(doctype):
	return webnotes.conn.get_value('DocType', doctype, 'module')
