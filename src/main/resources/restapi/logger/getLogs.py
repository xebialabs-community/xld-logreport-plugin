# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import ch.qos.logback.core.Appender as LogAppender
import ch.qos.logback.core.util.COWArrayList as COWArrayList
import ch.qos.logback.classic.encoder.PatternLayoutEncoder as PatternLayoutEncoder
import ch.qos.logback.core.FileAppender as FileAppender

import org.slf4j.LoggerFactory as LoggerFactory
import ch.qos.logback.classic.Level as logLevels
import json
import os
import re

def createLogAppender( name="ROOT", file="log/deployit.log" ):
    lc = LoggerFactory.getILoggerFactory()
    ple = PatternLayoutEncoder()
    ple.setPattern("%date %level [%thread] %logger{10} [%file:%line] %msg%n")
    ple.setContext(lc)
    ple.start()
    fileAppender = FileAppender()
    fileAppender.setFile(file)
    fileAppender.setEncoder(ple)
    fileAppender.setContext(lc)
    fileAppender.start()

    logger = LoggerFactory.getLogger(name)
    logger.addAppender(fileAppender)
    #logger.setLevel(logLevels.DEBUG)
    # set to true if root should log too
    logger.setAdditive(True)
    return logger

#def tail(f, n, offset=0):
def tail(f, n, offset=0):
    myLogger = LoggerFactory.getLogger("logmanager")
    avg_line_length = 74
    to_read = n + (offset or 0)

    while 1:
        try:
            fo = open(f, "r+")
            fo.seek(-(avg_line_length * to_read), 2)
        except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
            myLogger.error("wooops file is too small")
            fo.seek(0)
        except:
            myLogger.error("Invalid request")
        pos = fo.tell()
        lines = fo.read().splitlines(True)
        if len(lines) >= to_read or pos == 0:
            fo.close()
            #return lines[-to_read:offset and -offset or None], \
            #       len(lines) > to_read or pos > 0
            #return lines[-to_read:offset and -offset or None]
            return lines
        if len(lines) < 5:
            fo.close()
            return lines

        avg_line_length = int( avg_line_length * 1.3 + 0.5 )

myLogger = LoggerFactory.getLogger("logmanager")
filename = request.query['file']
numberOfLines = request.query['numberOfLines']
myLogger.debug("filename = %s" % filename)
if ( os.path.isfile( filename ) == False ):
    myLogger.info("filename %s does not exist" % filename)
    createLogAppender( "ROOT", filename )
    myLogger.error("Log file %s create for ROOT appender" % filename)

lines = tail( filename, int(numberOfLines) )
response.entity = {"status": "OK", "logLines": lines}
