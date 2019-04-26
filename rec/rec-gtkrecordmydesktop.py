#!/usr/bin/python

import subprocess, shlex, os
from gi.repository import Gtk	

class Handler:
	
	pids = []

	def on_window1_delete_event(self, *args):
		Gtk.main_quit(*args)

	def screenCheck_toggled(self, *args):
		if builder.get_object("screenCheck").get_active():
			builder.get_object("soundCheck").props.sensitive = True
		else:
		   	builder.get_object("soundCheck").props.sensitive = False
			builder.get_object("soundCheck").props.active = False
		
	def on_start_toggled(self, *args):

		if builder.get_object("startButton").get_active():
			builder.get_object("startButton").set_label("Stop")
			test = False
			filename = subprocess.check_output(['date', '+%F_%I%M%S'])
			folder = builder.get_object("outputButton").get_filename()
			
			if builder.get_object("screenCheck").get_active():
				rmd_cmd = 'recordmydesktop --delay 5 --no-frame --no-sound --v_quality 16 --workdir ' + folder + ' -o ' + folder + '/rec-' + filename.rstrip() + '.ogv'
				test  = True
			if builder.get_object("soundCheck").get_active():
				rmd_cmd = 'recordmydesktop --delay 5 --no-frame --v_quality 16 --s_quality 5 --workdir ' + folder + ' -o ' + folder + '/rec-' + filename.rstrip() + '.ogv'
				test = True
			if builder.get_object("networkCheck").get_active():
				interface = builder.get_object("networkBox").get_active() + 1
				tcpd_cmd = 'tcpdump -nnvvXSs 1514 -Z root -i ' + str(interface) + ' -C 2000 -w ' + folder + '/rec-' + filename.rstrip() + '.pcap'
				run_tcpd = subprocess.Popen(shlex.split(tcpd_cmd), shell=False, stdin=None, stdout=None, stderr=None)
				Handler.pids.append(run_tcpd.pid)
			if test:
				run_rmd = subprocess.Popen(shlex.split(rmd_cmd), shell=False, stdin=None, stdout=None, stderr=None)
				Handler.pids.append(run_rmd.pid)
		
		else:
			for p in Handler.pids:
				subprocess.Popen(shlex.split("kill " + str(p)))
			Handler.pids[:] = []
			builder.get_object("startButton").set_label("Start")

builder = Gtk.Builder()
builder.add_from_file("rec.glade")
builder.connect_signals(Handler())

interfaces = subprocess.check_output(['tcpdump','-D'])

box = builder.get_object("networkBox")
for iface in interfaces.splitlines():	
	box.append_text(iface.split()[0])
box.set_active(0)


window = builder.get_object("window1")
window.show_all()

Gtk.main()

