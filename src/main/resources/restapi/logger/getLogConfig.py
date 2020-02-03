# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import org.slf4j.LoggerFactory as LoggerFactory
import ch.qos.logback.classic.Level as logLevels
import json

def getLogLevel( loggerName="console" ):
    loggerMap = []
    myLogger = LoggerFactory.getLogger("logmanager")
    logger = LoggerFactory.getLogger(loggerName)

    loggerContext = LoggerFactory.getILoggerFactory()
    loggerList = loggerContext.getLoggerList()
    myLogger.info("===================")
    for loggerItem in loggerList:
        if loggerItem.getLevel() is not None:
            myLogger.info("%s = %s" % (loggerItem.getName(), loggerItem.getLevel()))
            loggerMap.append({"logger": loggerItem.getName(), "level": loggerItem.getLevel().toString()})
        else:
            myLogger.info("%s = %s" % (loggerItem.getName(), ""))
            loggerMap.append({"logger": loggerItem.getName(), "level": ""})
    myLogger.info("===================")
    return loggerMap


def setLogLevel( loggerName="console", logLevel = "DEBUG"):
    loggerMap = {}
    logLevel = logLevel.upper()
    loggerContext = LoggerFactory.getILoggerFactory()
    loggerList = loggerContext.getLoggerList()
    for loggerItem in loggerList:
        if( loggerItem.getName() == loggerName ):
            myLogger.info("Setting %s to %s" % (loggerName, logLevel))
            loggerItem.setLevel( logLevels.toLevel( logLevel ) )
            myLogger.info("%s = %s" % (loggerName, logLevel))
        #myLogger.error("%s != %s" % (loggerItem.getName(), loggerName))
    return

myLogger = LoggerFactory.getLogger("logmanager")
verb = "GET"

if (request):
    if (request.query):
        if (request.query['verb']):
            verb = request.query['verb']

if( verb == "SET"):
    loggerName = request.query['logger']
    logLevel = request.query['level']
    myLogger.info("Setting %s to %s" % (loggerName, logLevel))
    setLogLevel(loggerName, logLevel)

loggerMap = getLogLevel()
#loggerMap = {}
myLogger.debug("%s" % json.dumps(loggerMap, indent=4, sort_keys=True))
response.entity = {"status": "OK", "data":loggerMap }
