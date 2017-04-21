#!/usr/bin/python

import sys
import os
from subprocess import Popen,PIPE

class Process(object):
    def __init__(self,name,program,args,workdir,kill):
        self.name=name
        self.program=program
        self.args=args
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

    def start(self):
        pid=self.pidfile()
        if pid:
            print '%s is running' %self.name
            sys.exit()
        self._init()
        cmd=self.program +' '+self.args    
        p=Popen(cmd,stdout=PIPE,shell=True)
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
    args='-u memcached -p 11211 -m 64 -c 1024'
    dir='/var/tmp/memcached/'
    killall='/usr/bin/killall'
    pm=Process(name = name,
               program = program,
               args = args,
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






