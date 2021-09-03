#!/usr/bin/python3
# -*- coding: utf-8 -*-
from server import startServer, stopServer

import sys, os, argparse

oldpath = os.getcwd()

parser = argparse.ArgumentParser(description='Micro Web Server')
parser.add_argument('-d','--dir', help='Select Directory (Default: .)',default=oldpath,dest='path')
parser.add_argument('--host',     help='Host (Default: localhost)',default='localhost',dest='host')
parser.add_argument('-p','--port',help='Port Number (Default: 8000)',default=8000,dest='port',type=int)

args = parser.parse_args()
print(args)

os.chdir(args.path)

#if sys.argv[1:]:path = sys.argv[1]

startServer(args.path,args.host,args.port);
