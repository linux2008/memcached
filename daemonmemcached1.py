#!/usr/bin/python

import sys
import os
from subprocess import Popen,PIPE

class Process(object):
    '''memcached rc script'''
    args={'USER':'memcached',
          'PORT':11211,
          'MAXCONN':1024,
          'CACHESIZE':64,
          'OPTIONS':' '}

    def __init__(self,name,program,workdir,kill):
        self.name=name
        self.program=program
        self.workdir=workdir
        self.kill=kill

    def _init(self):
        '''/var/tmp/memcached'''
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)
            os.chdir(self.workdir)

    def _pidfile(self):
        '''/var/tmp/memcached/memcached.pid'''
        return os.path.join(self.workdir,"%s.pid" % self.name)
 
    def _write(self):
        if self.pid:
            with open(self._pidfile(),'w') as fd:
                fd.write(str(self.pid))       
  
    def _read(self,f):
        with open(f) as fd:
            lines=fd.readlines()
            return dict([i.strip().replace('"','').split('=') for i in lines])

    def _parseconf(self):
        conf=self._read('/etc/sysconfig/memcached')
        if 'USER' in conf:
            self.args['USER']=conf['USER']
        if 'PORT' in conf:
            self.args['PORT']=conf['PORT']
        if 'MAXCONN' in conf:
            self.args['MAXCONN']=conf['MAXCONN']
        if 'CACHESIZE' in conf:
            self.args['CACHESIZE']=conf['CACHESIZE'] 
        options=['-u',self.args['USER'],
                 '-p',self.args['PORT'],
                 '-m',self.args['CACHESIZE'],
                 '-c',self.args['MAXCONN']] 
        return options  

    def start(self):
        pid=self.pidfile()
        if pid:
            print '%s is running.....' %self.name
            sys.exit()
        self._init()
        cmd=[self.program] + self._parseconf()+['-d','-p',self._pidfile()]  
        print cmd
        p=Popen(cmd,stdout=PIPE)
        self.pid=p.pid
        self._write()
        print '%s start successful' %self.name
 
    def stop(self):
        cmd=self.kill +' '+self.name
        p=Popen(cmd,stdout=PIPE,shell=True)
        file=self._pidfile()
        if file:
            with open(file,'w') as fd:
                fd.write('')
            print '%s stop successful' %self.name
        else:
            print 'please order %s' %self.start()
    def pidfile(self):
        p=Popen(['pidof',self.name],stdout=PIPE)
        pids=p.stdout.read().strip()
        return pids

    def restart(self):
        self.stop()
        self.start()
 
    def status(self):
        pids=self.pidfile()
        if pids:
            print ' %s is already running' % self.name
        else:
            print ' %s is not running' % self.name

    def help(self):
        print "Usage:%s{start|stop|restart|status}" %__file__

def main():
    name='memcached'
    program='/usr/bin/memcached'
    dir='/var/tmp/memcached/'
    killall='/usr/bin/killall'
    pm=Process(name = name,
               program = program,
               workdir = dir,
               kill=killall)
    try:
        cmd=sys.argv[1]
    except IndexError,e:
        print 'option error'
        sys.exit(1)
#        pm.help()
    if cmd == 'start':
        pm.start()
    elif cmd== 'stop':
        pm.stop()
    elif cmd=='restart':
        pm.restart()
    elif cmd=='status':
        pm.status()
    else:
        pm.help()

if __name__=='__main__':
    main()






